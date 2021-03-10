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


def get_json(filename):
    """returns the settings from "settings.json" file

    Returns:
        dict: content of settings.json
    """
    with open(filename) as f:
        data = json.load(f)
    return data


def oled_setup(width, height):
    i2c = busio.I2C(SCL, SDA)
    disp = adafruit_ssd1306.SSD1306_I2C(width, height, i2c)
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    disp.fill(255)
    disp.show()
    time.sleep(1)
    disp.fill(0)
    disp.show()
    return disp, image, draw


def oled_print(width, height):
    """Prints line by line assets information

    Args:
        width (int): width of the OLED screen
        height (int): height of the OLED screen
        assets (list): a list of assets
    """
    disp, image, draw = oled_setup(width, height)

    # this is the endless loop
    while True:
        assets = get_json("settings.json")["assets"]
        assets_prices = crypto_prices.from_coinmarketcap(assets)
        lines = constructor.construct_line(assets_prices)
        for line in lines:
            print(line)

        asset_nr = 1 if isinstance(assets, str) else len(assets)
        nominal_height = (height / asset_nr) - (asset_nr - 1)
        lines_height = int(nominal_height) if nominal_height <= 14 else 14
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", int(lines_height)
        )
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 7
        )

        y_cursor = 0
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        for line in lines:
            disp.fill(0)
            draw.text((0, y_cursor), line, font=font, fill=255)
            y_cursor = y_cursor + lines_height + 1
        disp.image(image)
        disp.show()

        # update interval, but make sure we don't DDOS ourselves with stupid requests
        interval = get_json("settings.json")["interval"]
        if not interval:
            print("No valid interval indication loaded")
            interval = 900
        i_min, i_sec = divmod(interval, 60)
        print(f"next cycle interval is in {i_min} min {i_sec} sec")
        for i in tqdm(range(interval)):
            draw.text((width - 10, height - 10), f"{i/interval*100}%")
            disp.image(image)
            disp.show()
            time.sleep(1)
            draw.rectangle((width - 10, height - 10, width, height), outline=0, fill=0)
            disp.image(image)
            disp.show()


def main():
    width = 0
    height = 0
    oled_mod = {
        "091": ['0.91"', 128, 32],
        "112": ['1.12"', 128, 128],
    }
    numerize = lambda entry: "".join(list(filter(str.isdigit, entry)))
    args = sys.argv

    # oleds = get_json("oled.json")
    # for model in oleds:
    #     oled_mod[numerize(model)] = oleds
    if len(args) == 2:
        # mod_numeric = filter(str.isdigit, args[1])
        _, width, height = oled_mod.get(numerize(args[1]))
    elif len(args) == 3:
        width = str(int(numerize(args[1])))
        height = str(int(numerize(args[2])))
        print(width, "x", height)

    if width and height:
        print(f"Launching OLED resolution {width} x {height}")
        oled_print(width, height)

    else:
        print("Please provide OLED model")
        print("Currently supported models are:")
        for entry in oled_mod:
            model, _, _ = oled_mod.get(entry)
            print(f"\t{model}")

        print("\nor provide resolution, like 128, 32")


if __name__ == "__main__":
    main()