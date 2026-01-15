# rpi-kill
Testing the amount of unsafe shutdowns and recording its affects on the camera -
- Create program to turn Relay ON/OFF 
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
+12V  ------------------>  [ RELAY COM ]
                              |
                              |  (NC contact)
                              v
                          [ RELAY NC ]  ------------------>  [ Pi POWER HAT  VIN + ]

GND   ----------------------------------------------------->  [ Pi POWER HAT  GND ]
```
```
Relay OFF  (not energized):
COM -- NC  --> Pi has power

Relay ON   (energized):
COM --X-- NC  --> Pi loses power
```
1. put kill_power_test.sh in /usr/local/bin/camera
2. sudo chmod +x /usr/local/bin/kill_power_test.sh
4. put in system_init.sh
5. on laptop start the relay_controller
6. monitor pi health

#### Test Result Interpretation
####### PASS
- System boots
- Root filesystem mounted RW
- RTSP services running
- Database running
- No critical storage failures
- DEGRADED
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
