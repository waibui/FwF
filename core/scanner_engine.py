import sys
import requests
import threading
import signal
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup

from models.scan_config import ScannerConfig
from views.logger import Logger
from core.utilities import Utilities
from core.requests import request

class ScannerEngine:
    
    def __init__(self, configs: ScannerConfig, wordlist: Queue, user_agent: list):
        self.configs = configs
        self.wordlist = wordlist
        self.user_agent = user_agent
        self.session = requests.Session()
        self.results = []
        self.stop_event = threading.Event()
        signal.signal(signal.SIGINT, self.handle_exit)

    def handle_exit(self, signum, frame):
        Logger.info("[!] Keyboard Interrupt detected! Stopping all threads immediately...")
        self.stop_event.set()
        sys.exit(1)

    def scan(self):
        try:
            with ThreadPoolExecutor(max_workers=self.configs.threads) as executor:
                futures = {executor.submit(self.worker, path): path for path in list(self.wordlist.queue)}
                
                for future in as_completed(futures):
                    if self.stop_event.is_set():
                        break
                    try:
                        result = future.result()
                        if result:
                            self.results.append(result)
                    except Exception as e:
                        Logger.error(f"[!] Worker error: {e}")

            if self.configs.output and not self.stop_event.is_set():
                self.save_results()
        except (KeyboardInterrupt, SystemExit):
            self.stop_event.set()
            Logger.info("[!] Stopping all workers...")
            sys.exit(1)
        except Exception as e:
            Logger.error(f"[!] Unexpected error: {e}")
            sys.exit(1)
        
        return self.results

    def worker(self, path):
        if self.stop_event.is_set():
            return None
        try:
            result = request(
                session=self.session,
                path=path,
                configs=self.configs,
                user_agent=Utilities.random_user_agent(self.user_agent)
            )
            if result and not self.stop_event.is_set():
                Logger.result_scan(*result)
                self.extract_and_scan_links(result[1])  # Extract and scan links from the response URL
                return result
        except Exception as e:
            if not self.stop_event.is_set():
                Logger.error(f"[!] Error scanning {path}: {e}")
        return None

    def extract_and_scan_links(self, url):
        try:
            response = self.session.get(url, timeout=self.configs.timeout)
            if response.status_code != 200:
                return
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            
            for link in links:
                if not link.startswith(('http://', 'https://')):
                    link = f"{self.configs.url.rstrip('/')}/{link.lstrip('/')}"
                
                link_status = self.check_link_status(link)
                if link_status:
                    Logger.result_scan(link_status, link)
        except Exception as e:
            Logger.error(f"[!] Error extracting links from {url}: {e}")

    def check_link_status(self, link):
        try:
            response = self.session.get(link, timeout=self.configs.timeout, allow_redirects=self.configs.allow_redirect)
            return response.status_code
        except requests.RequestException:
            return None

    def save_results(self):
        for file_path in map(str.strip, self.configs.output.split(",")):
            Logger.logging_to_file(file_path, self.results)
