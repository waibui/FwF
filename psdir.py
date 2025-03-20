import argparse
import asyncio
import aiohttp
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import random
import time
from dataclasses import dataclass
import logging
from aiohttp import ClientSession

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('dir_scanner')

# Model - Data and business logic
@dataclass
class ScanResult:
    url: str
    status_code: int
    content_length: int
    response_time: float

class ScannerModel:
    def __init__(self, base_url: str, wordlist_path: str, extensions: List[str], 
                 user_agents: List[str], concurrency: int, timeout: int):
        self.base_url = base_url.rstrip('/')
        self.wordlist_path = wordlist_path
        self.extensions = extensions
        self.concurrency = concurrency
        self.timeout = timeout
        self.user_agents = user_agents if user_agents else ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"]
        self.results: List[ScanResult] = []
        
    def load_wordlist(self) -> List[str]:
        """Load the directory wordlist from file"""
        try:
            with open(self.wordlist_path, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"Wordlist file not found: {self.wordlist_path}")
            sys.exit(1)
            
    def get_paths_to_scan(self) -> List[str]:
        """Generate all paths to scan based on wordlist and extensions"""
        paths = []
        words = self.load_wordlist()
        
        # Add base directories
        paths.extend(words)
        
        # Add extensions if specified
        if self.extensions:
            for word in words:
                for ext in self.extensions:
                    ext = ext.lstrip('.')
                    paths.append(f"{word}.{ext}")
        
        return paths
        
    def add_result(self, result: ScanResult):
        """Add a scan result to the results list"""
        self.results.append(result)
        
    def get_results(self) -> List[ScanResult]:
        """Return all scan results"""
        return sorted(self.results, key=lambda x: x.url)
    
    def get_random_user_agent(self) -> str:
        """Return a random user agent from the list"""
        return random.choice(self.user_agents)

# View - Output formatting and user interface
class ScannerView:
    @staticmethod
    def print_banner():
        banner = """
        ###############################
        #  Directory Scanner Tool     #
        #  MVC Pattern with Asyncio   #
        ###############################
        """
        print(banner)
    
    @staticmethod
    def print_config(model: ScannerModel):
        print(f"\nTarget URL: {model.base_url}")
        print(f"Wordlist: {model.wordlist_path}")
        print(f"Extensions: {model.extensions if model.extensions else 'None'}")
        print(f"Concurrency: {model.concurrency}")
        print(f"Timeout: {model.timeout}s")
        print(f"User Agents: {len(model.user_agents)} configured\n")
        
    @staticmethod
    def print_progress(current: int, total: int):
        percent = (current / total) * 100
        sys.stdout.write(f"\rProgress: {current}/{total} ({percent:.1f}%)")
        sys.stdout.flush()
        
    @staticmethod
    def print_result(result: ScanResult):
        status_color = "\033[92m" if 200 <= result.status_code < 300 else "\033[94m" if 300 <= result.status_code < 400 else "\033[91m"
        reset_color = "\033[0m"
        print(f"{status_color}[{result.status_code}]{reset_color} {result.url} - {result.content_length} bytes - {result.response_time:.2f}s")
    
    @staticmethod
    def print_summary(results: List[ScanResult], duration: float):
        status_counts = {}
        
        for result in results:
            status = result.status_code
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1
            
        print("\n\n--- Scan Summary ---")
        print(f"Total URLs scanned: {len(results)}")
        print(f"Total time: {duration:.2f} seconds")
        print("Status code distribution:")
        
        for status, count in sorted(status_counts.items()):
            status_color = "\033[92m" if 200 <= status < 300 else "\033[94m" if 300 <= status < 400 else "\033[91m"
            reset_color = "\033[0m"
            print(f"  {status_color}{status}{reset_color}: {count}")

