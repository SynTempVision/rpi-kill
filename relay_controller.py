import time
import requests
import csv
from datetime import datetime

RELAY_IP = "172.17.17.105"
CHANNEL  = 3
LOG_FILE = "relay_power_cycles.csv"

def log_event(cycle, action):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            cycle,
            action,
            CHANNEL
        ])

def restore_power(cycle):
    requests.get(f"http://{RELAY_IP}/relay_off.cgi?relay={CHANNEL}")
    log_event(cycle, "POWER_ON")
    print("POWER ON")

def cut_power(cycle):
    requests.get(f"http://{RELAY_IP}/relay_on.cgi?relay={CHANNEL}")
    log_event(cycle, "POWER_CUT")
    print("POWER CUT")

cycle = 0

while True:
    cycle += 1
    print(f"\n--- CYCLE {cycle} ---")

    restore_power(cycle)
    time.sleep(180)   # 3 min uptime

    cut_power(cycle)
    time.sleep(10)    # outage
