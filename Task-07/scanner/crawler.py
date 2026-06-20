import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from scanner.utils import is_internal_url, clean_url

class WebCrawler:
    """
    Crawls a target website to extract all internal links, query parameters,
    and HTML forms.
    """
    def __init__(self, base_url, session=None, logger=None):
        self.base_url = clean_url(base_url)
        self.session = session or requests.Session()
        self.logger = logger
        self.visited_urls = set()
        self.discovered_forms = []
        self.discovered_parameters = {}  # {url: [param1, param2, ...]}
        
    def _log(self, message, level="info"):
        if self.logger:
            if level == "info":
                self.logger.info(message)
            elif level == "debug":
                self.logger.debug(message)
            elif level == "warn":
                self.logger.warning(message)
            elif level == "error":
                self.logger.error(message)

    def extract_forms(self, url, html_content):
        """
        Extracts all HTML forms from a given page.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        forms = soup.find_all('form')
        extracted_forms = []
        
        for index, form in enumerate(forms):
            action = form.attrs.get('action', '')
            method = form.attrs.get('method', 'get').lower()
            
            # Resolve relative action URL to absolute URL
            form_url = urljoin(url, action)
            form_url = clean_url(form_url)
            
            # Extract inputs
            inputs = []
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                name = input_tag.attrs.get('name')
                input_type = input_tag.attrs.get('type', 'text').lower()
                value = input_tag.attrs.get('value', '')
                
                # We only care about inputs that have names (which are submitted to server)
                if name:
                    inputs.append({
                        'name': name,
                        'type': input_type,
                        'value': value
                    })
            
            form_data = {
                'url': form_url,
                'method': method,
                'inputs': inputs,
                'source_url': url
            }
            extracted_forms.append(form_data)
            
            self._log(f"Discovered Form [{method.upper()}] at {form_url} with {len(inputs)} inputs", "debug")
            
        return extracted_forms

    def extract_links_and_params(self, url, html_content):
        """
        Extracts all internal links and checks for query parameters.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all('a')
        found_links = set()
        
        for link in links:
            href = link.attrs.get('href', '')
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue
                
            # Resolve relative URL
            absolute_url = urljoin(url, href)
            cleaned_url = clean_url(absolute_url)
            
            # Check if it is an internal link (belongs to same domain)
            if is_internal_url(cleaned_url, self.base_url):
                found_links.add(cleaned_url)
                
                # Check for GET query parameters in the link
                parsed_url = urlparse(absolute_url)
                if parsed_url.query:
                    # Extract parameter names
                    params = [p.split('=')[0] for p in parsed_url.query.split('&') if p]
                    base_path = clean_url(absolute_url.split('?')[0])
                    
                    if base_path not in self.discovered_parameters:
                        self.discovered_parameters[base_path] = set()
                    for p in params:
                        if p:
                            self.discovered_parameters[base_path].add(p)
                            
        # Convert param sets to lists
        for k in self.discovered_parameters:
            if isinstance(self.discovered_parameters[k], set):
                self.discovered_parameters[k] = list(self.discovered_parameters[k])
                
        return found_links

    def crawl_page(self, url):
        """
        Crawls a single URL, extracts links/forms/params.
        """
        url = clean_url(url)
        if url in self.visited_urls:
            return set()
            
        self.visited_urls.add(url)
        self._log(f"Crawling URL: {url}")
        
        try:
            # Send GET request with a timeout
            response = self.session.get(url, timeout=10, allow_redirects=True)
            
            # Ensure the response is HTML
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                self._log(f"Skipping non-HTML page: {url} (Content-Type: {content_type})", "debug")
                return set()
                
            # Check for URL parameters in the current URL itself
            parsed_url = urlparse(url)
            if parsed_url.query:
                base_path = clean_url(url.split('?')[0])
                params = [p.split('=')[0] for p in parsed_url.query.split('&') if p]
                if base_path not in self.discovered_parameters:
                    self.discovered_parameters[base_path] = set()
                for p in params:
                    if p:
                        self.discovered_parameters[base_path].add(p)
            
            # Parse forms
            forms = self.extract_forms(url, response.text)
            self.discovered_forms.extend(forms)
            
            # Parse links and parameters
            links = self.extract_links_and_params(url, response.text)
            return links
            
        except requests.exceptions.RequestException as e:
            self._log(f"Failed to crawl {url}: {str(e)}", "warn")
            return set()

    def start(self, max_depth=3):
        """
        Performs recursive crawling up to the specified max_depth.
        """
        self._log(f"Starting crawl on target: {self.base_url} (Max Depth: {max_depth})")
        
        current_depth_urls = {self.base_url}
        
        for depth in range(max_depth):
            if not current_depth_urls:
                break
                
            self._log(f"Crawling depth level {depth + 1}...")
            next_depth_urls = set()
            
            for url in current_depth_urls:
                if url not in self.visited_urls:
                    discovered = self.crawl_page(url)
                    next_depth_urls.update(discovered)
                    
            # Filter next depth URLs to keep only unvisited internal ones
            current_depth_urls = {
                u for u in next_depth_urls 
                if u not in self.visited_urls and is_internal_url(u, self.base_url)
            }
            
        self._log(f"Crawling completed. Visited {len(self.visited_urls)} page(s). Discovered {len(self.discovered_forms)} form(s).")
        
        # Clean up parameter sets
        for k in self.discovered_parameters:
            if isinstance(self.discovered_parameters[k], set):
                self.discovered_parameters[k] = list(self.discovered_parameters[k])
                
        return {
            'visited_urls': list(self.visited_urls),
            'forms': self.discovered_forms,
            'params': self.discovered_parameters
        }
