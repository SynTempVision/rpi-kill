#!/bin/bash

LOG="/var/log/kill_power_test.log"
RESULT="PASS"
BOOT_TIME="$(date --iso-8601=seconds)"

echo "===================================" >> "$LOG"
echo "BOOT @ $BOOT_TIME"                  >> "$LOG"

# 1. Root filesystem must be RW
ROOT_LINE=$(mount | grep " / ")
echo "ROOT: $ROOT_LINE" >> "$LOG"

if echo "$ROOT_LINE" | grep -q " ro,"; then
    echo "ERROR: root filesystem is read-only" >> "$LOG"
    RESULT="FAIL"
fi

# 2. NVMe must exist
if ! lsblk | grep -q nvme0n1; then
    echo "ERROR: NVMe device missing" >> "$LOG"
    RESULT="FAIL"
else
    echo "NVME: present" >> "$LOG"
fi

# 3. Storage / USB warnings (non-fatal unless persistent)
STORAGE_ERR=$(dmesg | grep -i "nvme\|usb\|uas\|reset" | tail -n 5)
if [[ -n "$STORAGE_ERR" ]]; then
    echo "STORAGE WARNINGS:" >> "$LOG"
    echo "$STORAGE_ERR" >> "$LOG"
    [[ "$RESULT" == "PASS" ]] && RESULT="DEGRADED"
fi

# 4. RTSP processes must be running
pgrep -f rtsp-color-server.sh >/dev/null || {
    echo "ERROR: rtsp-color-server not running" >> "$LOG"
    RESULT="FAIL"
}

pgrep -f rtsp-seek-server.sh >/dev/null || {
    echo "ERROR: rtsp-seek-server not running" >> "$LOG"
    RESULT="FAIL"
}

# 5. Database must be active
if ! systemctl is-active mariadb >/dev/null; then
    echo "ERROR: database not active" >> "$LOG"
    RESULT="FAIL"
else
    echo "DB: active" >> "$LOG"
fi

# 6. systemd overall state
SYSTEMD_STATE=$(systemctl is-system-running)
echo "SYSTEMD: $SYSTEMD_STATE" >> "$LOG"

if [[ "$SYSTEMD_STATE" == "maintenance" ]]; then
    RESULT="FAIL"
elif [[ "$SYSTEMD_STATE" == "degraded" && "$RESULT" == "PASS" ]]; then
    RESULT="DEGRADED"
fi

# Final verdict
echo "TEST RESULT: $RESULT" >> "$LOG"
echo "===================================" >> "$LOG"

exit 0
