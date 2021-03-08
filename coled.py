import adafruit_ssd1306
import busio
import sys
import time
import constructor
import crypto_prices
from PIL import Image, ImageDraw, ImageFont

from board import SCL, SDA

i2c = busio.I2C(SCL, SDA)


def oled_print(width, height, assets):
    disp = adafruit_ssd1306.SSD1306_I2C(width, height)
    image = Image.new("1", width, height)
    draw = ImageDraw.Draw(image)
    disp.fill(255)
    disp.show()
    time.sleep(1)
    disp.fill(0)
    disp.show()

    asset_nr = 1 if isinstance(assets, str) else len(assets)
    lines_height = (height / asset_nr) - (asset_nr - 1)
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", lines_height
    )
    font_small = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 8
    )

    while True:
        y_cursor = 0
        for line in constructor.construct_line(assets_prices):
            disp.fill(0)
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            assets_prices = crypto_prices.from_coinmarketcap(assets)
            draw.text((0, y_cursor), line, font=font, fill=255)
            disp.show()
            time.sleep(60)


def main():
    assets = ["BTC", "ETH"]
    width = 0
    height = 0
    oled_mod = {
        "091": ['0.91"', 128, 32],
        "112": ['1.12"', 128, 128],
    }
    numerize = lambda entry: "".join(list(filter(str.isdigit, entry)))
    args = sys.argv

    if len(args) == 2:
        # mod_numeric = filter(str.isdigit, args[1])
        _, width, height = oled_mod.get(numerize(args[1]))
    elif len(args) == 3:
        width = str(int(numerize(args[1])))
        height = str(int(numerize(args[2])))
        print(width, "x", height)

    if width and height:
        print(f"Launching OLED resolution {width} x {height} for {assets}")
        assets_prices = crypto_prices.from_coinmarketcap(
            ["BTC", "ETH", "DOT", "Cardano"]
        )
        for line in constructor.construct_line(assets_prices):
            print(line)

    else:
        print("Please provide OLED model")
        print("Currently supprted models are:")
        for entry in oled_mod:
            model, _, _ = oled_mod.get(entry)
            print(f"\t{model}")

        print("\nor provide resolution, like 128, 32")


if __name__ == "__main__":
    main()