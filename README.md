# OLED crypto tracker on RPi

A massive mess of a hacked lines from all over the place that somehow gets the I2C interfaced OLED working on a Raspberry Pi Zero working with hardcoded data. Currently supported data providers are:

- CoinGecko
- CoinmarketCap

Prerequisites:

- a file `settings.json` defines the assets and intervals between API requests. Changes during runtime will be loaded with the next cycle:
```json
{
    "assets": [
        "BTC",
        "ETH",
        "DOT"
    ]
}
```

- in a directory `venv` make a file `keys.json` and do this for exchange keys:
```json
{
    "coinmarketcap": {
        "key": "some-super-secret-key",
        "interval": 900
    }
}
```
- if you want to get the directions for unit base price, in the directory `venv` make a file `ucb.json` and do something like this:
```json
{
    "BTC": 3000,
    "ETH": 1000,
    "DOT": 20
}
```
