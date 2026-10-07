import subprocess
import os
from dotenv import load_dotenv
from notifier import send_alert

load_dotenv()

def start_postgres_listener():
    print("🚀 PostgreSQL log listener started...")
    print("Waiting for PostgreSQL errors...\n")

    process = subprocess.Popen(
        ["docker", "logs", "-f", "postgres-alert-db"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    try:
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue

            print(line)

            if "ERROR" in line or "FATAL" in line or "authentication failed" in line:
                print("\n🚨 PostgreSQL ERROR DETECTED!")
                
                subject = "🚨 PostgreSQL Error Alert"
                body = f"""PostgreSQL error detected!

Log:

{line}

--------------------------------
Detected by PostgreSQL Log Listener"""
                
                send_alert(subject, body)
                
    except KeyboardInterrupt:
        print("\n🛑 PostgreSQL listener stopped.")


if __name__ == "__main__":
    start_postgres_listener()
