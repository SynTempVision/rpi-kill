# rpi-kill - using a Managed Switch
Testing the amount of unsafe shutdowns and recording its affects on the camera -
- Create program to disable PoE on the Ethernet port supplying the device.
- Connect a SV04 camera system to a relay channel and Turn the Relay ON/OFF to kill the power on the camera system on a timed basis.
- Monitor the health and status of the normal operations and the system.
- Log and document:
    - SD card corruption frequency
    - Filesystem integrity
    - Service recovery behavior
    - Boot reliability
    - Data loss patterns
    - Hardware side effects over time

### Wiring 
```
[ AC / DC Power ]
        │
[ ING10-082GSMP PoE Switch ]
        │   (PoE ON / OFF)
        │
[ Anivision PoE Splitter ]
        ├────────── Ethernet (Data)
        │               │
        │          [ Pi Ethernet ]
        │
        └────────── DC Output (5V)
                        │
                 [ Raspberry Pi HAT ]

```
1. Enable PoE on target port
2. Allow system to boot and stabilize
3. Disable PoE (hard power loss)
4. Wait configurable delay (e.g. 5–60 seconds)
5. Re-enable PoE
6. Observe boot, services, filesystem
7. Log results
8. Repeat for N cycles

#### Test Result Interpretation

###### PASS
- System boots
- Root filesystem mounted RW
- RTSP services running
- Database running
- No critical storage failures

###### DEGRADED
- USB or storage warnings
- systemd in degraded state
- Services recover automatically

###### FAIL
- Root filesystem mounted RO
- Storage device missing or unstable
- RTSP services fail to start
- Database fails to start
- Manual intervention required
- Testing stops on FAIL.
