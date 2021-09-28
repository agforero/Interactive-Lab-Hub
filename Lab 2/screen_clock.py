import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
font = ImageFont.truetype("unifont.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Define buttons
topButton = digitalio.DigitalInOut(board.D23)
botButton = digitalio.DigitalInOut(board.D24)
topButton.switch_to_input()
botButton.switch_to_input()

def numToBase(n, b):
    if n == 0:
        return '0'

    ret = ""
    while n > 0:
        ret = str(n % b) + ret
        n //= b

    return ret


def unpackTimeToBase(TIME, b, spaces=2, indent=3):
    units = [int(unit) for unit in TIME.split(',')]
    bins = [numToBase(unit, b) for unit in units]    

    bins_distributedzeros = []
    for entry in bins:
        bins_distributedzeros.append(f"{'0' * (8-len(entry))}" + entry)

    labels = [
            u"MO",
            u"DA",
            u"YR",
            u"HR",
            u"MN",
            u"SC",
            ]

    symbols = {
            '0': u' ',
            '1': u'·',
            '2': u':',
            '3': u'∴',
            '4': u'⁘',
            '5': u'⁙'
            }

    ret = []
    for i, entry in enumerate(bins_distributedzeros):
        thisAddition = labels[i] + ' '
        for ch in entry:
            thisAddition += symbols[ch] + ' '*spaces
        
        ret.append(thisAddition)

    return ret


# import from lab2colors.py, get the colors, and set default scheme to white
from lab2colors import getColors
colors = getColors()
scheme = 0

bases = [2, 3, 4, 5, 6]
base_selection = 0 # holds the INDEX of the selection, not the value

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # handle buttons
    if not topButton.value:
        scheme = (scheme + 1) % len(colors)

    if not botButton.value:
        nxt = (base_selection + 1) % len(bases)
        base_selection = nxt

    # draw text
    y = top
    TIME = time.strftime("%m,%d,%y,%H,%M,%S")
    TIME_UNPACKED = unpackTimeToBase(TIME, bases[base_selection])
    y += font.getsize(TIME_UNPACKED[0])[1]
    for i, entry in enumerate(TIME_UNPACKED):
        draw.text((x, y), entry, font=font, fill=colors[scheme][i])
        y += font.getsize(entry)[1]

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.125)
