from datetime import datetime, date
import os
import shutil
import PyPDF2
import qrcode
import cv2
import requests
from bs4 import BeautifulSoup
import webbrowser


def backup(ext, directories):
    """
    Tworzy kopię zapasową podanych katalogów.

    :param ext: (str) - rozszerzenie
    :param directories: (tuple or float or string) - katalogi do spakowania
    :return: None
    """

    if type(directories) != (tuple and list):
        directories = (directories,)
    name = '/Users/tomasz/PycharmProjects/programowanie/Backup/copy-'+str(date.today())
    os.makedirs(name, exist_ok=True)
    for directory in directories:
        for file in os.listdir(str(directory)):
            ts = os.path.getmtime(file)  # timestamp
            duration = datetime.now() - datetime.fromtimestamp(ts)  # timedelta
            duration_in_days = duration.total_seconds()/259200  # timedelta w dniach
            if duration_in_days < 3 and str(file).endswith(str(ext)):
                shutil.copy(file, name)


def endline_swapper(txtfiles):
    """
    Zamienia w podanych plikach końcówki linii na Windowsowe lub Unixowe.

    :param txtfiles: (tuple or float or string) - pliki do zmiany
    :return: None
    """

    if type(txtfiles) != (tuple and list):
        txtfiles = (txtfiles,)
    for file in txtfiles:
        with open(file, 'rb') as f:
            text = f.read()
            print(text)
            if b'\r\n' in text:  # Windows
                rplc = (b'\r\n', b'\n')
            elif b'\n' in text:  # Unix
                rplc = (b'\n', b'\r\n')
            else:
                print('Niepoprawny plik')
                return
            text = text.replace(rplc[0], rplc[1])
        with open(file, 'wb') as f:
            f.write(text)


def pdf_merg(files):
    """
    Łączy pliki pdf w jeden.

    :param files: (tuple or float or string) - pliki do połączenia
    :return: None
    """

    writer = PyPDF2.PdfWriter()
    if type(files) != (tuple and list):
        files = (files,)
    for file in files:
        writer.append(PyPDF2.PdfReader(file))
    writer.write('merged.pdf')
    writer.close()


def qrcode_generator(url):
    """
    Tworzy kod QR z podanego adresu URL.

    :param url: (str) - adres URL
    :return: None
    """

    img = qrcode.make(url)
    img.save('qrcode.png')


def qrcode_reader(img):
    """
    Odczytuje kod QR z podanego obrazka.

    :param img: (str) - nazwa pliku z obrazkiem
    :return:   str - odczytany kod QR
    """

    image = cv2.imread(img)
    detector = cv2.QRCodeDetector()
    value, points, straight_qrcode = detector.detectAndDecode(image)
    return value


def brackets_matcher(expression):
    """
    Sprawdza czy nawiasy w podanym wyrażeniu są poprawnie sparowane.

    :param expression: (str) - wyrażenie do sprawdzenia
    :return: bool - czy nawiasy są poprawnie sparowane
    """

    stack = []
    for char in expression:
        if char == '(' or char == '[' or char == '{':
            stack.append(char)
        elif char == ')':
            if not stack or stack[-1] != '(':
                return False
            else:  # stack[-1] == '(':
                stack.pop()
        elif char == ']':
            if not stack or stack[-1] != '[':
                return False
            else:  # stack[-1] == '[':
                stack.pop()
        elif char == '}':
            if not stack or stack[-1] != '{':
                return False
            else:  # stack[-1] == '{':
                stack.pop()
        else:
            continue
    return not stack


def wiki_article():
    """
    Pobiera z Wikipedii losowy artykuł i jeżeli jego tytuł spodoba się użytkownikowi, wyświetla go.

    :return: None
    """

    res = requests.get('https://en.wikipedia.org/wiki/Special:Random')
    bs4_object = BeautifulSoup(res.text, 'html.parser')
    url = bs4_object.select('link[rel="canonical"]')[0].get('href')
    title = bs4_object.select('h1')[0].getText()
    print('Czy chcesz przeczytać artykuł o ' + title + '?')
    if input('T/N: ').lower() == 't':
        webbrowser.open(url)


if __name__ == "__main__":
    # backup('.py', '/Users/tomasz/PycharmProjects/programowanie')
    # pdf_merg(('test.pdf', 'test copy.pdf'))
    # endline_swapper('textfile.txt')
    # qrcode_generator('https://www.google.com')
    # print(qrcode_reader('qrcode.png'))
    # print(brackets_matcher('2+2*(3+4)[]{[{()gr}]seawf}'))
    # wiki_article()
    pass
