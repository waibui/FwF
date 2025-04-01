```
██████╗ ███████╗██████╗ ██╗██████╗  
██╔══██╗██╔════╝██╔══██╗██║██╔══██╗  AUTHOR: waibui
██████╔╝███████╗██║  ██║██║██████╔╝  
██╔═══╝ ╚════██║██║  ██║██║██╔══██╗ 
██║     ███████║██████╔╝██║██║  ██║ 
╚═╝     ╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝  
```
# PSDIR - Web path scanner

## Installation

* Use git: `git clone https://github.com/waibui/psdir.git`

* Download zip file: [https://github.com/waibui/psdir.git](https://github.com/waibui/psdir/archive/refs/heads/main.zip)

## Option
```
usage: psdir.py [-u|--url] target [options].

psdir - Web Path Scanner

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Target URL
  -w WORDLIST, --wordlist WORDLIST
                        Path to wordlist file(s)
  -ua USER_AGENT, --user-agent USER_AGENT
                        Path to user-agent file(s)
  -c CONCURRENCY, --concurrency CONCURRENCY
                        Number of threads
  -t TIMEOUT, --timeout TIMEOUT
                        Connection timeout in seconds
  -m HTTP_METHOD, --http-method HTTP_METHOD
                        HTTP method
  -mc MATCH_CODE, --match-code MATCH_CODE
                        Match HTTP status codes

HTTP Settings:
  --cookie COOKIE       Cookies for requests (e.g., 'key=value; key2=value2')
  --proxies PROXIES     Proxy for requests (e.g., 'http://user:pass@proxy.com:8080')
  -ar, --allow-redirect
                        Allow HTTP redirects (true/false)
  -s, --scrape          Scrape <a> tags and request their URLs
  -rl RATE_LIMIT, --rate-limit RATE_LIMIT
                        Limit requests per second (default: unlimited)

Output Settings:
  -o OUTPUT, --output OUTPUT
                        Save output to a file (.txt, .log, .json)

See 'config/settings.py' for the example configuration file
```
## Usage
```python3 psdir.py [-u|--url] target [options]```

Recommend using `Virtual Enviroment` (*venv*) to avoid library conflict.
---
[More infomation...](https://waibui.github.io/2025/03/psdir-web-path-scan-tool/)