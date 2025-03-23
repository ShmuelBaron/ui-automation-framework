"""
HTML reporter for UI automation framework.
"""
import os
import time
from datetime import datetime
import logging
import jinja2
import shutil

class HtmlReporter:
    """Class for generating HTML test reports."""
    
    def __init__(self, report_dir=None):
        """
        Initialize the HTML reporter.
        
        Args:
            report_dir: Directory for reports (default: project_root/reports)
        """
        self.logger = logging.getLogger(__name__)
        
        if report_dir is None:
            # Default report directory is project_root/reports
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.report_dir = os.path.join(project_root, 'reports')
        else:
            self.report_dir = report_dir
        
        # Create report directory if it doesn't exist
        os.makedirs(self.report_dir, exist_ok=True)
        
        # Initialize Jinja2 environment
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        if not os.path.exists(template_dir):
            os.makedirs(template_dir, exist_ok=True)
            self._create_default_template(template_dir)
        
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
    
    def generate_report(self, test_results, report_name=None):
        """
        Generate HTML report from test results.
        
        Args:
            test_results: Dictionary containing test results
            report_name: Name of the report file (default: timestamp)
            
        Returns:
            str: Path to the generated report
        """
        if report_name is None:
            # Generate name with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_name = f"test_report_{timestamp}.html"
        
        # Ensure name has .html extension
        if not report_name.lower().endswith('.html'):
            report_name = f"{report_name}.html"
        
        # Create full path
        report_path = os.path.join(self.report_dir, report_name)
        
        try:
            # Load template
            template = self.jinja_env.get_template('report_template.html')
            
            # Add timestamp to results
            test_results['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            test_results['duration'] = self._format_duration(test_results.get('duration', 0))
            
            # Render template with test results
            html_content = template.render(**test_results)
            
            # Write to file
            with open(report_path, 'w', encoding='utf-8') as file:
                file.write(html_content)
            
            self.logger.info(f"HTML report generated: {report_path}")
            return report_path
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {str(e)}")
            raise
    
    def _format_duration(self, seconds):
        """
        Format duration in seconds to a readable string.
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            str: Formatted duration
        """
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{int(hours)}h {int(minutes)}m {seconds:.2f}s"
        elif minutes > 0:
            return f"{int(minutes)}m {seconds:.2f}s"
        else:
            return f"{seconds:.2f}s"
    
    def _create_default_template(self, template_dir):
        """
        Create default HTML report template.
        
        Args:
            template_dir: Directory to create template in
        """
        template_path = os.path.join(template_dir, 'report_template.html')
        
        template_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title|default('UI Automation Test Report') }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .summary {
            display: flex;
            justify-content: space-between;
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .summary-item {
            text-align: center;
        }
        .summary-label {
            font-weight: bold;
            margin-bottom: 5px;
        }
        .summary-value {
            font-size: 24px;
        }
        .passed {
            color: #28a745;
        }
        .failed {
            color: #dc3545;
        }
        .skipped {
            color: #ffc107;
        }
        .error {
            color: #6c757d;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        .test-details {
            margin-top: 10px;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        .test-log {
            font-family: monospace;
            white-space: pre-wrap;
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            max-height: 200px;
            overflow-y: auto;
        }
        .screenshot {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            margin-top: 10px;
        }
        .footer {
            margin-top: 20px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title|default('UI Automation Test Report') }}</h1>
        <p>Generated on: {{ timestamp }}</p>
        
        <div class="summary">
            <div class="summary-item">
                <div class="summary-label">Total Tests</div>
                <div class="summary-value">{{ total_tests }}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Passed</div>
                <div class="summary-value passed">{{ passed_tests }}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Failed</div>
                <div class="summary-value failed">{{ failed_tests }}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Skipped</div>
                <div class="summary-value skipped">{{ skipped_tests }}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Duration</div>
                <div class="summary-value">{{ duration }}</div>
            </div>
        </div>
        
        <h2>Test Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Duration</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                {% for test in tests %}
                <tr>
                    <td>{{ test.name }}</td>
                    <td class="{{ test.status|lower }}">{{ test.status }}</td>
                    <td>{{ test.duration }}</td>
                    <td>
                        {% if test.details %}
                        <div class="test-details">
                            {{ test.details }}
                            
                            {% if test.log %}
                            <h4>Log</h4>
                            <div class="test-log">{{ test.log }}</div>
                            {% endif %}
                            
                            {% if test.screenshot %}
                            <h4>Screenshot</h4>
                            <img src="{{ test.screenshot }}" alt="Test Screenshot" class="screenshot">
                            {% endif %}
                        </div>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <div class="footer">
            <p>Generated by UI Automation Framework</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(template_path, 'w', encoding='utf-8') as file:
            file.write(template_content)
        
        self.logger.info(f"Created default HTML report template: {template_path}")
