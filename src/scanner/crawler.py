import re
import aiohttp
from typing import Set, List, Optional
from urllib.parse import urljoin, urlparse
from src.models.config import ScanConfig
from src.output.logger import Logger

logger = Logger.get_instance()

class WebCrawler:
    """Crawls a website to discover URLs and paths."""
    
    def __init__(self, config: ScanConfig):
        self.config = config
        self.visited_urls: Set[str] = set()
        self.url_queue: List[str] = []
        self.found_urls: Set[str] = set()
        self.skip_extensions = {
            '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
            '.mp3', '.mp4', '.wav', '.avi', '.mov', '.flv', '.wmv',
            '.zip', '.tar', '.gz', '.rar', '.7z', '.pdf', '.doc', 
            '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.exe'
        }
    
    async def crawl(self, start_url: str, max_depth: int = 1) -> Set[str]:
        """
        Crawl a website starting from the given URL up to the specified depth.
        
        Args:
            start_url: The URL to start crawling from
            max_depth: Maximum depth to crawl (1 = only the start page)
            
        Returns:
            Set of discovered URLs
        """
        self.url_queue = [(start_url, 0)]  
        self.visited_urls = set()
        self.found_urls = set()
        
        connector = aiohttp.TCPConnector(
            limit=self.config.concurrency,
            ssl=False
        )
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            while self.url_queue:
                url, depth = self.url_queue.pop(0)
                
                if url in self.visited_urls or depth > max_depth:
                    continue
                
                parsed_url = urlparse(url)
                if any(parsed_url.path.endswith(ext) for ext in self.skip_extensions):
                    continue
                
                self.visited_urls.add(url)
                self.found_urls.add(url)
                
                if depth == max_depth:
                    continue
                
                try:
                    headers = {"User-Agent": "FwFCrawler/1.0"}
                    async with session.get(url, allow_redirects=True, headers=headers) as response:
                        if response.status == 200 and 'text/html' in response.headers.get('Content-Type', ''):
                            html = await response.text()
                            new_urls = self._extract_urls(html, url)
                            
                            for new_url in new_urls:
                                if new_url not in self.visited_urls:
                                    self.url_queue.append((new_url, depth + 1))
                except Exception as e:
                    logger.debug("Crawler", f"Error crawling {url}: {str(e)}")
        
        return self.found_urls
    
    def _extract_urls(self, html: str, base_url: str) -> Set[str]:
        """Extract URLs from HTML content."""
        urls = set()
        
        href_pattern = re.compile(r'href=[\'"]?([^\'" >]+)', re.IGNORECASE)
        for match in href_pattern.finditer(html):
            href = match.group(1)
            full_url = urljoin(base_url, href)
            
            if self._is_same_domain(base_url, full_url):
                urls.add(full_url)
        
        src_pattern = re.compile(r'src=[\'"]?([^\'" >]+)', re.IGNORECASE)
        for match in src_pattern.finditer(html):
            src = match.group(1)
            full_url = urljoin(base_url, src)
            
            if self._is_same_domain(base_url, full_url):
                urls.add(full_url)
                
        action_pattern = re.compile(r'action=[\'"]?([^\'" >]+)', re.IGNORECASE)
        for match in action_pattern.finditer(html):
            action = match.group(1)
            full_url = urljoin(base_url, action)
            
            if self._is_same_domain(base_url, full_url):
                urls.add(full_url)
        
        clean_urls = {url.split('#')[0] for url in urls}
        
        return clean_urls
    
    def _is_same_domain(self, url1: str, url2: str) -> bool:
        """Check if two URLs belong to the same domain."""
        domain1 = urlparse(url1).netloc
        domain2 = urlparse(url2).netloc
        
        if not domain2:
            return True
            
        return domain1 == domain2