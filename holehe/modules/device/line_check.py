import httpx

async def line_check(phone, client, out):
    """
    Check if a phone number is registered on LINE.
    """
    name = "line"
    domain = "line.me"
    method = "register-check"
    
    try:
        clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'X-Line-Application': 'CHROMEOS\t3.0.0\tChrome OS\t1',
        }
        
        # LINE's account recovery endpoint
        response = await client.post(
            'https://gd2.line.naver.jp/Q',
            headers=headers,
            json={"phone": clean_phone, "region": "JP"},
            timeout=10
        )
        
        resp_text = response.text.lower() if response.text else ""
        
        if response.status_code == 200:
            if 'exist' in resp_text or 'registered' in resp_text or 'found' in resp_text:
                out.append({
                    "name": name, "domain": domain, "method": method,
                    "frequent_rate_limit": False,
                    "rateLimit": False, "exists": True,
                    "emailrecovery": None, "phoneNumber": clean_phone,
                    "others": None
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
