# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (C) 2025 waibui
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  Author: waibui

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