from holehe.core import *
from holehe.localuseragent import *


async def cloudbet(email, client, out):
    name = "cloudbet"
    domain = "cloudbet.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'https://www.cloudbet.com',
        'Referer': 'https://www.cloudbet.com/',
    }

    try:
        data = {"email": email}
        response = await client.post(
            'https://www.cloudbet.com/api/user/register/check-email',
            headers=headers,
            json=data,
            timeout=10
        )
        resp_text = response.text.lower()

        if response.status_code == 200 or response.status_code == 201:
            if 'already' in resp_text or 'exist' in resp_text or 'registered' in resp_text or 'duplicate' in resp_text:
                out.append({"name": name, "domain": domain, "method": "register",
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": True,
                    "emailrecovery": None, "phoneNumber": None, "others": None})
                return
            if 'not found' in resp_text or 'not exist' in resp_text or 'no account' in resp_text or 'not registered' in resp_text or 'invalid' in resp_text:
                out.append({"name": name, "domain": domain, "method": "register",
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": False,
                    "emailrecovery": None, "phoneNumber": None, "others": None})
                return

        # Fallback endpoint 2
        data2 = {"email": email}
        response2 = await client.post(
            'https://www.cloudbet.com/api/user/forgot-password',
            headers=headers,
            json=data2,
            timeout=10
        )
        resp_text2 = response2.text.lower()

        if response2.status_code == 200 or response2.status_code == 201:
            if 'already' in resp_text2 or 'exist' in resp_text2 or 'registered' in resp_text2 or 'success' in resp_text2 or 'sent' in resp_text2:
                out.append({"name": name, "domain": domain, "method": "forgot-password",
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": True,
                    "emailrecovery": None, "phoneNumber": None, "others": None})
                return
            if 'not found' in resp_text2 or 'not exist' in resp_text2 or 'no account' in resp_text2 or 'not registered' in resp_text2:
                out.append({"name": name, "domain": domain, "method": "forgot-password",
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": False,
                    "emailrecovery": None, "phoneNumber": None, "others": None})
                return

        # Could not determine, mark as rate limited
        out.append({"name": name, "domain": domain, "method": method,
            "frequent_rate_limit": frequent_rate_limit,
            "rateLimit": True, "exists": False,
            "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method,
            "frequent_rate_limit": frequent_rate_limit,
            "rateLimit": True, "exists": False,
            "emailrecovery": None, "phoneNumber": None, "others": None})
