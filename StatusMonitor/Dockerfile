FROM python:3

WORKDIR /status_monitor
COPY . .

ENV COOLER_ON=50
ENV COOLER_OFF=40
ENV FAN_ON=55
ENV FAN_OFF=50
ENV DELAY=5

RUN pip install -r requirements.txt
RUN CFLAGS="-fcommon" pip install RPi.GPIO
CMD python "status-monitor.py" --cooler-on $COOLER_ON --cooler-off $COOLER_OFF --fan-on $FAN_ON --fan-off $FAN_OFF --delay $DELAY