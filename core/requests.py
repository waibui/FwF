
import requests
from models.scan_config import ScannerConfig

def request(session: requests.Session, path: str, configs: ScannerConfig, user_agent: str):
    url = f"{configs.url.rstrip('/')}/{path.lstrip('/')}"
    
    headers = {
        "User-Agent": user_agent,
    }
    kwargs = {
        "headers": headers, 
        "timeout": configs.timeout,
        "allow_redirects": configs.allow_redirect,
    }
    
    if configs.cookie:
        kwargs["cookies"] = configs.cookie  
    if configs.proxies:
        kwargs["proxies"] = configs.proxies  
        
    try:
        request_func = getattr(session, configs.http_method.lower(), session.get)
        response = request_func(url=url, **kwargs)
        if response.status_code in configs.match_code:
            return [response.status_code, url]
    except requests.RequestException:
        return None