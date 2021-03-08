import sys


def main():
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
        print(f"Launching OLED resolution {width} x {height}")
    else:
        print("Please provide OLED model")
        print("Currently supprted models are:")
        for entry in oled_mod:
            model, _, _ = oled_mod.get(entry)
            print(f"\t{model}")

        print("or provide resolution, like 128, 32")


if __name__ == "__main__":
    main()