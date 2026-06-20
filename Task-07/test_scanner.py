import unittest
from unittest.mock import MagicMock, patch
import json
import os
import shutil

from scanner.utils import is_internal_url, clean_url
from scanner.crawler import WebCrawler
from scanner.detector import check_sqli, check_xss, check_csrf, check_security_headers
from scanner.reporter import ReportGenerator

class TestVulnerabilityScanner(unittest.TestCase):
    
    def setUp(self):
        # Setup temporary directories if needed
        self.test_reports_dir = "test_reports"
        if not os.path.exists(self.test_reports_dir):
            os.makedirs(self.test_reports_dir)

    def tearDown(self):
        # Cleanup temporary files
        if os.path.exists(self.test_reports_dir):
            shutil.rmtree(self.test_reports_dir)

    def test_url_helpers(self):
        # Test internal URL check
        self.assertTrue(is_internal_url("http://example.com/page", "http://example.com"))
        self.assertTrue(is_internal_url("/page", "http://example.com"))
        self.assertFalse(is_internal_url("http://different.com/page", "http://example.com"))
        
        # Test clean URL
        self.assertEqual(clean_url("http://example.com/page#section"), "http://example.com/page")
        self.assertEqual(clean_url("http://example.com/page/"), "http://example.com/page")

    def test_crawler_form_extraction(self):
        crawler = WebCrawler("http://example.com")
        
        html_with_form = """
        <html>
            <body>
                <form action="/login" method="post">
                    <input type="text" name="username" value="admin">
                    <input type="password" name="password">
                    <input type="hidden" name="csrf_token" value="abc123xyz">
                </form>
            </body>
        </html>
        """
        
        forms = crawler.extract_forms("http://example.com/index.html", html_with_form)
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0]['url'], "http://example.com/login")
        self.assertEqual(forms[0]['method'], "post")
        self.assertEqual(len(forms[0]['inputs']), 3)
        
        # Verify inputs details
        names = [inp['name'] for inp in forms[0]['inputs']]
        self.assertIn('username', names)
        self.assertIn('password', names)
        self.assertIn('csrf_token', names)

    def test_crawler_link_and_param_extraction(self):
        crawler = WebCrawler("http://example.com")
        
        html_with_links = """
        <html>
            <body>
                <a href="/about">About Us</a>
                <a href="http://example.com/search?q=security&page=2">Search</a>
                <a href="http://external.com/docs">External</a>
            </body>
        </html>
        """
        
        links = crawler.extract_links_and_params("http://example.com/home", html_with_links)
        
        # Should only return internal links (about, search)
        self.assertEqual(len(links), 2)
        self.assertIn("http://example.com/about", links)
        self.assertIn("http://example.com/search?q=security&page=2", links)
        
        # Check query parameters extraction
        self.assertIn("http://example.com/search", crawler.discovered_parameters)
        params = crawler.discovered_parameters["http://example.com/search"]
        self.assertIn("q", params)
        self.assertIn("page", params)

    def test_detector_sqli(self):
        # Vulnerable cases
        vuln, db_type, evidence = check_sqli("You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version")
        self.assertTrue(vuln)
        self.assertEqual(db_type, "MySQL")
        
        vuln, db_type, evidence = check_sqli("pg_query(): Query failed: ERROR: invalid input syntax for integer")
        self.assertTrue(vuln)
        self.assertEqual(db_type, "PostgreSQL")
        
        # Safe case
        vuln, db_type, evidence = check_sqli("Welcome to our homepage, user!")
        self.assertFalse(vuln)

    def test_detector_xss(self):
        payload = "<script>alert(1)</script>"
        
        # Vulnerable case
        vuln, evidence = check_xss(payload, f"<html><body>{payload}</body></html>")
        self.assertTrue(vuln)
        
        # Safe case (escaped)
        escaped_response = "<html><body>&lt;script&gt;alert(1)&lt;/script&gt;</body></html>"
        vuln, evidence = check_xss(payload, escaped_response)
        self.assertFalse(vuln)

    def test_detector_csrf(self):
        # Vulnerable form (POST without token)
        form_no_csrf = {
            'url': 'http://example.com/post',
            'method': 'post',
            'inputs': [
                {'name': 'comment', 'type': 'text', 'value': ''}
            ]
        }
        vuln, evidence = check_csrf(form_no_csrf)
        self.assertTrue(vuln)
        
        # Safe form (POST with token)
        form_with_csrf = {
            'url': 'http://example.com/post',
            'method': 'post',
            'inputs': [
                {'name': 'comment', 'type': 'text', 'value': ''},
                {'name': 'csrf_token', 'type': 'hidden', 'value': 'token123'}
            ]
        }
        vuln, evidence = check_csrf(form_with_csrf)
        self.assertFalse(vuln)
        
        # GET forms shouldn't flag CSRF
        form_get = {
            'url': 'http://example.com/search',
            'method': 'get',
            'inputs': [
                {'name': 'q', 'type': 'text', 'value': ''}
            ]
        }
        vuln, evidence = check_csrf(form_get)
        self.assertFalse(vuln)

    def test_detector_security_headers(self):
        headers_vuln = {
            'Server': 'Apache/2.4.41 (Ubuntu)',
            'X-Powered-By': 'PHP/7.4.3'
        }
        findings = check_security_headers(headers_vuln)
        
        # Should flag missing headers (X-Frame-Options, X-Content-Type-Options, CSP, HSTS) 
        # and version info leaks
        vuln_types = [f['vuln_type'] for f in findings]
        self.assertIn('Missing X-Frame-Options Header', vuln_types)
        self.assertIn('Missing X-Content-Type-Options Header', vuln_types)
        self.assertIn('Server Information Leakage', vuln_types)
        self.assertIn('Technology Stack Disclosure', vuln_types)

    def test_reporter_json(self):
        reporter = ReportGenerator(output_dir=self.test_reports_dir)
        test_data = {
            'target_url': 'http://test.com',
            'vulnerabilities_count': 1,
            'vulnerabilities': [
                {'vuln_type': 'SQLi', 'severity': 'Critical'}
            ]
        }
        
        report_path = reporter.save_json_report(test_data, "test_report.json")
        self.assertTrue(os.path.exists(report_path))
        
        # Verify JSON content
        with open(report_path, 'r') as f:
            read_data = json.load(f)
        self.assertEqual(read_data['target_url'], 'http://test.com')

if __name__ == '__main__':
    unittest.main()
