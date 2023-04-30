from tkinter import *
from tkinter import ttk
import json
import requests


# funkcja pobierjąca nowego jsona lub otwierająca istniejący plik i wczytująca kursy
def get_data():
    url = "http://api.nbp.pl/api/exchangerates/tables/A/?format=json"
    connection = 0
    try:
        r = requests.get(url)
        connection = 1
        r = r.json()
        with open("kursy.json", 'w') as f:
            json.dump(r, f)
        rates = r[0]["rates"]  # 33 kursy - lista słowników curr, code, mid
        date = r[0]["effectiveDate"]
    except requests.exceptions.ConnectionError:
        with open("kursy.json", 'r') as f:
            data = json.load(f)
            rates = data[0]["rates"]
            date = data[0]["effectiveDate"]
    return rates, connection, date


rates = get_data()[1]
print(rates)
# print(rates)
# print(rates[i]["currency"] for i in range(len(rates)))
# print(rates[0]["currency"])
# print(rates[i]["currency"] for i in range(1,2))
# print(range(len(rates)))
# currncies = [rate["currency"] for rate in rates]
# print(currncies)