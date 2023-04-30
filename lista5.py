from tkinter import *
from tkinter import ttk
import json
import requests
from tkcalendar import DateEntry


def get_data():
    """
    Funkcja pobierająca kursy walut z NBP API lub wczytująca z pliku kursy z ostatniego pobrania.
    :return: rates - lista słowników currency, code, mid
    """

    url = "http://api.nbp.pl/api/exchangerates/tables/A/?format=json"
    connection = False
    try:
        r = requests.get(url)
        connection = True
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


def get_selected_date():
    """
    Funkcja pobierająca datę z kalendarza.
    :return: date - wybrana data
    """
    pass
    # date = selected_date.get()
    # print(date)


def przewalutowanie():
    """
    Funkcja przeliczająca waluty.

    :return: output_value - przeliczona wartość
    """
    input_currency = input_currency_list.get()
    output_currency = output_currency_list.get()
    input_amount = original_value_entry.get()
    input_currency_str = input_currency
    output_currency_str = output_currency
    output = ("", "")

    try:
        input_amount = float(input_amount)
        if input_currency != "-" and output_currency != "-":
            for i in range(len(codes)):
                if codes[i] == input_currency:
                    input_currency = mids[i]
                    input_currency_str = currencies[i]
                if codes[i] == output_currency:
                    output_currency = mids[i]
                    output_currency_str = currencies[i]
            output_amount = input_amount * float(input_currency) / float(output_currency)
            output = (f"{input_amount} {input_currency_str} to", f"{output_amount:.2f} {output_currency_str}")
    except ValueError:
        pass

    lbl4.config(text=output[0])
    output_value_entry.config(text=output[1])
    root.after(1000, przewalutowanie)


def refresh():
    pass
    # rates = get_data()[0]
    # currencies = [rate["currency"] for rate in rates]
    # currencies.insert(0, "polski złoty")
    # codes = [rate["code"] for rate in rates]
    # codes.insert(0, "PLN")
    # mids = [rate["mid"] for rate in rates]
    # mids.insert(0, 1)
    # online = "Online" if get_data()[1] else "Offline"
    # # Label z informacją o stanie połączenia
    # online_label = Label(root, text=online, fg="green" if get_data()[1] else "red")
    # online_label.configure(font="underline")
    # online_label.grid(row=0, column=0, sticky=NW)
    # date_label = Label(root, text=f"Dane z dnia: {get_data()[2]}")
    # # date_label.pack(side=LEFT, anchor=NW)
    # date_label.grid(row=0, column=0, sticky=NE)


# application calculating currency exchange based on NBP API
if __name__ == "__main__":
    root = Tk()
    root.geometry('450x300+400+400')
    root.title("Przelicznik walut")
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=2)
    root.rowconfigure(2, weight=2)
    root.rowconfigure(3, weight=2)
    root.rowconfigure(4, weight=3)
    root.rowconfigure(5, weight=1)

    # ładowanie danych
    rates, is_online, date = get_data()
    currencies = [rate["currency"] for rate in rates]
    currencies.insert(0, "polski złoty")
    codes = [rate["code"] for rate in rates]
    codes.insert(0, "PLN")
    mids = [rate["mid"] for rate in rates]
    mids.insert(0, 1)
    online = "Online" if is_online else "Offline"


    # Menu bar
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Refresh", command=refresh, accelerator="CMD+R")
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    # Label z informacją o stanie połączenia
    online_label = Label(root, text=online, fg="green" if is_online else "red")
    online_label.grid(row=0, column=0, sticky=NW)

    # Kalendarz
    # selected_date = StringVar()
    # cal = DateEntry(root, selectmode='day',date_pattern='yyyy-mm-dd',
    #                 year=int(date[:4]), month=int(date[5:7]), day=int(date[8:]), textvariable=selected_date)
    # cal.grid(row=0, column=0, sticky=NE)
    # selected_date.trace("w", get_selected_date)

    date_label = Label(root, text=f"Dane z dnia: {get_data()[2]}")
    date_label.grid(row=0, column=0, sticky=NE, columnspan=2)

    # Combobox z walutą początkową
    lbl1 = Label(root, text="Waluta początkowa")
    lbl1.configure(font=13)
    lbl1.grid(row=1, column=0, sticky=W, padx=20)
    input_currency_list = ttk.Combobox(root, values=codes)
    input_currency_list.set("-")
    input_currency_list.grid(row=1, column=1)

    # Combobox z walutą końcową
    lbl2 = Label(root, text="Waluta końcowa")
    lbl2.configure(font=13)
    lbl2.grid(row=2, column=0, sticky=W, padx=20)
    output_currency_list = ttk.Combobox(root, values=codes)
    output_currency_list.set("-")
    output_currency_list.grid(row=2, column=1)

    # Entry z kwotą początkową
    lbl3 = Label(root, text="Kwota początkowa")
    lbl3.configure(font=13)
    lbl3.grid(row=3, column=0, sticky=W, padx=20)
    original_value_entry = Entry(root)
    original_value_entry.grid(row=3, column=1)

    # Label z kwotą końcową
    lbl4 = Label(root)
    lbl4.configure(font=13)
    lbl4.grid(row=4, column=0, sticky=W, padx=10)
    output_value_entry = Label(root)
    output_value_entry.config(font=("Courier", 16, "bold"))
    output_value_entry.grid(row=4, column=1, sticky=W)
    # changed=0

    # Przycisk do wyjścia
    btn = Button(root, text="Wyjście", command=quit)
    btn.grid(row=5, column=0, columnspan=2)

    przewalutowanie()

    root.mainloop()
