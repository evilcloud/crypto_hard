import requests

url = "https://community-bitcointy.p.rapidapi.com/convert/10/USD"

headers = {
    "x-rapidapi-key": "c16a162c86msh139e25e10ddaa5fp11fc9ajsnea2003a619ee",
    "x-rapidapi-host": "community-bitcointy.p.rapidapi.com",
}

response = requests.request("GET", url, headers=headers)

print(response.text)