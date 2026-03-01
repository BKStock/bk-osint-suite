import httpx
import hashlib
import base64

async def imessage_check(phone, client, out):
    """
    Check if a phone number has iMessage enabled (= iPhone/iPad).
    Uses Apple's IDS (Identity Services) lookup.
    
    Note: This is a simplified check using Apple's public-facing
    validation endpoint. For production use, pypush library is recommended.
    """
    name = "imessage"
    domain = "apple.com"
    method = "lookup"
    
    try:
        # Method 1: Apple IDS lookup via iMessage registration check
        # Apple's servers respond differently for iMessage-enabled numbers
        headers = {
            'User-Agent': 'com.apple.madrid-lookup [macOS,13.0,22A380,MacBookPro18,1]',
            'Content-Type': 'application/x-apple-plist',
        }
        
        # Normalize phone number
        clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not clean_phone.startswith('+'):
            clean_phone = '+' + clean_phone
        
        # Try Apple's validation service
        # This endpoint checks if a phone number is registered with Apple services
        lookup_url = "https://profile.ess.apple.com/WebObjects/VCProfileService.woa/wa/isPhoneNumberAnisetted"
        
        response = await client.post(
            lookup_url,
            headers=headers,
            json={"phoneNumber": clean_phone},
            timeout=10
        )
        
        if response.status_code == 200:
            resp_text = response.text.lower()
            if 'true' in resp_text or '"registered":true' in resp_text:
                out.append({
                    "name": name, "domain": domain, "method": method,
                    "frequent_rate_limit": False,
                    "rateLimit": False, "exists": True,
                    "emailrecovery": None, "phoneNumber": clean_phone,
                    "others": {"device": "iPhone/iPad", "service": "iMessage"}
                })
                return
        
        # Method 2: FaceTime availability check (also Apple-only)
        facetime_url = "https://profile.ess.apple.com/WebObjects/VCProfileService.woa/wa/isFaceTimeAvailable"
        response2 = await client.post(
            facetime_url,
            headers=headers,
            json={"phoneNumber": clean_phone},
            timeout=10
        )
        
        if response2.status_code == 200:
            resp_text2 = response2.text.lower()
            if 'true' in resp_text2 or 'available' in resp_text2:
                out.append({
                    "name": name, "domain": domain, "method": "facetime",
                    "frequent_rate_limit": False,
                    "rateLimit": False, "exists": True,
                    "emailrecovery": None, "phoneNumber": clean_phone,
                    "others": {"device": "iPhone/iPad", "service": "FaceTime"}
                })
                return
        
        # Not found = likely Android
        out.append({
            "name": name, "domain": domain, "method": method,
            "frequent_rate_limit": False,
            "rateLimit": False, "exists": False,
            "emailrecovery": None, "phoneNumber": clean_phone,
            "others": {"device": "Android (probable)", "service": "iMessage not found"}
        })
        
    except Exception:
        out.append({
            "name": name, "domain": domain, "method": method,
            "frequent_rate_limit": True,
            "rateLimit": True, "exists": False,
            "emailrecovery": None, "phoneNumber": None,
            "others": None
        })
