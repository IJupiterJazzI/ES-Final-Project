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
from GestureExampleLists import GestureExampleLists

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
count = 0
# These are the lists that will hold the accelerometer data from the user's gesture input
userGesture=[]
listX = []
listY = []
listZ = []
corrList = []

finalGesture = "no gesture"

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
        # STAGE 00:Checks if button is pushed
        if button.value != True:
            stage = 1
    elif stage == 1:
        #  STAGE 01:Checks if button is released
        if button.value == True:
            stage = 2
    elif stage == 2:
        # STAGE 02:This code records the users gesture by adding the
        # x, y, and z values from the accelerometer to three different
        # lists that are then combined into one singular userGesture list
        if count < 100:
            # append the x,y,z data to the lists
            listX.append(xCoord.value)
            listY.append(yCoord.value)
            listZ.append(zCoord.value)
            count += 1
            time.sleep(0.02)
        if count == 100:
            # append the x,y,z lists to the userGesture list
            userGesture.append(listX)
            userGesture.append(listY)
            userGesture.append(listZ)
            stage == 3
    elif stage == 3:
        # STAGE 03: Calculates the correlation between the user input and
        # the Example Gesture Lists for each gesture. Then, those correlation
        # values are averaged for each gesture.

        # RAISE VOLUME/UP GESTURE CORRELATION
        upCorr1 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.upGesture1)
        upCorr2 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.upGesture2)
        upCorr3 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.upGesture3)
        upCorr4 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.upGesture4)
        upCorr5 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.upGesture5)
        upCorr6 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.upGesture6)
        upCorr7 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.upGesture7)
        upCorr8 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.upGesture8)
        upCorr9 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.upGesture9)
        upCorr10 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.upGesture10)
        upCorrAvg = (upCorr1+upCorr2+upCorr3+upCorr3+upCorr4+upCorr5+upCorr6+upCorr7+upCorr8+upCorr9+upCorr10) / 10

        # LOWER VOLUME/DOWN GESTURE CORRELATION
        downCorr1 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.downGesture1)
        downCorr2 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.downGesture2)
        downCorr3 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.downGesture3)
        downCorr4 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.downGesture4)
        downCorr5 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.downGesture5)
        downCorr6 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.downGesture6)
        downCorr7 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.downGesture7)
        downCorr8 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.downGesture8)
        downCorr9 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.downGesture9)
        downCorr10 = GestureFunctions.corrForListsOfLists(userGesture, GestureExampleLists.downGesture10)
        downCorrAvg = (downCorr1+downCorr2+downCorr3+downCorr3+downCorr4+downCorr5+downCorr6+downCorr7+downCorr8+downCorr9+downCorr10) / 10

        # GO BACK/LEFT GESTURE CORRELATION
        leftCorr1 = corrForListsOfLists(userGesture, GestureExampleLists.leftGesture1)
        leftCorr2 = corrForListsOfLists(userGesture, GestureExampleLists.leftGesture2)
        leftCorr3 = corrForListsOfLists(userGesture, GestureExampleLists.leftGesture3)
        leftCorr4 = corrForListsOfLists(userGesture, GestureExampleLists.leftGesture4)
        leftCorr5 = corrForListsOfLists(userGesture, GestureExampleLists.leftGesture5)
        leftCorr6 = corrForListsOfLists(userGesture, GestureExampleLists.leftGesture6)
        leftCorr7 = corrForListsOfLists(userGesture, GestureExampleLists.leftGesture7)
        leftCorr8 = corrForListsOfLists(userGesture, GestureExampleLists.leftGesture8)
        leftCorr9 = corrForListsOfLists(userGesture, GestureExampleLists.leftGesture9)
        leftCorr10 = corrForListsOfLists(userGesture, GestureExampleLists.leftGesture10)
        leftCorrAvg = (leftCorr1+leftCorr2+leftCorr3+leftCorr3+leftCorr4+leftCorr5+leftCorr6+leftCorr7+leftCorr8+leftCorr9+leftCorr10) / 10

        # SKIP SONG/RIGHT GESTURE CORRELATION
        rightCorr1 = corrForListsOfLists(userGesture, GestureExampleLists.rightGesture1)
        rightCorr2 = corrForListsOfLists(userGesture, GestureExampleLists.rightGesture2)
        rightCorr3 = corrForListsOfLists(userGesture, GestureExampleLists.rightGesture3)
        rightCorr4 = corrForListsOfLists(userGesture, GestureExampleLists.rightGesture4)
        rightCorr5 = corrForListsOfLists(userGesture, GestureExampleLists.rightGesture5)
        rightCorr6 = corrForListsOfLists(userGesture, GestureExampleLists.rightGesture6)
        rightCorr7 = corrForListsOfLists(userGesture, GestureExampleLists.rightGesture7)
        rightCorr8 = corrForListsOfLists(userGesture, GestureExampleLists.rightGesture8)
        rightCorr9 = corrForListsOfLists(userGesture, GestureExampleLists.rightGesture9)
        rightCorr10 = corrForListsOfLists(userGesture, GestureExampleLists.rightGesture10)
        rightCorrAvg = (rightCorr1+rightCorr2+rightCorr3+rightCorr3+rightCorr4+rightCorr5+rightCorr6+rightCorr7+rightCorr8+rightCorr9+rightCorr10) / 10

        # MASTER LIST OF ALL GESTURE CORRELATION AVERAGES
        corrList = [upCorrAvg, downCorrAvg, leftCorrAvg, rightCorrAvg]

        stage = 4
    elif stage == 4:
        # STAGE 04: Chooses whichever correlation number is the largest,
        # above a certain value, and then sends that command to the website.
        print(upCorrAvg)

        # If there is very little correlation to any of the gestures,
        # then it is registered as no gesture
        if max(corrList) < 6: #TODO Choose number
            finalGesture = "no gesture"
        # Chooses whichever gesture that the users gesture has the most
        # correlation to at sets that to finalOut
        elif max(corrList) == upCorrAvg:
            finalGesture = "up gesture"
        elif max(corrList) == downCorrAvg:
            finalGesture = "down gesture"
        elif max(corrList) == leftCorrAvg:
            finalGesture = "left gesture"
        elif max(corrList) == rightCorrAvg:
            finalGesture = "right gesture"

        # This posts the gesture to the speaker website so that the speaker knows
        # which gesture was done and in effect, what command the speaker needs to do
        try:
            s = "http://608dev.net/sandbox/mostec/speaker?gesture={}".format(finalGesture)
            c = requests.post(s)
            print (s)
        except Exception as e:
            print(e)

        stage = 5
    elif stage == 5:
        # STAGE 05: This stage resets and clears all the necessary values so
        # that the glove can take in another gesture
        userGesture.clear()
        listX.clear()
        listY.clear()
        listZ.clear()
        corrList.clear()
        finalGesture = "no gesture"
        count = 0