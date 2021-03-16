import json
import sys


def get_json(filename):
    """returns the settings from "settings.json" file

    Returns:
        dict: content of settings.json
    """
    with open(filename) as f:
        data = json.load(f)
    return data


# def numerize(entry):
#     return "".join(c for c in entry if c.isdigit())


def main():
    numerize = lambda entry: "".join(c for c in entry if c.isdigit())
    
    args = sys.argv
    width = 0
    height = 0
    if len(args) == 3:
        width = args[1]
        height = args[2]
    elif len(args) == 2:
        model = numerize(args[1])

        oleds = get_json("oled.json")
        model_res = oleds.get(model)
        if not model_res:
            model_res = oleds.get(numerize(model))
        input(model_res)

        model_res = oleds.get(model) if oleds.get(model) else oleds.get(numerize(model))
        if model_res:
            width, height = model_res

    if width and height:
        print(width, height)
    else:
        print("nope")


if __name__ == "__main__":
    main()
