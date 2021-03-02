# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

from os import getpgid
import time
import requests

# from pycoingecko import CoinGeckoAPI

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# # Create blank image for drawing.
# # Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# # Get drawing object to draw on image.
draw = ImageDraw.Draw(image)


# Load default font.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
font_small = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 8
)

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)


from requests.api import get

time_interval = 60


def get_prices():
    api_key = "ce24263e-b0fa-4be8-8e5c-9e5f64697b52"
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": api_key}
    response = requests.get(url, headers=headers)
    response_json = response.json()

    btc_price = response_json["data"][0]
    eth_price = response_json["data"][1]
    return btc_price["quote"]["USD"]["price"], eth_price["quote"]["USD"]["price"]


duration = 900
while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # CoinGecko
    # cg = CoinGeckoAPI()
    # print(cg.ping())
    # btc_price = cg.get_price(ids="bitcoin", vs_currencies="usd")["bitcoin"]["usd"]
    # eth_price = cg.get_price(ids="ethereum", vs_currencies="usd")["ethereum"]["usd"]

    btc_price, eth_price = get_prices()
    bit_dir = "▲" if btc_price > 35964.79 else "▼"
    eth_dir = "▲" if eth_price > 1563.85 else "▼"
    # Display image.
    draw.text((0, 0), "฿ " + f"{int(btc_price):,}" + bit_dir, font=font, fill=255)
    draw.text((0, 15), "Δ  " + f" {int(eth_price):,}" + eth_dir, font=font, fill=255)
    disp.image(image)
    disp.show()

    t = 0
    for t in range(duration):
        mins, secs = divmod(duration - t, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)

        draw.rectangle((100, 0, width, height), outline=0, fill=0)

        # dial = height / 60
        # draw.rectangle(
        #     (width - 4, dial * secs, width, dial * secs), outline=1, fill=255
        # )
        # draw.rectangle((width - 2, height, width, dial * mins), outline=1, fill=255)
        draw.text((100, 5), "next:", font=font_small, fill=255)
        draw.text((100, 15), str(timer), font=font_small, fill=255)

        disp.fill(0)
        disp.image(image)
        disp.show()
        time.sleep(1)
