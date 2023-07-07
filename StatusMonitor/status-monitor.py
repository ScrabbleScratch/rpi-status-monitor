import I2C_LCD_driver_UBUNTU as driver     #modified script to work on Ubuntu
import RPi.GPIO as gpio             #to take control of the gpio pins
import socket                       #to get ip address
import psutil                       #to read system stats
import argparse                     #to read arguments parsed from console
from time import sleep              #to ake pauses between reads

parser = argparse.ArgumentParser(description="Get system info displayed on an LCD screen")
parser.add_argument("--cooler-on", dest="cooler_on", default=50, help="Temperature at which the cooler turns on", type=int)
parser.add_argument("--cooler-off", dest="cooler_off", default=40, help="Temperature at which the cooler turns off", type=int)
parser.add_argument("--fan-on", dest="fan_on", default=55, help="Temperature at which the fan turns on", type=int)
parser.add_argument("--fan-off", dest="fan_off", default=50, help="Temperature at which the fan turns off", type=int)
parser.add_argument("-d", "--delay", dest="delay", default=5, help="Delay between each read cycle", type=float)
args = parser.parse_args()

lcd = driver.lcd()

gpio.setmode(gpio.BCM)              #set gpio label to BCM

#define names for gpio pins
cooler_pin = 17
relay1_pin = 1
relay2_pin = 7
relay3_pin = 8
fan_pin = 25    #relay4 pin

#set gpio pins as outputs
gpio.setup(cooler_pin, gpio.OUT)
gpio.setup(relay1_pin, gpio.OUT)
gpio.setup(relay2_pin, gpio.OUT)
gpio.setup(relay3_pin, gpio.OUT)
gpio.setup(fan_pin, gpio.OUT)

#define temperatures to turn cooler and fan on/off
cooler_on = args.cooler_on
cooler_off = args.cooler_off
fan_on = args.fan_on
fan_off = args.fan_off

#seconds between cycles
cycle = args.delay

#get the hostname
hostname = socket.gethostname()

print(f"""
COOLER TEMPS: {cooler_off} - {cooler_on}
FAN TEMPS: {fan_off} - {fan_on}
CYCLE DELAY: {cycle}

""")

#variables to save last states read
cpu = None
ram = None
temp = None
cooler = None
fan = None
ip = None

#lcd control
def refresh(tcpu=0, tram=0, ttemp=0, tcooler="", tfan="", tip=""):
    global cpu, ram, temp, cooler, fan, ip
    if cpu != tcpu:                                 #update cpu if changed
        cpu = tcpu
        lcd.lcd_print(" "*10, 1, 0)
        lcd.lcd_print(f"CPU:{cpu}%", 1, 0)
    if ram != tram:                                 #update ram if changed
        ram = tram
        lcd.lcd_print(" "*10, 1, 10)
        lcd.lcd_print(f"RAM:{ram}G", 1, 10)
    if temp != ttemp:                               #update temp if changed
        temp = ttemp
        lcd.lcd_print(" "*10, 2, 0)
        lcd.lcd_print(f"TMP:{temp}C", 2, 0)
    if cooler != tcooler:                           #update cooler if changed
        cooler = tcooler
        lcd.lcd_print(" "*10, 3, 0)
        lcd.lcd_print(f"CLR:{tcooler}", 3, 0)
    if fan != tfan:                                 #update fan if changed
        fan = tfan
        lcd.lcd_print(" "*10, 3, 10)
        lcd.lcd_print(f"FAN:{tfan}", 3, 10)
    if ip != tip:                                   #update ip address if changed
        ip = tip
        lcd.lcd_print(" "*20, 4, 0)
        lcd.lcd_print(f"IP:{ip}", 4, 0)
    print(f"CPU:{cpu}%\tRAM:{ram}G\tTMP:{temp}C\tCLR:{cooler}\tFAN:{fan}\tIP:{ip}")
    return

motd = """\
+------------------+
|   INITIALISING   |
|  STATUS MONITOR  |
+------------------+"""
print(motd)
lcd.lcd_print("+------------------+", 1)
lcd.lcd_print("|   INITIALISING   |", 2)
lcd.lcd_print("|  STATUS MONITOR  |", 3)
lcd.lcd_print("+------------------+", 4)
sleep(5)
lcd.lcd_clear()

while True:
    tcpu = round(psutil.cpu_percent())                                      #get cpu percent
    tram = round(psutil.virtual_memory()[3]*(10**-9), 1)                    #get ram percent converted from byte to gigabyte
    ttemp = round(psutil.sensors_temperatures()["cpu_thermal"][0][1], 1)    #get cpu temperature
    tip = socket.gethostbyname(hostname)                                    #get ip address
    if cooler:
        if ttemp >= cooler_on:
            gpio.output(cooler_pin, True)
            tcooler = "ON"
        elif ttemp <= cooler_off:
            gpio.output(cooler_pin, False)
            tcooler = "OFF"
    else:
        gpio.output(cooler_pin, False)
        tcooler = "OFF"
    if fan:
        if ttemp >= fan_on:
            gpio.output(fan_pin, True)
            tfan = "ON"
        elif ttemp <= fan_off:
            gpio.output(fan_pin, False)
            tfan = "OFF"
    else:
        gpio.output(fan_pin, False)
        tfan = "OFF"
    refresh(tcpu, tram, ttemp, tcooler, tfan, tip)
    sleep(cycle)