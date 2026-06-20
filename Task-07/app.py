import os
import json
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory, abort
from scanner.engine import VulnerabilityScanner
from scanner.utils import setup_logger, get_logs, clear_logs

app = Flask(__name__)
logger = setup_logger()

# Global variables to track the active scan
active_scanner = None
scan_thread = None
scan_lock = threading.Lock()

# Ensure reports directory exists
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

def get_historical_reports():
    """
    Scans the reports/ directory and returns metadata of all completed JSON reports.
    """
    reports = []
    if not os.path.exists(REPORTS_DIR):
        return reports
        
    for filename in os.listdir(REPORTS_DIR):
        if filename.startswith('scan_report_') and filename.endswith('.json'):
            file_path = os.path.join(REPORTS_DIR, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Clean up filename prefix to get the ID/timestamp
                report_id = filename.replace('scan_report_', '').replace('.json', '')
                
                reports.append({
                    'id': report_id,
                    'target_url': data.get('target_url'),
                    'scan_time': data.get('scan_time'),
                    'vulnerabilities_count': data.get('vulnerabilities_count', 0),
                    'pages_crawled_count': data.get('pages_crawled_count', 0),
                    'duration': data.get('duration_seconds', 0)
                })
            except Exception as e:
                logger.error(f"Failed to read report file {filename}: {str(e)}")
                
    # Sort reports by scan time descending
    reports.sort(key=lambda x: x['scan_time'], reverse=True)
    return reports

@app.route('/')
def dashboard():
    """
    Renders the web control panel interface.
    """
    reports = get_historical_reports()
    return render_template('index.html', reports=reports)

@app.route('/scan/start', methods=['POST'])
def start_scan():
    """
    API endpoint to kick off a security scan in the background.
    """
    global active_scanner, scan_thread
    
    data = request.json or {}
    target_url = data.get('target_url')
    max_depth = int(data.get('max_depth', 3))
    custom_cookies = data.get('custom_cookies', '')
    
    if not target_url:
        return jsonify({'error': 'Target URL is required'}), 400
        
    if not (target_url.startswith('http://') or target_url.startswith('https://')):
        return jsonify({'error': 'Invalid URL. Target must start with http:// or https://'}), 400
        
    with scan_lock:
        if active_scanner and active_scanner.status in ['crawling', 'scanning', 'compiling']:
            return jsonify({'error': 'A scan is already actively running. Please stop or wait for it to complete.'}), 400
            
        # Reset logs buffer for new scan
        clear_logs()
        
        # Initialize new scanner
        active_scanner = VulnerabilityScanner(
            target_url=target_url,
            max_depth=max_depth,
            custom_cookies=custom_cookies,
            logger=logger
        )
        
        # Start thread
        scan_thread = threading.Thread(target=active_scanner.run)
        scan_thread.daemon = True
        scan_thread.start()
        
    return jsonify({
        'message': 'Scan initiated successfully',
        'target_url': target_url
    })

@app.route('/scan/status', methods=['GET'])
def scan_status():
    """
    Polled endpoint that returns scanning state, progress, findings, and logs buffer.
    """
    global active_scanner
    
    if not active_scanner:
        return jsonify({
            'status': 'idle',
            'progress_percentage': 0,
            'progress_text': 'No active scan',
            'vulnerabilities_count': 0,
            'vulnerabilities': [],
            'crawled_urls': [],
            'logs': []
        })
        
    status_summary = active_scanner.get_status_summary()
    status_summary['logs'] = get_logs()
    
    return jsonify(status_summary)

@app.route('/scan/stop', methods=['POST'])
def stop_scan():
    """
    Cancels the currently running scan.
    """
    global active_scanner
    
    if not active_scanner:
        return jsonify({'error': 'No active scan running'}), 400
        
    active_scanner.stop()
    return jsonify({'message': 'Scan stop signal sent.'})

@app.route('/reports/view/<report_id>')
def view_report(report_id):
    """
    Loads and renders a saved HTML report, or falls back to compiling from JSON.
    """
    json_path = os.path.join(REPORTS_DIR, f"scan_report_{report_id}.json")
    html_path = os.path.join(REPORTS_DIR, f"scan_report_{report_id}.html")
    
    # If the static HTML report file already exists, send it
    if os.path.exists(html_path):
        return send_from_directory(REPORTS_DIR, f"scan_report_{report_id}.html")
        
    # If HTML is missing but JSON exists, we can dynamically render the report template
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            return render_template('report_template.html', results=report_data, generation_time=report_data.get('scan_time'))
        except Exception as e:
            logger.error(f"Error rendering report dynamic fallback: {str(e)}")
            abort(500, description="Error reading JSON report data.")
            
    abort(404, description="Report not found.")

@app.route('/reports/download/<format_type>/<report_id>')
def download_report(format_type, report_id):
    """
    Download endpoint for offline reports (format_type: 'json' or 'html').
    """
    filename = f"scan_report_{report_id}.{format_type}"
    file_path = os.path.join(REPORTS_DIR, filename)
    
    if not os.path.exists(file_path):
        # If HTML file is missing but JSON is present, we try to compile it on the fly
        if format_type == 'html':
            json_path = os.path.join(REPORTS_DIR, f"scan_report_{report_id}.json")
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        report_data = json.load(f)
                    template_file = os.path.join(app.root_path, 'templates', 'report_template.html')
                    
                    from scanner.reporter import ReportGenerator
                    reporter = ReportGenerator()
                    reporter.generate_html_report(report_data, template_file, filename)
                except Exception as e:
                    logger.error(f"Failed to generate HTML report on the fly: {str(e)}")
                    abort(500)
            else:
                abort(404)
        else:
            abort(404)
            
    return send_from_directory(REPORTS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
