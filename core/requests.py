import aiohttp
import random
from views.logger import Logger 

async def request(session, path, configs, user_agents):
    url = f"{configs.url.rstrip('/')}/{path.lstrip('/')}"
    headers = {"User-Agent": random.choice(user_agents)} 
    kwargs = {
        "headers": headers,
        "timeout": aiohttp.ClientTimeout(total=configs.timeout),
        "allow_redirects": configs.allow_redirect
    }
    
    if configs.cookie:
        kwargs["cookies"] = configs.cookie
    if configs.proxies:
        kwargs["proxy"] = configs.proxies  
    
    try:
        async with session.get(url, **kwargs) as response:
            if response.status in configs.match_code:
                Logger.info(f"[+] {response.status} - {url}")  
                return [response.status, url]
            
    except aiohttp.ClientError as e:
        Logger.error(f"[!] Request error for {url}: {e}")  
    
    return None