# Controller - Coordination and application flow
class ScannerController:
    def __init__(self, model: ScannerModel, view: ScannerView):
        self.model = model
        self.view = view
        
    async def scan_url(self, session: ClientSession, path: str) -> Optional[ScanResult]:
        """Scan a single URL and return the result"""
        url = f"{self.model.base_url}/{path}"
        headers = {"User-Agent": self.model.get_random_user_agent()}
        
        try:
            start_time = time.time()
            async with session.get(url, headers=headers, timeout=self.model.timeout, 
                                  allow_redirects=False) as response:
                response_time = time.time() - start_time
                content_length = len(await response.read())
                
                return ScanResult(
                    url=url,
                    status_code=response.status,
                    content_length=content_length,
                    response_time=response_time
                )
        except asyncio.TimeoutError:
            logger.debug(f"Timeout on {url}")
            return None
        except Exception as e:
            logger.debug(f"Error scanning {url}: {str(e)}")
            return None
    
    async def scan_worker(self, queue: asyncio.Queue, session: ClientSession, 
                        progress_counter: Dict[str, int], total_paths: int):
        """Worker to process URLs from the queue"""
        while True:
            try:
                path = await queue.get()
                result = await self.scan_url(session, path)
                
                if result:
                    # Interesting results are 200s, 30Xs, or specific status codes
                    if (200 <= result.status_code < 400) or result.status_code == 401 or result.status_code == 403:
                        self.model.add_result(result)
                        self.view.print_result(result)
                
                # Update progress
                progress_counter["scanned"] += 1
                if progress_counter["scanned"] % 10 == 0:
                    self.view.print_progress(progress_counter["scanned"], total_paths)
                    
                queue.task_done()
            except Exception as e:
                logger.error(f"Worker error: {str(e)}")
                queue.task_done()
    
    async def run_scan(self):
        """Run the directory scan"""
        self.view.print_banner()
        self.view.print_config(self.model)
        
        paths = self.model.get_paths_to_scan()
        total_paths = len(paths)
        
        print(f"Loaded {total_paths} paths to scan")
        print("Starting scan...\n")
        
        start_time = time.time()
        progress_counter = {"scanned": 0}
        
        # Create queue and workers
        queue = asyncio.Queue()
        
        # Custom TCP connector with limit on connections
        connector = aiohttp.TCPConnector(limit=self.model.concurrency)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            # Create workers
            workers = []
            for _ in range(self.model.concurrency):
                worker = asyncio.create_task(
                    self.scan_worker(queue, session, progress_counter, total_paths)
                )
                workers.append(worker)
            
            # Add paths to queue
            for path in paths:
                await queue.put(path)
                
            # Wait for all tasks to be processed
            await queue.join()
            
            # Cancel worker tasks
            for worker in workers:
                worker.cancel()
            
            # Wait until all worker tasks are cancelled
            await asyncio.gather(*workers, return_exceptions=True)
        
        duration = time.time() - start_time
        self.view.print_summary(self.model.get_results(), duration)

def load_user_agents(file_path: Optional[str]) -> List[str]:
    """Load user agents from a file if provided"""
    default_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    ]
    
    if not file_path:
        return default_agents
        
    try:
        with open(file_path, 'r') as f:
            agents = [line.strip() for line in f if line.strip()]
            return agents if agents else default_agents
    except FileNotFoundError:
        logger.warning(f"User agents file not found: {file_path}, using defaults")
        return default_agents

def main():
    parser = argparse.ArgumentParser(description="Directory Scanner Tool")
    parser.add_argument("url", help="Target URL to scan")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("-e", "--extensions", help="Comma-separated list of extensions to append (e.g., php,html,txt)")
    parser.add_argument("-c", "--concurrency", type=int, default=10, help="Number of concurrent requests (default: 10)")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Request timeout in seconds (default: 5)")
    parser.add_argument("-a", "--user-agents", help="Path to file containing user agents")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Set log level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Process extensions
    extensions = []
    if args.extensions:
        extensions = [ext.strip() for ext in args.extensions.split(",")]
    
    # Load user agents
    user_agents = load_user_agents(args.user_agents)
    
    # Create MVC components
    model = ScannerModel(
        base_url=args.url,
        wordlist_path=args.wordlist,
        extensions=extensions,
        user_agents=user_agents,
        concurrency=args.concurrency,
        timeout=args.timeout
    )
    
    view = ScannerView()
    controller = ScannerController(model, view)
    
    # Run the scan
    asyncio.run(controller.run_scan())

if __name__ == "__main__":
    main()