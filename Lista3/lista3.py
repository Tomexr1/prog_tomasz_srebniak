from datetime import datetime, date
import os
import shutil
import PyPDF2
import qrcode
import cv2
import requests
from bs4 import BeautifulSoup
import webbrowser
import pathlib


def backup(ext, directories, days=3, dst='/Users/tomasz/PycharmProjects/programowanie/'):
    """
    Tworzy kopię zapasową podanych plików o podanym rozszerzeniu, zapisuje w podanym katalogu.

    :param ext: (str) - rozszerzenie
    :param directories: (tuple or float or string) - katalogi do spakowania
    :param days: (float) - ile dni upłynęlo od ostatniej modyfikacji
    :param dst: (str) - katalog docelowy
    :return: None
    """

    if type(directories) != tuple and type(directories) != list:
        directories = (directories,)
    name = str(dst)+'Backup/copy-'+str(date.today())
    os.makedirs(name, exist_ok=True)
    for directory in directories:
        path = pathlib.Path(str(directory))
        for file in path.rglob('*'):
            # print(file)
            ts = os.path.getmtime(file)  # timestamp
            duration = datetime.now() - datetime.fromtimestamp(ts)  # timedelta
            duration_in_days = duration.total_seconds()/259200  # timedelta w dniach
            if duration_in_days < days and str(file).endswith(str(ext)):
                shutil.copy(file, name)


def endline_swapper(txtfiles):
    """
    Zamienia w podanych plikach końcówki linii na Windowsowe lub Unixowe.

    :param txtfiles: (tuple or float or string) - pliki do zmiany
    :return: None
    """

    if type(txtfiles) != tuple and type(txtfiles) != list:
        txtfiles = (txtfiles,)
    for file in txtfiles:
        with open(file, 'rb') as f:
            text = f.read()
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
            print(text)


def pdf_merg(files):
    """
    Łączy pliki pdf w jeden.

    :param files: (tuple or float or string) - pliki do połączenia
    :return: None
    """

    writer = PyPDF2.PdfWriter()
    if type(files) != tuple and type(files) != list:
        files = (files,)
    print(files)
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


def brackets_matching(expression):
    """
    Sprawdza czy nawiasy w podanym wyrażeniu są poprawnie sparowane.

    :param expression: (str) - wyrażenie do sprawdzenia
    :return: bool - czy nawiasy są poprawnie sparowane
    """

    stack = []
    for char in expression:
        if char == '(' or char == '[' or char == '{' or char == '<':
            if stack and char == stack[-1]:  # dwa nawiasy nie mogą być koło siebie!!
                return False
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
        elif char == '>':
            if not stack or stack[-1] != '<':
                return False
            else:  # stack[-1] == '<':
                stack.pop()
        else:
            continue
    return not stack


def wiki_article():
    """
    Pobiera z Wikipedii losowy artykuł i jeżeli jego tytuł spodoba się użytkownikowi, wyświetla go.

    :return: None
    """

    counter = 0
    while counter < 5:
        res = requests.get('https://en.wikipedia.org/wiki/Special:Random')
        bs4_object = BeautifulSoup(res.text, 'html.parser')
        url = bs4_object.select('link[rel="canonical"]')[0].get('href')
        title = bs4_object.select('h1')[0].getText()
        print('Czy chcesz przeczytać artykuł o ' + title + '?')
        if input('T/N: ').lower() == 't':
            webbrowser.open(url)
            break
        else: counter += 1
    return


if __name__ == "__main__":
    # backup('.txt', '/Users/tomasz/PycharmProjects/wstep_do_programowania')
    # pdf_merg(('test.pdf', 'test copy.pdf'))
    # endline_swapper('tekst.txt')
    # qrcode_generator('https://www.google.com')
    # print(qrcode_reader('qrcode.png'))
    # print(brackets_matching('()2+2*(3+4)[]{[{()gr}]seawf}'))
    # print(brackets_matching('()(())'))
    # wiki_article()
    # pdf_merg(("Duży_pdf 1-3.pdf", "Duży_pdf 4-6.pdf", "Duży_pdf 7-9.pdf", "Duży_pdf 10-12.pdf", "Duży_pdf 13-14.pdf"))
    pass
