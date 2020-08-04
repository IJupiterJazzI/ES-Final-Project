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
import GestureExampleLists

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

stage = 0
# These are the lists that will hold the accelerometer data from the user's gesture input
userGesture=[]
listX = []
listY = []
listZ = []
corrList = []

# These next two fuctions check for the correlation between two different lists of lists
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

while True:
    if stage == 0:
        # Checks if button is pushed
        if button.value == True:
            stage = 1
    elif stage == 1:
        # Checks if button is released
        if button.value != True:
            stage = 2
    elif stage == 2:
        # This code records the users gesture by adding the x, y, and z
        # values from the accelerometer to three different lists that
        # are then combined into one singular userGesture list
        if count < 100:
            # append the x,y,z data to the lists
            listX.append(xCoord.value)
            listY.append(yCoord.value)
            listZ.append(zCoord.value)
            time.sleep(0.02)
        if count == 100:
            # append the x,y,z lists to the userGesture list
            userGesture[0] = listX
            userGesture[1] = listY
            userGesture[2] = listZ
            stage == 3
    elif stage == 3:
        # Calculates the correlation between the user input and the Example
        # Gesture Lists for each gesture. Then, those correlation values 
        # are averaged for each gesture.

        # RAISE VOLUME/UP GESTURE CORRELATION
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

        # LOWER VOLUME/DOWN GESTURE CORRELATION
        downCorr1 = correlation(userGesture, downGesture1)
        downCorr2 = correlation(userGesture, downGesture2)
        downCorr3 = correlation(userGesture, downGesture3)
        downCorr4 = correlation(userGesture, downGesture4)
        downCorr5 = correlation(userGesture, downGesture5)
        downCorr6 = correlation(userGesture, downGesture6)
        downCorr7 = correlation(userGesture, downGesture7)
        downCorr8 = correlation(userGesture, downGesture8)
        downCorr9 = correlation(userGesture, downGesture9)
        downCorr10 = correlation(userGesture, downGesture10)
        downCorrAvg = (downCorr1+downCorr2+downCorr3+downCorr3+downCorr4+downCorr5+downCorr6+downCorr7+downCorr8+downCorr9+downCorr10) / 10

        # GO BACK/LEFT GESTURE CORRELATION
        leftCorr1 = correlation(userGesture, leftGesture1)
        leftCorr2 = correlation(userGesture, leftGesture2)
        leftCorr3 = correlation(userGesture, leftGesture3)
        leftCorr4 = correlation(userGesture, leftGesture4)
        leftCorr5 = correlation(userGesture, leftGesture5)
        leftCorr6 = correlation(userGesture, leftGesture6)
        leftCorr7 = correlation(userGesture, leftGesture7)
        leftCorr8 = correlation(userGesture, leftGesture8)
        leftCorr9 = correlation(userGesture, leftGesture9)
        leftCorr10 = correlation(userGesture, leftGesture10)
        leftCorrAvg = (leftCorr1+leftCorr2+leftCorr3+leftCorr3+leftCorr4+leftCorr5+leftCorr6+leftCorr7+leftCorr8+leftCorr9+leftCorr10) / 10

        # SKIP SONG/RIGHT GESTURE CORRELATION
        rightCorr1 = correlation(userGesture, rightGesture1)
        rightCorr2 = correlation(userGesture, rightGesture2)
        rightCorr3 = correlation(userGesture, rightGesture3)
        rightCorr4 = correlation(userGesture, rightGesture4)
        rightCorr5 = correlation(userGesture, rightGesture5)
        rightCorr6 = correlation(userGesture, rightGesture6)
        rightCorr7 = correlation(userGesture, rightGesture7)
        rightCorr8 = correlation(userGesture, rightGesture8)
        rightCorr9 = correlation(userGesture, rightGesture9)
        rightCorr10 = correlation(userGesture, rightGesture10)
        rightCorrAvg = (rightCorr1+rightCorr2+rightCorr3+rightCorr3+rightCorr4+rightCorr5+rightCorr6+rightCorr7+rightCorr8+rightCorr9+rightCorr10) / 10

        # MASTER LIST OF ALL GESTURE CORRELATION AVERAGES
        corrList = [upCorrAvg, downCorrAvg, leftCorrAvg, rightCorrAvg]

        stage = 4
    elif stage == 4:
        print(upCorrGesture)

        #Depending on which correlation # is the largest
        #that string will be sent to the website



#while True:
    #try:
        #what i think should work
        #s = "http://608dev.net/sandbox/mostec/speaker?x={}&y={}&z={}".format(x.value,y.value,z.value)
       # c = requests.post(s)
       # print (s)