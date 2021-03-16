import sys
import time
import json
import constructor
import crypto_prices
from tqdm import tqdm


def get_json(filename):
    """returns the settings from "settings.json" file

    Returns:
        dict: content of settings.json
    """
    with open(filename) as f:
        data = json.load(f)
    return data


def oled_setup(width, height):
    import adafruit_ssd1306
    import busio
    from PIL import Image, ImageDraw, ImageFont
    from board import SCL, SDA

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
            draw.rectangle(
                (width - 2, height - 2, width, height),
                outline=0,
                fill=0,
            )
            # draw.text(
            #     (width - 20, height - 10),
            #     f"{int(i/interval*100)}%",
            #     font=font_small,
            #     fill=255,
            # )
            disp.image(image)
            disp.show()
            time.sleep(1)
            draw.rectangle((width, height, width - 2, height - 2), outline=0, fill=255)
            disp.image(image)
            disp.show()


def main():
    numerize = lambda entry: "".join(c for c in entry if c.isdigit())

    args = sys.argv
    width = 0
    height = 0
    oleds = get_json("oled.json")

    if len(args) == 3:
        width = args[1]
        height = args[2]
    elif len(args) == 2:
        model = numerize(args[1])

        model_res = oleds.get(model)
        if not model_res:
            model_res = oleds.get(numerize(model))

        model_res = oleds.get(model) if oleds.get(model) else oleds.get(numerize(model))
        if model_res:
            width, height = model_res

    if width and height:
        print(f"Launching OLED resolution {width} x {height}")
        oled_print(width, height)

    else:
        print("Please provide OLED model")
        print("Currently supported models are:")
        for entry in oleds:
            print(f"\t{entry}: {oleds[entry][0]} x {oleds[entry][1]}")

        print("\nor provide resolution like: 128, 32")


if __name__ == "__main__":
    main()