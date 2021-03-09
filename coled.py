import adafruit_ssd1306
import busio
import sys
import time
import constructor
import crypto_prices
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont

from board import SCL, SDA


def oled_print(width, height, assets):
    """Prints line by line assets information

    Args:
        width (int): width of the OLED screen
        height (int): height of the OLED screen
        assets (list): a list of assets
    """
    i2c = busio.I2C(SCL, SDA)
    disp = adafruit_ssd1306.SSD1306_I2C(width, height, i2c)
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    disp.fill(255)
    disp.show()
    time.sleep(1)
    disp.fill(0)
    disp.show()

    asset_nr = 1 if isinstance(assets, str) else len(assets)
    nominal_height = (height / asset_nr) - (asset_nr - 1)
    lines_height = nominal_height if nominal_height <= 14 else 14
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", int(lines_height)
    )
    font_small = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", lines_height
    )

    while True:
        y_cursor = 0
        # assets_prices = crypto_prices.from_coinmarketcap(assets)
        # for line in constructor.construct_line(assets_prices):
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        for line in assets:
            disp.fill(0)
            draw.text((0, y_cursor), line, font=font, fill=255)
            print(f"{line} on line {y_cursor}")
            y_cursor = +lines_height + 1
        disp.Image(image)
        disp.show()
        for _ in tqdm(range(600)):
            time.sleep(0.1)


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
        assets_prices = crypto_prices.from_coinmarketcap(assets)
        lines = constructor.construct_line(assets_prices)
        for line in lines:
            print(line)
        oled_print(width, height, lines)

    else:
        print("Please provide OLED model")
        print("Currently supprted models are:")
        for entry in oled_mod:
            model, _, _ = oled_mod.get(entry)
            print(f"\t{model}")

        print("\nor provide resolution, like 128, 32")


if __name__ == "__main__":
    main()