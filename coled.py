import adafruit_ssd1306
import busio
import sys
import time
import json
import constructor
import crypto_prices
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont

from board import SCL, SDA


def get_assets():
    with open("assets.json") as f:
        data = json.load(f)
    return data["assets"]


def oled_print(width, height):
    """Prints line by line assets information

    Args:
        width (int): width of the OLED screen
        height (int): height of the OLED screen
        assets (list): a list of assets
    """

    # Setting up the OLED and making the first clean up
    i2c = busio.I2C(SCL, SDA)
    disp = adafruit_ssd1306.SSD1306_I2C(width, height, i2c)
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    disp.fill(255)
    disp.show()
    time.sleep(1)
    disp.fill(0)
    disp.show()

    # Let's get looping and working
    while True:
        assets = get_assets()
        assets_prices = crypto_prices.from_coinmarketcap(assets)
        lines = constructor.construct_line(assets_prices)
        for line in lines:
            print(line)
        # oled_print(width, height, lines)

        asset_nr = 1 if isinstance(assets, str) else len(assets)
        nominal_height = (height / asset_nr) - (asset_nr - 1)
        lines_height = int(nominal_height) if nominal_height <= 14 else 14
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", int(lines_height)
        )
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", lines_height
        )

        y_cursor = 0
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        for line in lines:
            disp.fill(0)
            draw.text((0, y_cursor), line, font=font, fill=255)
            print(f"{line} on line {y_cursor}")
            y_cursor = y_cursor + lines_height + 1
        disp.image(image)
        disp.show()
        for _ in tqdm(range(900)):
            time.sleep(1)


def main():
    assets = ["BTC", "ETH", "DOT"]
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
        # assets_prices = crypto_prices.from_coinmarketcap(assets)
        # lines = constructor.construct_line(assets_prices)
        # for line in lines:
        #     print(line)
        # oled_print(width, height, lines)
        oled_print(width, height)

    else:
        print("Please provide OLED model")
        print("Currently supprted models are:")
        for entry in oled_mod:
            model, _, _ = oled_mod.get(entry)
            print(f"\t{model}")

        print("\nor provide resolution, like 128, 32")


if __name__ == "__main__":
    main()