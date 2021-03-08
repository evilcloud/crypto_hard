import adafruit_ssd1306
import busio
import time
import requests
import json
import crypto_prices

from PIL import Image, ImageDraw, ImageFont

from board import SCL, SDA
import busio
import adafruit_ssd1306

# from oled_ada import height, time_interval, width

height = 35
width = 128
time_interval = 900

# Initialize and clean screen
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
image = Image.new("1", (disp.width, disp.height))
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


def get_exchange_data(exchange):
    with open("venv/keys.json") as f:
        data = json.load(f)
    return data[exchange]["key"], data[exchange]["interval"]


# def coinmarketcap():
#     api_key, _ = get_exchange_data("CoinmarketCap")
#     url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
#     headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": api_key}

#     try:
#         response = requests.get(url, headers=headers)
#         resp = response.json()
#     except Exception as err:
#         print(err)
#         return 0, 0

#     btc = resp["data"][0]
#     eth = resp["data"][1]
#     price_data = lambda data: data["quote"]["USD"]["price"]
#     return price_data(btc), price_data(eth)


def crypto_direction(asset: str, price: float):
    unit_price = {
        "BTC": 35964.79,
        "ETH": 1563.85,
    }
    # if asset not in unit_price:
    #     return "?"
    if price:
        return "▲" if price > unit_price[asset] else "▼"
    return "X"


# def quote_line(asset: str, price: float, spaces: int) -> str:
#     icons = {
#         "BTC": "฿",
#         "ETH": "Δ",
#     }
#     return f"{icons[asset]} {int(price)} {crypto_direction(asset, price) if asset else 'X'}"


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
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    prices = crypto_prices.from_coinmarketcap(['BTC', 'ETH'])
    
    
    
    btc_quote, eth_quote = coinmarketcap()
    if btc_quote and eth_quote:
        btc = btc_quote
        eth = eth_quote
        btc_direction = crypto_direction("BTC", btc)
        eth_direction = crypto_direction("ETH", eth)
    else:
        # btc_direction = "X"
        draw.text((100, 25), "EX-ERROR", font=font_small, fill=255)

    icons = {
        "BTC": "฿",
        "ETH": "Δ",
    }

    btc_spaces, eth_spaces = line_spaces(btc, eth)
    draw.text(
        (0, 0),
        f"{icons['BTC']} {btc_spaces}{int(btc):,}{crypto_direction('BTC', btc)}",
        font=font,
        fill=255,
    )
    draw.text(
        (0, 15),
        f"{icons['ETH']} {eth_spaces}{int(eth):,}{crypto_direction('ETH', eth)}",
        font=font,
        fill=255,
    )

    for t in range(time_interval):
        draw.rectangle((100, 0, width, 24), outline=0, fill=0)
        mins, secs = divmod(time_interval - t, 60)
        timer = f"{mins:02d}:{secs:02d}"
        draw.text((100, 2), "next:", font=font_small, fill=255)
        draw.text((100, 12), str(timer), font=font_small, fill=255)

        disp.fill(0)
        disp.image(image)
        disp.show()
        time.sleep(1)