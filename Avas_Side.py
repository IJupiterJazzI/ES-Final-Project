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

userGesture=[]
listX = []
listY = []
listZ = []

def offset_and_normalize(inp):
    mean_input = sum(inp) / len(inp)
    remove_offset = [x-mean_input for x in inp]
    norm_factor = (sum([x*x for x in remove_offset]))**0.5
    return [x/norm_factor for x in remove_offset]

def correlation(x,y):
    norm_x = offset_and_normalize(x)
    norm_y = offset_and_normalize(y)
    sum_of_products = sum([x*y for (x,y) in zip(norm_x,norm_y)])
    return sum_of_products

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
    if stage == 0:
        if button.value == True:
            stage = 1
    elif stage == 1:
        if button.value != True:
            stage = 2
    elif stage == 2:
        if count < 100:
            listX.append(xCoord.value)
            listY.append(yCoord.value)
            listZ.append(zCoord.value)
            time.sleep(0.02)
        if count == 100:
            userGesture[0] = listX
            userGesture[1] = listY
            userGesture[2] = listZ
            stage == 3
    elif stage == 3:
        upCorr1 = correlation(userGesture, upGesture1)
        upCorr2 = correlation(userGesture, upGesture2)
        upCorr3 = correlation(userGesture, upGesture3)
        upCorr4 = correlation(userGesture, upGesture4)
        upCorr5 = correlation(userGesture, upGesture5)
        upCorr6 = correlation(userGesture, upGesture6)
        upCorr7 = correlation(userGesture, upGesture7)
        upCorr8 = correlation(userGesture, upGesture8)
        upCorr9 = correlation(userGesture, upGesture9)
        upCorr10 = correlation(userGesture, upGesture10)
        upCorrAvg = (upCorr1+upCorr2+upCorr3+upCorr3+upCorr4+upCorr5+upCorr6+upCorr7+upCorr8+upCorr9+upCorr10) / 10

        stage = 4
    elif stage == 4:
        #Depending on which correlation # is the largest
        #that string will be sent to the website



#while True:
    #try:
        #what i think should work
        #s = "http://608dev.net/sandbox/mostec/speaker?x={}&y={}&z={}".format(x.value,y.value,z.value)
       # c = requests.post(s)
       # print (s)