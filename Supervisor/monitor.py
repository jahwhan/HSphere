import os
import time
from datetime import datetime

LOGS_DIR = "Logs"
AGENTS_DIR = "Agents"
REPORT_FILE = "status_report.md"

def get_file_info(path):
    try:
        size = os.path.getsize(path)
        last_modified = time.ctime(os.path.getmtime(path))
        return f"{path} | {size / 1024:.1f} KB | Last Modified: {last_modified}"
    except Exception as e:
        return f"{path} | ERROR: {e}"

def scan_logs():
    logs = [f for f in os.listdir(LOGS_DIR) if f.endswith(".log") or f.endswith(".txt")]
    report = "\n## Logs Overview\n"
    for log in logs:
        path = os.path.join(LOGS_DIR, log)
        report += f"- {get_file_info(path)}\n"
    return report

def scan_agents():
    agents = [f for f in os.listdir(AGENTS_DIR) if f.endswith(".py")]
    report = "\n## Agent Modules\n"
    for agent in agents:
        path = os.path.join(AGENTS_DIR, agent)
        report += f"- {get_file_info(path)}\n"
    return report

def scan_other_files():
    files = [
        "Agents/main_booking.py",
        "Agents/main_inventory.py",
        "Agents/main_promptforge.py",
        "Agents/main_selfimprove.py",
        "Supervisor/supervisor.py",
        "Logs/improvement_logger.py",
        "Data/clients.py",
        "Data/stylists.py"
    ]
    report = "\n## Core System Files\n"
    for f in files:
        if os.path.exists(f):
            report += f"- {get_file_info(f)}\n"
        else:
            report += f"- {f} | MISSING\n"
    return report

def generate_report():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"# HSphere Status Report\n\nGenerated: {now}\n"
    content += scan_logs()
    content += scan_agents()
    content += scan_other_files()

    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            safe_content = content.encode("ascii", "ignore").decode()
            f.write(safe_content)
        print(f"[Monitor] Report generated at {REPORT_FILE}")
    except Exception as e:
        print(f"[Monitor] Failed to write report: {e}")

if __name__ == "__main__":
    generate_report()
