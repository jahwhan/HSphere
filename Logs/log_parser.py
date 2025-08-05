import os
import time

LOGS_DIR = "Logs"
KEYWORDS = ["Improvement", "Booking", "Prompt", "Client", "SelfImprove", "Inventory"]

def parse_log_file(filepath):
    summary = {
        "lines": 0,
        "matches": {},
        "last_modified": time.ctime(os.path.getmtime(filepath))
    }

    for key in KEYWORDS:
        summary["matches"][key] = 0

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            summary["lines"] += 1
            for key in KEYWORDS:
                if key.lower() in line.lower():
                    summary["matches"][key] += 1

    return summary

def summarize_logs():
    print("\n🧾 Log Summary Report\n")
    files = [f for f in os.listdir(LOGS_DIR) if f.endswith(".log") or f.endswith(".txt")]
    
    if not files:
        print("No log files found.")
        return

    for file in files:
        path = os.path.join(LOGS_DIR, file)
        data = parse_log_file(path)
        print(f"📄 {file}")
        print(f"   🕒 Last Modified: {data['last_modified']}")
        print(f"   🧾 Total Lines: {data['lines']}")
        for key, count in data["matches"].items():
            if count > 0:
                print(f"   🔍 {key}: {count}")
        print("")

if __name__ == "__main__":
    summarize_logs()

