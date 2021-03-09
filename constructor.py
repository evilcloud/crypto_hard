import crypto_prices
import json


def get_direction(assets_prices):
    """Returns "▲" or "▼" (or X or _) for the prices relative to unit cost base from ucb.json

    Args:
        assets_prices (dict): {"SYM": price}

    Returns:
        dict: {"SYM": "▲" or "▼" or "_" for non-existent. "X" for error}
    """
    with open("venv/ucb.json") as f:
        unit_price = json.load(f)

    assets_dirs = {}
    # unit_price = {
    #     "BTC": 35964.79,
    #     "ETH": 156.85,
    # }
    for asset in assets_prices:
        up = unit_price.get(asset)
        if up:
            assets_dirs[asset] = "▲" if assets_prices[asset] > up else "▼"
        else:
            assets_dirs[asset] = "_" if assets_prices(asset) else "X"
    return assets_dirs


# def define_spaces(assets_prices):
#     """Determines the max line length based on line lenght of all prices

#     Args:
#         assets_prices (dict): {"SYM": price}

#     Returns:
#         max_space (int): number of max spaces (incl. separators)
#     """
#     prices = set()
#     asset_spaces = []
#     for asset in assets_prices:
#         prices.add(len(str(int(assets_prices[asset]))))
#     max_len = max(prices)
#     for asset in assets_prices:
#         asset_spaces[asset] = max_len - len(str(int(assets_prices[asset])))
#     return max(asset_spaces)


def construct_line(assets_prices):
    """constructs the printline

    Args:
        assets_prices (dict): {"SYM": price}

    Returns:
        list: lines ready to be used, printed
    """
    print(f"constructing line with {assets_prices}")
    assets_dirs = get_direction(assets_prices)

    def number():
        x = assets_prices[asset]
        return f"{int(x):,}" if x > 999 else f"{x:,.2f}"

    max_len = 0
    for asset in assets_prices:
        l = len(number())
        max_len = l if (l) > max_len else max_len

    lines = []
    for asset in assets_prices:
        lines.append(f"{asset} {number().rjust(max_len)} {assets_dirs[asset]}")
    return lines


# def test():
#     assets_prices = crypto_prices.from_coinmarketcap(["BTC", "ETH", "DOT", "Cardano"])
#     for line in construct_line(assets_prices):
#         print(line)


def main():
    print("Line constructor module")


if __name__ == "__main__":
    main()