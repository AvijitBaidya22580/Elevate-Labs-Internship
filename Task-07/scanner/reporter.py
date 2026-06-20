import json
import os
from datetime import datetime
from jinja2 import Template

class ReportGenerator:
    """
    Handles generation of JSON and HTML vulnerability scan reports.
    """
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def save_json_report(self, scan_results, filename=None):
        """
        Saves the scan results in JSON format.
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scan_report_{timestamp}.json"
            
        file_path = os.path.join(self.output_dir, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(scan_results, f, indent=4)
            return file_path
        except Exception as e:
            print(f"Error saving JSON report: {str(e)}")
            return None

    def generate_html_report(self, scan_results, template_path, output_filename=None):
        """
        Generates a standalone HTML report using a template.
        """
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"scan_report_{timestamp}.html"
            
        output_path = os.path.join(self.output_dir, output_filename)
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
                
            # Create a Jinja2 template and render it
            template = Template(template_content)
            rendered_html = template.render(
                results=scan_results,
                generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
                
            return output_path
        except Exception as e:
            print(f"Error generating HTML report: {str(e)}")
            return None
