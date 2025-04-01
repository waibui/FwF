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
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  CORE SETTINGS:
    -u URL, --url=URL   Target URL, eg: https://example.com,
                        http://example.com
    -w WORDLISTS, --wordlists=WORDLISTS
                        Wordlist files or directories contain wordlists
    --ua=USER_AGENT, --user-agent=USER_AGENT
                        User-Agent files or directories contain useragent

  PERFORMENT & REQUEST SETTINGS:
    -t THREADS, --threads=THREADS
                        Number of threads (default: 40)
    --to=TIMEOUT, --timeout=TIMEOUT
                        Connection timeout in seconds
    -m METHOD, --http-method=METHOD
                        HTTP method (default: GET)
    --mc=MATCH_CODE, --match-code=MATCH_CODE
                        Match HTTP status code
                        (default:200,204,301,302,307,401,403)
    --cookie=COOKIE     The cookie of the requests, eg: key:value
    --proxies=PROXY     PROXY for requests, eg:
                        https://username:password@proxy.example.com:8080,
                        https://proxy.example.com:8080
    --ar=ALLOW_REDIRECT, --allow-redirect=ALLOW_REDIRECT
                        Accept redirect in request

  OUTPUT & LOGGING SETTINGS:
    -o FILE, --output=FILE
                        Save output to a file

See 'core/setting.py' for the example configuration file
```
## Usage
```python3 psdir.py [-u|--url] target [options]```