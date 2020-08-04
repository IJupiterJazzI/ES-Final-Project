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

button = digitalio.DigitalInOut(board.D0)
button.switch_to_input(pull=digitalio.Pull.UP)

#internet stuff we copied and pasted
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
requests.set_socket(socket, esp)

# These are the lists that will hold the accelerometer data from the user's gesture input
count = 0
stage = 0
upGesture1=[]
listX = []
listY = []
listZ = []

# wifi set up stuffs
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
print(button.value)

while True:
    if stage == 0:
        # Checks if button is pushed
        if button.value != True:
            stage = 1
    elif stage == 1:
        # This code records the users gesture by adding the x, y, and z
        # values from the accelerometer to three different lists.
        # Then, these lists are printed out.
        if (count < 100):
            # Append the x,y,z data to the lists
            listX.append(xCoord.value)
            listY.append(yCoord.value)
            listZ.append(zCoord.value)
            count += 1
            time.sleep(0.02)
        if count == 100:
            # The lists are printed out
            print("[")
            print(listX)
            print(",")
            print(listY)
            print(",")
            print(listZ)
            print("]")
            stage = 2
    elif stage == 2:
        # Clear the lists and reset the code so that
        # it is ready to collect and print out a new
        # list of lists of data
        if button.value:
            listX.clear()
            listY.clear()
            listZ.clear()
            count = 0
            print("Ready for the next gesture")
            stage = 0
