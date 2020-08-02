import board
import displayio
import digitalio
import time
import busio
from analogio import AnalogIn
from math import log
from analogio import AnalogOut
import audioio
from adafruit_st7735r import ST7735R
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.roundrect import RoundRect
import terminalio
from adafruit_display_text.label import Label
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests

#x,y,z for accelerometer
from analogio import AnalogIn
xCoord = AnalogIn(board.A0)
yCoord = AnalogIn(board.A1)
zCoord = AnalogIn(board.A2)

#internet stuff we copied and pasted
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
requests.set_socket(socket, esp)
count = 0

upXList1 = []
upYList1 = []
upZList1 = []


from secrets import secrets

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")
print("Connecting to AP...")

while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)

while True:
    if (count < 100):
        upXList1.append(xCoord.value)
        upYList1.append(yCoord.value)
        upZList1.append(zCoord.value)
        time.sleep(1.0)

#while True:
    #try:
        #what i think should work
        #s = "http://608dev.net/sandbox/mostec/speaker?x={}&y={}&z={}".format(x.value,y.value,z.value)
       # c = requests.post(s)
       # print (s)