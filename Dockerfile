FROM python:3

ADD status-monitor.py /
ADD I2C_LCD_driver_UBUNTU.py /

RUN pip install smbus2
RUN pip install RPi.GPIO
RUN pip install psutil

CMD ["python", "./status-monitor.py"]
