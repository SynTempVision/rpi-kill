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
