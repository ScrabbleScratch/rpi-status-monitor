# rpi-status-monitor
A dockerized python script that's monitoring system parameters such as:

- CPU _usage percent_
- CPU _temperature_
- _RAM used_ by the system

It displays each of them in an _LCD_ controlled via _I2C_ communication.

The python script named "status-monitor.py" contains the set of instructions needed to monitor the system statistics.
While the "I2C_LCD_driver_UBUNTU.py" script is the module needed to take control of the I2C LCD attached to the Raspberry.

# IMPORTANT
- In order to get the script o work, `i2c-tools` has to be installed before using:
```
sudo apt install i2c-tools
```
- Due to some issues when installing the `RPi.GPIO` module in the container, the _Dockerfile_ has been modified to install it with the line:
```
RUN CFLAGS="-fcommon" pip install RPi.GPIO
```

# _ADDED:_
 - _It now has support to take control over a 4 channel relay module._
 - _A control for a fan was added, including it's temperature control._

# I2C_LCD_driver_UBUNTU.py

In the LCD driver script it's needed to specify the memory address that the I2C module is pointed to. You can do it by running an I2C scan.
```
ADDRESS = 0x27    #change the 0x27 with the address of your module
```

# Dockerfile

The Dockerfile contains the configuration for a minimal dockerization of the python script. Including the local LCD driver that cannot be installed within _pip_.

# Specs of the system where the project is tested:

- **Board:** Raspberry Pi 4B
- **OS:** Ubuntu Server 20.04.3 arm64
- **Python:** Latest image of Python for docker ARM64
