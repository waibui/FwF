# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (c) 2025 waibui
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from lxml import html
from urllib.parse import urljoin, urlparse

def extract_links(self, base_url, html_content):
    try:
        if not html_content.strip():
            return []
        
        if isinstance(html_content, str):
            html_content = html_content.encode('utf-8')
            
        tree = html.fromstring(html_content)
        links = []
        
        for link in tree.xpath('//a[@href]'):
            href = link.get('href')
            if href:
                absolute_url = urljoin(base_url, href)
                if (absolute_url not in self.crawled_links and 
                    not href.startswith('#') and 
                    not href.startswith('javascript:') and
                    not href.startswith('mailto:') and
                    not href.startswith('tel:')):
                    
                    base_domain = urlparse(self.args.url).netloc
                    link_domain = urlparse(absolute_url).netloc
                    
                    if base_domain == link_domain:
                        links.append(absolute_url)
                        self.crawled_links.add(absolute_url)
                        self.extracted_links.append(absolute_url)
        
        return links
    except Exception:
        return []