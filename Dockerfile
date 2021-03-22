from python:3

ADD I2C_LCD_driver.py /
ADD Status.py /

RUN pip install smbus2
RUN pip install RPi.GPIO
RUN pip install psutil

CMD ["python", "./Status.py"]

