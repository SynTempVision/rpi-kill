#!/bin/bash
set -u

LOG_DIR="/var/log/rpi-kill"
LOG_FILE="$LOG_DIR/boot.csv"

mkdir -p "$LOG_DIR"

# --- Immutable identifiers ---
EPOCH=$(date +%s)
BOOT_ID=$(cat /proc/sys/kernel/random/boot_id)
UPTIME=$(cut -d. -f1 /proc/uptime)

# --- Defaults ---
RESULT="PASS"
FS_INTEGRITY=1
ROOT_RW=1
STORAGE_PRESENT=1
SERVICES_OK=1
CAMERA_OK=1
UNDERVOLTAGE=0
NOTES=""

# --- Root filesystem state ---
if mount | grep " / " | grep -q " ro,"; then
    ROOT_RW=0
    RESULT="FAIL"
    NOTES+="root_ro;"
fi

# --- Previous boot filesystem errors ---
FS_ERR=$(journalctl -b -1 -k 2>/dev/null | grep -Ei "EXT4|fsck|orphan|I/O error" | head -n 1)
if [[ -n "$FS_ERR" ]]; then
    FS_INTEGRITY=0
    RESULT="FAIL"
    NOTES+="fs_err;"
fi

# --- Storage presence (NVMe or SD acceptable) ---
if ! lsblk | grep -Eq "nvme0n1|mmcblk0"; then
    STORAGE_PRESENT=0
    RESULT="FAIL"
    NOTES+="storage_missing;"
fi

# --- Undervoltage / throttling ---
if command -v vcgencmd >/dev/null; then
    THROTTLED=$(vcgencmd get_throttled | cut -d= -f2)
    if (( THROTTLED & 0x1 )); then
        UNDERVOLTAGE=1
        [[ "$RESULT" == "PASS" ]] && RESULT="DEGRADED"
        NOTES+="undervoltage;"
    fi
fi

# --- Required services ---
REQUIRED_SERVICES=(
  rtsp-color-server.sh
  rtsp-seek-server.sh
  mariadb
)

for SVC in "${REQUIRED_SERVICES[@]}"; do
    if ! pgrep -f "$SVC" >/dev/null && ! systemctl is-active "$SVC" >/dev/null 2>&1; then
        SERVICES_OK=0
        RESULT="FAIL"
        NOTES+="svc_${SVC}_down;"
    fi
done

# --- Camera enumeration ---
if ! lsusb | grep -qi "camera\|seek\|video"; then
    CAMERA_OK=0
    [[ "$RESULT" == "PASS" ]] && RESULT="DEGRADED"
    NOTES+="camera_enum;"
fi

# --- systemd global state ---
SYSTEMD_STATE=$(systemctl is-system-running 2>/dev/null || echo "unknown")
if [[ "$SYSTEMD_STATE" == "maintenance" ]]; then
    RESULT="FAIL"
elif [[ "$SYSTEMD_STATE" == "degraded" && "$RESULT" == "PASS" ]]; then
    RESULT="DEGRADED"
fi

# --- Write header if first run ---
if [[ ! -f "$LOG_FILE" ]]; then
    echo "epoch,boot_id,uptime_sec,result,fs_integrity,root_rw,storage_present,services_ok,camera_ok,undervoltage,systemd_state,notes" >> "$LOG_FILE"
fi

# --- Append authoritative row ---
echo "$EPOCH,$BOOT_ID,$UPTIME,$RESULT,$FS_INTEGRITY,$ROOT_RW,$STORAGE_PRESENT,$SERVICES_OK,$CAMERA_OK,$UNDERVOLTAGE,$SYSTEMD_STATE,$NOTES" >> "$LOG_FILE"
sync

exit 0
