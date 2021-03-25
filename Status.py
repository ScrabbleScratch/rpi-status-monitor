import I2C_LCD_driver as driver     #modified script to work on Ubuntu
import RPi.GPIO as gpio             #to take control of the gpio pins
import socket                       #to get ip address
import psutil                       #to read system stats
from time import sleep              #to ake pauses between reads

lcd = driver.lcd()

gpio.setmode(gpio.BCM)              #set gpio label to BCM
gpio.setup(17, gpio.OUT)            #set gpio pin 17 as output for fan

on_temp = 50                        #temperature to turn fan on
off_temp = 45                       #temperature to turn fan off

cpu = None                          #variable to save last cpu value
ram = None                          #variable to save last ram value
temp = None                         #variable to save last temperature
fan = None                          #variable to save last fan state
ip = None                           #variable to save last ip address

def refresh(tcpu=0, tram=0, ttemp=0, tfan="", tip=""):
    global cpu, ram, temp, fan, ip
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
    if fan != tfan:                                 #update fan if changed
        fan = tfan
        lcd.lcd_print(" "*10, 2, 10)
        lcd.lcd_print(f"FAN:{fan}", 2, 10)
    if ip != tip:                                   #update ip address if changed
        ip = tip
        lcd.lcd_print(" "*20, 4, 0)
        lcd.lcd_print(f"IP:{ip}", 4, 0)
    print(f"CPU:{cpu}%\tRAM:{ram}G\tTMP:{temp}C\tFAN:{fan}\tIP:{ip}")
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
    tip = socket.gethostbyname(socket.gethostname())                        #get ip address
    if fan:
        if ttemp >= on_temp:
            gpio.output(17, True)
            tfan = "ON"
        elif ttemp <= off_temp:
            gpio.output(17, False)
            tfan = "OFF"
    else:
        gpio.output(17, False)
        tfan = "OFF"
    refresh(tcpu, tram, ttemp, tfan, tip)
    sleep(5)
