import board
import busio
import audiomp3
import audioio
import digitalio
import displayio
import time
from analogio import AnalogIn
from analogio import AnalogOut
from digitalio import DigitalInOut
import neopixel
from math import log
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests
from adafruit_st7735r import ST7735R
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.roundrect import RoundRect
import terminalio
from adafruit_display_text.label import Label
#set up the screen:
#spi = board.SPI()
tft_cs = board.D5
tft_dc = board.D6
displayio.release_displays()
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D7)
display = ST7735R(display_bus, width=128, height=160, colstart=0, rowstart=0)
scene = displayio.Group(max_size=10)
display.show(scene)
SCREEN_WIDTH = 127
SCREEN_HEIGHT = 159


#Volume Control
switchVup = digitalio.DigitalInOut(board.D2)
switchVup.switch_to_input(pull=digitalio.Pull.UP)
switchVdown = digitalio.DigitalInOut(board.D3)
switchVdown.switch_to_input(pull=digitalio.Pull.UP)
volume_fill = 10
volume_pos = 15
volume_bar = RoundRect(15, 0, 100, int(SCREEN_HEIGHT/20), 5, fill=0xFFFFFF)
volume_status = RoundRect(volume_pos, 0 , volume_fill, int(SCREEN_HEIGHT/20), 5, fill=0x00FF00)

#Pause/Play/Skip UI
ui_playpause = Circle(64, 130, 15, fill=0xFFFFFF)
ui_back = Circle(32, 130, 15, fill=0x00FF00)
ui_next = Circle(96, 130, 15, fill=0x00FF00)
ui_thumbnail = RoundRect(24,25, 80, 80, 10, fill=0xFFFFFF)
image_next = Triangle(90,120, 90, 140, 107, 130, fill = 0x000000)
image_back = Triangle(39, 120, 39, 140, 22, 130, fill = 0x000000)
#Append Assets
scene.append(volume_bar)
scene.append(ui_playpause)
scene.append(ui_back)
scene.append(ui_next)
scene.append(ui_thumbnail)
scene.append(image_next)
scene.append(image_back)
scene.append(volume_status)
#Speaker and playlist step-up
i = 0
state = 0
play_pause_state = 0 #0 is playing and 1 is paused
speaker = audioio.AudioOut(board.A0)
playlist = ("oboe.mp3", "bach.mp3", "insp.mp3", "marimba.mp3", "sax.mp3", "shaku.mp3")
open_song = open(playlist[i], "rb")
print(playlist[i])
current_song = audiomp3.MP3Decoder(open_song)

print("playing")

#internet stuff
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
requests.set_socket(socket, esp)

from secrets import secrets

dot = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

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
    if state == 0:
        speaker.play(current_song)
        while speaker.playing:
            try:
                r = requests.get("http://608dev.net/sandbox/mostec/speaker?gesture")#I just ended up calling it "string" but idk
                print(r.text)
                if r.text == "skip song":
                    i += 1
                    current_song = audiomp3.MP3Decoder(open_song)
                    speaker.play(current_song)
                    state = 0
                elif r.text == "back song":
                    i -= 1
                    current_song = audiomp3.MP3Decoder(open_song)
                    speaker.play(current_song)
                    state = 0
                elif r.text == "volume up":
                    if volume_fill >= 100:
                        volume_fill = 100
                        state = 0
                    else:
                        volume_fill += 9
                        scene.pop(7)
                        scene.append(volume_status)
                        scene[7] = RoundRect(volume_pos, 0 , volume_fill, int(SCREEN_HEIGHT/20), 5, fill=0x00FF00)
                        #Potentionmeter resistance drop
                        state = 0
                elif r.text == "volume down":
                    if volume_fill <= 10:
                        volume_fill = 10
                        state = 0
                    else:
                        volume_fill -= 9
                        scene.pop(7)
                        scene.append(volume_status)
                        scene[7] = RoundRect(volume_pos, 0 , volume_fill, int(SCREEN_HEIGHT/20), 5, fill=0x00FF00)
                        #Potentionmeter resistance rise
                        state = 0
                elif r.text == "play/pause":
                    if play_pause_state == 0: #if it was already playing
                        speaker.pause()
                        play_pause_state = 1 #change state to paused
                        state = 0 #Go back to passive state
                    elif play_pause_state == 1: #if it was already paused
                        speaker.resume()
                        play_pause_state = 0 #change state to playing
                        state = 0 #Go back to passive state
                elif r.text == "no gesture":
                    state = 0
            except Exception as e:
                print(e)
            time.sleep(0.04)
