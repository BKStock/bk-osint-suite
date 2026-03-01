import httpx

async def whatsapp_check(phone, client, out):
    """
    Check if a phone number is registered on WhatsApp and detect device type.
    Uses WhatsApp's registration/exists check endpoint.
    """
    name = "whatsapp"
    domain = "whatsapp.com"
    method = "exists-check"
    
    try:
        clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
        
        # Method 1: WhatsApp contact check via web API
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'Origin': 'https://web.whatsapp.com',
            'Referer': 'https://web.whatsapp.com/',
        }
        
        # WhatsApp's registration check
        # v2 registration endpoint responds with whether number exists
        reg_url = f"https://v.whatsapp.net/v2/exists?phone={clean_phone}"
        
        response = await client.get(
            reg_url,
            headers={
                'User-Agent': 'WhatsApp/2.23.20.0 A',
                'Accept': 'application/json',
            },
            timeout=10
        )
        
        if response.status_code == 200:
            try:
                data = response.json()
                exists = data.get('status') == 'ok' or data.get('exists', False)
                device_info = None
                
                # Try to extract device info from response headers or body
                user_agent = data.get('user_agent', '')
                if 'iPhone' in str(data) or 'iOS' in str(data):
                    device_info = "iPhone"
                elif 'Android' in str(data) or 'Samsung' in str(data):
                    device_info = "Android"
                
                out.append({
                    "name": name, "domain": domain, "method": method,
                    "frequent_rate_limit": False,
                    "rateLimit": False, "exists": exists,
                    "emailrecovery": None, "phoneNumber": clean_phone,
                    "others": {"device": device_info} if device_info else None
                })
                return
            except Exception:
                pass
        
        # Method 2: WhatsApp Business API check
        biz_url = "https://graph.facebook.com/v18.0/waba_phone_numbers"
        response2 = await client.get(
            f"https://wa.me/{clean_phone}",
            headers=headers,
            timeout=10,
            follow_redirects=True
        )
        
        # If wa.me redirects to actual chat = number exists on WhatsApp
        if response2.status_code == 200:
            page_text = response2.text.lower()
            if 'send message' in page_text or 'chat' in page_text or 'whatsapp' in page_text:
                # Check for device hints in page
                device_info = None
                if 'iphone' in page_text:
                    device_info = "iPhone"
                elif 'android' in page_text:
                    device_info = "Android"
                
                out.append({
                    "name": name, "domain": domain, "method": "wa.me",
                    "frequent_rate_limit": False,
                    "rateLimit": False, "exists": True,
                    "emailrecovery": None, "phoneNumber": clean_phone,
                    "others": {"device": device_info} if device_info else None
                })
                return
        
        out.append({
            "name": name, "domain": domain, "method": method,
            "frequent_rate_limit": False,
            "rateLimit": False, "exists": False,
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
