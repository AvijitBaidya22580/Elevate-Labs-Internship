import os
import time
import requests
import threading
from datetime import datetime
from scanner.crawler import WebCrawler
from scanner.payloads import SQLI_PAYLOADS, XSS_PAYLOADS
from scanner.injector import inject_payload_in_url, inject_payload_in_form
from scanner.detector import check_sqli, check_xss, check_csrf, check_security_headers
from scanner.reporter import ReportGenerator
from scanner.utils import setup_logger, clear_logs

class VulnerabilityScanner:
    """
    Orchestrates the entire scanning lifecycle, managing crawling, payload injection,
    vulnerability detection, status tracking, and report generation.
    """
    def __init__(self, target_url, max_depth=3, custom_cookies=None, logger=None):
        self.target_url = target_url
        self.max_depth = max_depth
        self.logger = logger or setup_logger()
        
        # Parse and load cookies if provided as a string (e.g. 'PHPSESSID=12345; security=low')
        self.session = requests.Session()
        self.cookies = {}
        if custom_cookies:
            for cookie in custom_cookies.split(';'):
                if '=' in cookie:
                    k, v = cookie.strip().split('=', 1)
                    self.cookies[k] = v
            self.session.cookies.update(self.cookies)
            self.logger.info(f"Loaded {len(self.cookies)} custom cookie(s) for the scanning session.")
            
        # Status variables
        self.status = "idle"  # idle, crawling, scanning, compiling, completed, stopped
        self.progress_percentage = 0
        self.progress_text = "Ready to start"
        self.start_time = None
        self.end_time = None
        self.crawled_urls = []
        self.vulnerabilities = []
        
        # Thread control flags
        self.stop_event = threading.Event()

    def stop(self):
        """
        Signals the scanning thread to stop execution.
        """
        self.stop_event.set()
        self.status = "stopped"
        self.progress_text = "Scan aborted by user"
        self.logger.warning("Scan cancellation requested by the user.")

    def run(self):
        """
        Executes the vulnerability scan. Should be run in a separate thread.
        """
        try:
            self.stop_event.clear()
            self.start_time = datetime.now()
            self.status = "crawling"
            self.progress_percentage = 10
            self.progress_text = "Crawling website..."
            self.vulnerabilities = []
            
            self.logger.info(f"Initiating scan for: {self.target_url}")
            
            # Step 1: Reconnaissance (Crawling)
            crawler = WebCrawler(self.target_url, session=self.session, logger=self.logger)
            crawl_results = crawler.start(max_depth=self.max_depth)
            
            self.crawled_urls = crawl_results['visited_urls']
            discovered_forms = crawl_results['forms']
            discovered_params = crawl_results['params']
            
            if self.stop_event.is_set():
                self.status = "stopped"
                return
                
            # Step 2: Passive Scanning (CSRF and Headers checks)
            self.status = "scanning"
            self.progress_percentage = 30
            self.progress_text = "Checking security configurations..."
            self.logger.info("Executing passive security checks (CSRF & headers)...")
            
            # Form CSRF checks
            for form in discovered_forms:
                if self.stop_event.is_set():
                    self.status = "stopped"
                    return
                
                is_vuln, evidence = check_csrf(form)
                if is_vuln:
                    vuln = {
                        'vuln_type': 'CSRF (Missing Token)',
                        'severity': 'Medium',
                        'url': form['url'],
                        'method': form['method'].upper(),
                        'parameter': 'Form (No CSRF Input)',
                        'payload': 'N/A (Passive Check)',
                        'evidence': evidence,
                        'description': 'The form does not implement anti-CSRF tokens, leaving it vulnerable to Cross-Site Request Forgery.',
                        'owasp_category': 'A01:2025-Broken Access Control'
                    }
                    self.vulnerabilities.append(vuln)
                    self.logger.warning(f"Passive Vulnerability Found: CSRF at {form['url']}")
            
            # Header security checks on crawled URLs
            # We fetch a page's response headers to inspect security configurations
            for url in self.crawled_urls:
                if self.stop_event.is_set():
                    self.status = "stopped"
                    return
                    
                try:
                    res = self.session.head(url, timeout=5, allow_redirects=True)
                    header_vulns = check_security_headers(res.headers)
                    for hv in header_vulns:
                        hv['url'] = url
                        hv['method'] = 'HEAD/GET'
                        hv['parameter'] = 'HTTP Headers'
                        hv['payload'] = 'N/A (Passive Header Scan)'
                        self.vulnerabilities.append(hv)
                except Exception as e:
                    self.logger.debug(f"Failed to fetch headers for {url}: {str(e)}")

            if self.stop_event.is_set():
                self.status = "stopped"
                return

            # Step 3: Active Scanning (SQLi & XSS payload injection)
            self.progress_percentage = 50
            self.progress_text = "Injecting SQLi and XSS payloads..."
            self.logger.info("Executing active injection checks...")
            
            # Calculate total active tasks for progress tracking
            total_url_params = sum(len(params) for params in discovered_params.values())
            total_form_params = sum(len(form['inputs']) for form in discovered_forms)
            total_active_tasks = total_url_params + total_form_params
            
            completed_tasks = 0
            
            # Inject payloads into URL Parameters (GET)
            for url, params in discovered_params.items():
                for param in params:
                    if self.stop_event.is_set():
                        self.status = "stopped"
                        return
                        
                    self.logger.info(f"Scanning GET URL parameter: {param} on {url}")
                    
                    # 1. SQL Injection check
                    sqli_vuln = False
                    for payload in SQLI_PAYLOADS:
                        if self.stop_event.is_set():
                            self.status = "stopped"
                            return
                            
                        target_url, res = inject_payload_in_url(self.session, url, param, payload, cookies=self.cookies)
                        if res:
                            is_v, db_type, evidence = check_sqli(res.text)
                            if is_v:
                                vuln = {
                                    'vuln_type': 'SQL Injection',
                                    'severity': 'Critical',
                                    'url': url,
                                    'method': 'GET',
                                    'parameter': param,
                                    'payload': payload,
                                    'evidence': f"Database: {db_type}. Error matched: {evidence}",
                                    'description': 'SQL Injection vulnerability detected via database error message leakage. This allows unauthorized database read/write actions.',
                                    'owasp_category': 'A03:2025-Injection'
                                }
                                self.vulnerabilities.append(vuln)
                                self.logger.error(f"VULNERABILITY DETECTED: SQL Injection on parameter '{param}' at {url}")
                                sqli_vuln = True
                                break  # Break loop to test next param/vuln once confirmed
                                
                    # 2. XSS check (only if not already critically vulnerable to SQLi, or we can check both)
                    xss_vuln = False
                    for payload in XSS_PAYLOADS:
                        if self.stop_event.is_set():
                            self.status = "stopped"
                            return
                            
                        target_url, res = inject_payload_in_url(self.session, url, param, payload, cookies=self.cookies)
                        if res:
                            is_v, evidence = check_xss(payload, res.text)
                            if is_v:
                                vuln = {
                                    'vuln_type': 'Cross-Site Scripting (XSS)',
                                    'severity': 'High',
                                    'url': url,
                                    'method': 'GET',
                                    'parameter': param,
                                    'payload': payload,
                                    'evidence': evidence,
                                    'description': 'Reflected Cross-Site Scripting (XSS) detected. An attacker can inject and execute arbitrary client-side scripts in the context of the user session.',
                                    'owasp_category': 'A03:2025-Injection'
                                }
                                self.vulnerabilities.append(vuln)
                                self.logger.error(f"VULNERABILITY DETECTED: XSS on parameter '{param}' at {url}")
                                xss_vuln = True
                                break
                                
                    completed_tasks += 1
                    # Progress scale: 50% to 90% is active scanning
                    self.progress_percentage = int(50 + (completed_tasks / max(1, total_active_tasks)) * 40)
                    self.progress_text = f"Scanning parameters: {completed_tasks}/{total_active_tasks} complete..."

            # Inject payloads into HTML forms inputs (POST/GET forms)
            for form in discovered_forms:
                for inp in form['inputs']:
                    param = inp['name']
                    inp_type = inp['type']
                    
                    # Skip submit or non-injectable types
                    if inp_type in ['submit', 'button', 'file', 'image']:
                        continue
                        
                    if self.stop_event.is_set():
                        self.status = "stopped"
                        return
                        
                    self.logger.info(f"Scanning form parameter: {param} on {form['url']}")
                    
                    # 1. SQL Injection check
                    sqli_vuln = False
                    for payload in SQLI_PAYLOADS:
                        if self.stop_event.is_set():
                            self.status = "stopped"
                            return
                            
                        target_url, res = inject_payload_in_form(self.session, form, param, payload, cookies=self.cookies)
                        if res:
                            is_v, db_type, evidence = check_sqli(res.text)
                            if is_v:
                                vuln = {
                                    'vuln_type': 'SQL Injection',
                                    'severity': 'Critical',
                                    'url': form['url'],
                                    'method': form['method'].upper(),
                                    'parameter': param,
                                    'payload': payload,
                                    'evidence': f"Database: {db_type}. Error matched: {evidence}",
                                    'description': 'SQL Injection vulnerability detected in form input via database error message leakage.',
                                    'owasp_category': 'A03:2025-Injection'
                                }
                                self.vulnerabilities.append(vuln)
                                self.logger.error(f"VULNERABILITY DETECTED: SQL Injection on form parameter '{param}' at {form['url']}")
                                sqli_vuln = True
                                break
                                
                    # 2. XSS check
                    xss_vuln = False
                    for payload in XSS_PAYLOADS:
                        if self.stop_event.is_set():
                            self.status = "stopped"
                            return
                            
                        target_url, res = inject_payload_in_form(self.session, form, param, payload, cookies=self.cookies)
                        if res:
                            is_v, evidence = check_xss(payload, res.text)
                            if is_v:
                                vuln = {
                                    'vuln_type': 'Cross-Site Scripting (XSS)',
                                    'severity': 'High',
                                    'url': form['url'],
                                    'method': form['method'].upper(),
                                    'parameter': param,
                                    'payload': payload,
                                    'evidence': evidence,
                                    'description': 'Form-submitted Reflected Cross-Site Scripting (XSS) detected. Input parameter allows execution of arbitrary client-side script blocks.',
                                    'owasp_category': 'A03:2025-Injection'
                                }
                                self.vulnerabilities.append(vuln)
                                self.logger.error(f"VULNERABILITY DETECTED: XSS on form parameter '{param}' at {form['url']}")
                                xss_vuln = True
                                break
                                
                    completed_tasks += 1
                    self.progress_percentage = int(50 + (completed_tasks / max(1, total_active_tasks)) * 40)
                    self.progress_text = f"Scanning parameters: {completed_tasks}/{total_active_tasks} complete..."

            # Step 4: Compiling Results and Reports
            self.status = "compiling"
            self.progress_percentage = 95
            self.progress_text = "Compiling scan report..."
            self.logger.info("Compiling reports...")
            
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds()
            
            # Format report data
            report_data = {
                'target_url': self.target_url,
                'scan_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                'duration_seconds': round(duration, 2),
                'pages_crawled_count': len(self.crawled_urls),
                'crawled_urls': self.crawled_urls,
                'forms_discovered_count': len(discovered_forms),
                'vulnerabilities_count': len(self.vulnerabilities),
                'vulnerabilities': self.vulnerabilities
            }
            
            # Save report
            reporter = ReportGenerator()
            json_path = reporter.save_json_report(report_data)
            
            # Try to compile HTML report as well (requires the template to exist)
            html_path = None
            template_file = "templates/report_template.html"
            if os.path.exists(template_file):
                html_path = reporter.generate_html_report(report_data, template_file)
                
            self.logger.info(f"JSON scan report written to: {json_path}")
            if html_path:
                self.logger.info(f"HTML scan report written to: {html_path}")
                
            self.status = "completed"
            self.progress_percentage = 100
            self.progress_text = f"Scan complete. Found {len(self.vulnerabilities)} vulnerabilities."
            self.logger.info("Vulnerability scan operation complete.")
            
        except Exception as e:
            self.status = "stopped"
            self.progress_text = f"Scan failed: {str(e)}"
            self.logger.error(f"Scanner engine crashed: {str(e)}", exc_info=True)
            
    def get_status_summary(self):
        """
        Returns JSON-serializable status updates for dashboard polling.
        """
        return {
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'progress_text': self.progress_text,
            'pages_crawled_count': len(self.crawled_urls),
            'vulnerabilities_count': len(self.vulnerabilities),
            'vulnerabilities': self.vulnerabilities,
            'crawled_urls': self.crawled_urls
        }
