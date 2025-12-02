import json
import os

report_path = os.path.expanduser("~/Desktop/hva_debug_reports/report_20251202_205010.json")

try:
    with open(report_path, 'r') as f:
        data = json.load(f)
        
    print(f"Analyzing report: {report_path}")
    print("-" * 50)
    
    print("Backend Logs Dump (Last 50):")
    print("-" * 50)
    logs = data.get('logs', [])
    print(f"Type of logs: {type(logs)}")
    if isinstance(logs, list):
        print(f"Number of logs: {len(logs)}")
        for log in logs[-50:]:
            print(str(log).strip())
    else:
        print(f"Logs content: {logs}")
            
except Exception as e:
    print(f"Error reading report: {e}")
