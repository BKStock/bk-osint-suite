"""
BK OSINT Suite - Phone Number Checker
Usage: python -m holehe.phone_check +819012345678
"""
import sys
import trio
import httpx
from holehe.modules.device.imessage_check import imessage_check
from holehe.modules.device.whatsapp_check import whatsapp_check
from holehe.modules.device.telegram_check import telegram_check
from holehe.modules.device.line_check import line_check

async def check_phone(phone):
    results = []
    async with httpx.AsyncClient() as client:
        async with trio.open_nursery() as nursery:
            nursery.start_soon(imessage_check, phone, client, results)
            nursery.start_soon(whatsapp_check, phone, client, results)
            nursery.start_soon(telegram_check, phone, client, results)
            nursery.start_soon(line_check, phone, client, results)
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m holehe.phone_check <phone_number>")
        print("Example: python -m holehe.phone_check +819012345678")
        sys.exit(1)
    
    phone = sys.argv[1]
    print(f"\n{'='*50}")
    print(f"  BK OSINT Suite - Phone Check")
    print(f"  Target: {phone}")
    print(f"{'='*50}\n")
    
    results = trio.run(check_phone, phone)
    
    # Determine device
    device = "Unknown"
    for r in results:
        if r['name'] == 'imessage' and r['exists']:
            device = "iPhone / iPad"
            break
        elif r['name'] == 'imessage' and not r['exists'] and not r['rateLimit']:
            device = "Android (probable)"
    
    print(f"  Device: {device}\n")
    
    for r in results:
        status = "[+]" if r['exists'] else "[x]" if r['rateLimit'] else "[-]"
        extra = ""
        if r.get('others') and isinstance(r['others'], dict):
            extra = f" | {r['others']}"
        print(f"  {status} {r['name']:12s} ({r['domain']}){extra}")
    
    print(f"\n{'='*50}")
    print(f"  [+] Registered  [-] Not found  [x] Rate limited")
    print(f"{'='*50}\n")

if __name__ == '__main__':
    main()
