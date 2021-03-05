import adafruit_ssd1306
import busio
import time
import requests
import json

from PIL import Image, ImageDraw, ImageFont

from board import SCL, SDA
import busio
import adafruit_ssd1306
from oled_ada import height, time_interval, width


# Initialize and clean screen
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
image = Image.new("1", disp.width, disp.height)
draw = ImageDraw.Draw(image)
disp.fill(255)
disp.show()
time.sleep(1)
disp.fill(0)
disp.show()

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
font_small = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 8
)


def coinmarketcap():
    api_key = "ce24263e-b0fa-4be8-8e5c-9e5f64697b52"
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": api_key}

    try:
        response = requests.get(url, headers=headers)
        resp = response.json()
    except Exception as err:
        print(err)
        return 0, 0

    btc = resp["data"][0]
    eth = resp["data"][1]
    price_data = lambda data: data["quote"]["USD"]["price"]
    return price_data(btc), price_data(eth)


def crypto_direction(asset: str, price: float):
    unit_price = {
        "BTC": 35964.79,
        "ETH": 1563.85,
    }
    if asset not in unit_price:
        return "?"
    return "▲" if price > unit_price["asset"] else "▼"


def quote_line(asset: str, price: float, spaces: int) -> str:
    icons = {
        "BTC": "฿",
        "ETH": "Δ",
    }
    return f"{icons['icons']} {int(price)} {crypto_direction(asset, price)}"


def line_spaces(btc, eth):
    btc_len = len(str(int(btc)))
    eth_len = len(str(int(eth)))
    max_dist = max(btc_len, eth_len)
    btc_spaces = max_dist - btc_len
    eth_spaces = max_dist - eth_len
    return btc_spaces, eth_spaces


time_interval = 60
btc = 0
eth = 0

while True:
    disp.fill(0)
    btc_quote, eth_quote = coinmarketcap()
    if btc_quote and eth_quote:
        btc = btc_quote
        eth = eth_quote
        btc_direction = crypto_direction("BTC", btc)
        eth_direction = crypto_direction("ETH", eth)
    else:
        btc_direction = "X"
        draw.text((100, 25), "EX-ERROR", font=font_small, fill=255)

    btc_spaces, eth_spaces = line_spaces(btc, eth)
    draw.text((0, 0), quote_line("BTC", btc, btc_spaces), font=font, fill=255)
    draw.text((0, 15), quote_line("ETH", eth, eth_spaces), font=font, fill=255)

    for t in range(time_interval):
        mins, secs = divmod(time_interval - t, 60)
        timer = "{:02d}:{02d}".format(mins, secs)
        draw.text((100, 2), "next:", font=font_small, fill=255)
        draw.text((100, 12), str(timer), font=font_small, fill=255)

        disp.fill(0)
        disp.image(image)
        disp.show()
        time.sleep(1)