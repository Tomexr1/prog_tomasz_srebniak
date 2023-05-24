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


def get_selected_data(*args):
    """
    Funkcja pobierająca kursy walut z NBP API na podsawie wybranej daty i aktualizująca listy walut, kodów i kursów.

    :param args:
    :return: None
    """

    if len(selected_date.get()) > 9:
        new_date = selected_date.get()
        url = f"http://api.nbp.pl/api/exchangerates/tables/A/{new_date}/?format=json"
        try:
            r = requests.get(url)
            r = r.json()
            n_currencies = [rate["currency"] for rate in r[0]["rates"]]
            n_currencies.insert(0, "polski złoty")
            n_codes = [rate["code"] for rate in r[0]["rates"]]
            n_codes.insert(0, "PLN")
            n_mids = [rate["mid"] for rate in r[0]["rates"]]
            n_mids.insert(0, 1)
            n_date = r[0]["effectiveDate"]
            global currencies, codes, mids, date
            currencies = n_currencies
            codes = n_codes
            mids = n_mids
            date = n_date
            input_currency_list.config(values=codes)
            output_currency_list.config(values=codes)
            online_label.config(text="Online", fg="green")
            msg.config(text="Załadowano nowe kursy")
            msg.after(3000, lambda: msg.config(text=""))
            conversion()
        except requests.exceptions.ConnectionError:
            online_label.config(text="Offline", fg="red")
            cal.set_date(date)
            msg.config(text="Brak internetu")
            msg.after(3000, lambda: msg.config(text=""))
        except json.decoder.JSONDecodeError:
            cal.set_date(date)
            msg.config(text="Brak danych")
            msg.after(3000, lambda: msg.config(text=""))
            online_label.config(text="Online", fg="green")


def conversion(*args):
    """
    Funkcja przeliczająca waluty i aktualizująca etykiety z wynikami.

    :param args:
    :return: None
    """

    input_currency = var1.get()
    output_currency = var2.get()
    input_amount = var3.get()
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


def reload(*args):
    """
    Funkcja odświeżająca aplikację.

    :param args:
    :return: None
    """

    rates, is_online, n_date = get_data()
    n_currencies = [rate["currency"] for rate in rates]
    n_currencies.insert(0, "polski złoty")
    n_codes = [rate["code"] for rate in rates]
    n_codes.insert(0, "PLN")
    n_mids = [rate["mid"] for rate in rates]
    n_mids.insert(0, 1)
    global currencies, codes, mids, date
    currencies = n_currencies
    codes = n_codes
    mids = n_mids
    date = n_date
    cal.set_date(date)
    if is_online:
        online_label.config(text="Online", fg="green")
        msg.config(text="Załadowano nowe kursy")
        msg.after(3000, lambda: msg.config(text=""))
    else:
        online_label.config(text="Offline", fg="red")
        msg.config(text="Brak internetu")
        msg.after(3000, lambda: msg.config(text=""))
    conversion()


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
    root.rowconfigure(4, weight=1)
    root.rowconfigure(5, weight=2)
    root.rowconfigure(6, weight=1)
    style = ttk.Style(root)
    style.theme_use('clam')

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
    filemenu.add_command(label="Reload", command=reload, accelerator="CMD+R")
    menubar.add_cascade(label="File", menu=filemenu)
    root.bind('<Command-r>', reload)
    root.config(menu=menubar)

    # Label z informacją o stanie połączenia
    online_label = Label(root, text=online, fg="green" if is_online else "red")
    online_label.grid(row=0, column=0, sticky=NW)

    # Kalendarz
    lbl0 = Label(root, text="Dane z dnia: ")
    lbl0.configure(font=13)
    lbl0.grid(row=0, column=0, sticky=N)
    selected_date = StringVar()
    cal = DateEntry(root, selectmode='day', date_pattern='yyyy-mm-dd', year=int(date[:4]),
                    month=int(date[5:7]), day=int(date[8:]), textvariable=selected_date, locale='pl_PL')
    cal.grid(row=0, column=0, columnspan=2, sticky=N, pady=1)
    selected_date.trace("w", get_selected_data)
    msg = Message(root, text="", font=("Arial", 12), width=200)
    msg.grid(row=0, column=1, columnspan=2, sticky=NE, padx=2, pady=2)

    # Combobox z walutą początkową
    var1 = StringVar()
    lbl1 = Label(root, text="Waluta początkowa")
    lbl1.configure(font=13)
    lbl1.grid(row=1, column=0, sticky=W, padx=20)
    input_currency_list = ttk.Combobox(root, values=codes, textvariable=var1)
    input_currency_list.set("-")
    input_currency_list.grid(row=1, column=1)
    var1.trace("w", conversion)

    # Combobox z walutą końcową
    var2 = StringVar()
    lbl2 = Label(root, text="Waluta końcowa")
    lbl2.configure(font=13)
    lbl2.grid(row=2, column=0, sticky=W, padx=20)
    output_currency_list = ttk.Combobox(root, values=codes, textvariable=var2)
    output_currency_list.set("-")
    output_currency_list.grid(row=2, column=1)
    var2.trace("w", conversion)

    # Entry z kwotą początkową
    var3 = StringVar()
    lbl3 = Label(root, text="Kwota początkowa")
    lbl3.configure(font=13)
    lbl3.grid(row=3, column=0, sticky=W, padx=20)
    original_value_entry = Entry(root, textvariable=var3)
    original_value_entry.grid(row=3, column=1)
    var3.trace("w", conversion)

    # Label z kwotą końcową
    lbl4 = Label(root)
    lbl4.configure(font=13)
    lbl4.grid(row=4, column=0, sticky=W, padx=10, columnspan=2)

    output_value_entry = Label(root)
    output_value_entry.config(font=("Courier", 16, "bold"))
    output_value_entry.grid(row=5, column=0, sticky=W, padx=10, columnspan=2)

    # Przycisk do wyjścia
    btn = Button(root, text="Wyjście", command=quit)
    btn.grid(row=6, column=0, columnspan=2)

    root.mainloop()
