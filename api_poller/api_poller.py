import os
import time

from fetch_worker import run_fetch_worker

HOUR_TO_MS = 1*60*60_000

def main():
    poll_interval_ms = int(os.getenv("POLL_INTERVAL_MS") or 1*HOUR_TO_MS)
    poll_interval = poll_interval_ms / 1000
    while True:
        print("[!] Worker process started")
        run_fetch_worker()
        print("[!] Worker process completed")
        print("[!] waiting for the next run...")
        time.sleep(poll_interval)

if __name__ == "__main__":
    main()
