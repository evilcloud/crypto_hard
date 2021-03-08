# Module dealing with crypto prices retreival
# from different exchanges.
# The data with the keys is stored in /venv/keys.json
# Schema: {"exchange": {"key": str, "interval": int}}

import requests
import json


def get_key(exchange):
    """Retrieves API keys from venv/keys.json

    Args:
        exchange (str): exchange ID as set in keys.json

    Returns:
        str: exchange key
    """
    with open("venv/keys.json") as f:
        data = json.load(f)
    return data[exchange]["key"]


def from_coinmarketcap(assets: list):
    """Retrieves prices from Coinmarket Cap API

    Args:
        assets (list): list of desired asset symbols capitalised
                        or currency name (exchange specific case sensitivfity!).
                        Single string is also acceptable

    Returns:
        dict: {[ASSET: price]}
    """

    # assets = [assets]
    prices = {}
    if not isinstance(assets, list):
        assets = [assets]

    api_key = get_key("coinmarketcap")
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": api_key}
    try:
        response = requests.get(url, headers=headers)
        resp = response.json()
    except Exception as err:
        print(err)
        return prices

    for entry in resp["data"]:
        if entry["symbol"] in (assets) or entry["name"] in (assets):
            prices[entry["symbol"]] = entry["quote"]["USD"]["price"]

    return prices


def main():
    if __name__ == "__main__":
        print("Crypto prices retrieval module")