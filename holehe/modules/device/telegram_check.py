import httpx

async def telegram_check(phone, client, out):
    """
    Check if a phone number is registered on Telegram.
    Uses Telegram's auth.checkPhone-like method via web.
    """
    name = "telegram"
    domain = "telegram.org"
    method = "login-check"
    
    try:
        clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not clean_phone.startswith('+'):
            clean_phone = '+' + clean_phone
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://my.telegram.org',
            'Referer': 'https://my.telegram.org/auth',
        }
        
        # Telegram's auth page - sending phone number
        # This sends a code to the user BUT we can detect if the number is registered
        # based on the response
        response = await client.post(
            'https://my.telegram.org/auth/send_password',
            headers=headers,
            data={'phone': clean_phone},
            timeout=10
        )
        
        if response.status_code == 200:
            try:
                data = response.json()
                # If Telegram accepts the phone, account exists
                if data.get('random_hash'):
                    out.append({
                        "name": name, "domain": domain, "method": method,
                        "frequent_rate_limit": False,
                        "rateLimit": False, "exists": True,
                        "emailrecovery": None, "phoneNumber": clean_phone,
                        "others": {"note": "Telegram account exists, login code sent"}
                    })
                    return
            except Exception:
                pass
        
        # Check if error indicates "not registered"
        resp_text = response.text.lower() if response.text else ""
        if 'not registered' in resp_text or 'no account' in resp_text:
            out.append({
                "name": name, "domain": domain, "method": method,
                "frequent_rate_limit": False,
                "rateLimit": False, "exists": False,
                "emailrecovery": None, "phoneNumber": clean_phone,
                "others": None
            })
        else:
            out.append({
                "name": name, "domain": domain, "method": method,
                "frequent_rate_limit": True,
                "rateLimit": True, "exists": False,
                "emailrecovery": None, "phoneNumber": clean_phone,
                "others": None
            })
            
    except Exception:
        out.append({
            "name": name, "domain": domain, "method": method,
            "frequent_rate_limit": True,
            "rateLimit": True, "exists": False,
            "emailrecovery": None, "phoneNumber": None,
            "others": None
        })
