import time
import boto3

from config import AWS_REGION, LOG_GROUPS
from notifier import send_alert


class CloudWatchListener:

    def __init__(self):
        self.client = boto3.client(
            "logs",
            region_name=AWS_REGION
        )
        self.start_times = {}

    def initialize(self):
        current_time = int(time.time() * 1000)
        for log_group in LOG_GROUPS:
            self.start_times[log_group] = current_time
            print(f"👂 Listening to AWS CloudWatch: {log_group}")

    def get_events(self, log_group):
        start_time = self.start_times[log_group]
        try:
            response = self.client.filter_log_events(
                logGroupName=log_group,
                startTime=start_time,
                interleaved=True,
            )
            events = response.get("events", [])
            if events:
                self.start_times[log_group] = max(event["timestamp"] + 1 for event in events)
            return events
        except Exception as e:
            print(f"❌ CloudWatch error for {log_group}: {e}")
            return []

    @staticmethod
    def is_error(message):
        error_keywords = [
            "ERROR", "Error", "error", "FATAL", "Fatal", "fatal",
            "EXCEPTION", "Exception", "exception", "Traceback",
            "Task timed out", "RuntimeError", "Unhandled", "failed", "FAILED"
        ]
        return any(keyword in message for keyword in error_keywords)

    def process_event(self, log_group, event):
        message = event.get("message", "").strip()
        log_stream = event.get("logStreamName", "unknown")

        if not message:
            return

        print(f"\n☁️ [{log_group}]")
        print(message)

        if self.is_error(message):
            print("\n🚨 AWS LAMBDA ERROR DETECTED!")
            
            subject = f"🚨 AWS Lambda Error - {log_group}"
            body = f"""AWS CloudWatch Incident Detected

Log Group:
{log_group}

Log Stream:
{log_stream}

Error:

{message}

--------------------------------
Detected by AWS CloudWatch Listener"""

            send_alert(subject, body)

    def run(self):
        self.initialize()
        print("\n🚀 AWS CloudWatch listener started...")
        print("Waiting for Lambda errors...\n")
        
        while True:
            for log_group in LOG_GROUPS:
                events = self.get_events(log_group)
                for event in events:
                    self.process_event(log_group, event)
            time.sleep(5)


if __name__ == "__main__":
    listener = CloudWatchListener()
    try:
        listener.run()
    except KeyboardInterrupt:
        print("\n🛑 AWS CloudWatch listener stopped.")
