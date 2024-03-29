from PIL import Image, ImageDraw
from string import ascii_lowercase, ascii_uppercase, punctuation, digits
from random import choice
import zipfile
from datetime import date
import PyPDF2
import os
import pathlib


def zad1(length=8, characters=''):
    """
    Generuje losowe hasło o podanej długości znaków(domyślnie 8) złożone z podanych znaków.

    :param length: (int) - długość hasła
    :param characters: (str) - znaki do wykorzystania
    :return: None
    """

    if characters == '':
        characters = ascii_lowercase + ascii_uppercase + punctuation + digits
    password = ''
    for _ in range(length):
        password += choice(characters)
    return password


def zad2(name, size_of_miniature, new_name):
    """
    Tworzy miniaturę zdjęcia o podanej nazwie i rozmiarze, zapisuje ją pod nową nazwą.

    :param name: (str) - nazwa/ścieżka pliku do otwarcia
    :param size_of_miniature: (list or tuple) - rozmiar miniatury
    :param new_name: (str) - nazwa/ścieżka pliku do zapisu
    :return: None
    """

    img = Image.open(name)
    img.thumbnail(size_of_miniature)
    if not img.mode == 'RGB':
        img = img.convert('RGB')
    img.save(new_name)


def zad3(directories, destination=''):
    """
    Tworzy archiwa zip z podanych katalogów i zapisuje je w podanym katalogu.

    :param directories: (tuple or float or string) - katalogi do spakowania
    :param destination: (str) - katalog do zapisu archiwów
    :return: None
    """

    if destination == '':
        destination = os.getcwd()
    if type(directories) != (tuple and list):
        directories = (directories,)
    for directory in directories:
        with zipfile.ZipFile(str(destination) + '/' + str((date.today())) + ' ' + str(directory) + '.zip', 'w')\
                as zip_file:  # tworzy obiekt zip_file dla każdego podanego katalogu
            path = pathlib.Path(str(directory))
            for file in path.rglob('*'):
                zip_file.write(file)


def zad4(file_name, number_of_pages):
    """
    Rozdziela plik pdf na mniejsze pliki o podanej liczbie stron.

    :param file_name: (str) - nazwa/ścieżka pliku do otwarcia
    :param number_of_pages: (int) - liczba stron w podzielonych plikach
    :return: None
    """

    reader = PyPDF2.PdfReader(file_name)
    page_count = 0
    while page_count < len(reader.pages):
        if page_count + number_of_pages <= len(reader.pages):
            writer = PyPDF2.PdfWriter()
            writer.append(reader, pages=(page_count, page_count + number_of_pages))
            writer.write('Duży_pdf ' + str(page_count+1) + '-' + str(page_count+number_of_pages) + '.pdf')
            writer.close()
        else:
            writer = PyPDF2.PdfWriter()
            writer.append(reader, pages=(page_count, len(reader.pages)))
            writer.write('Duży_pdf ' + str(page_count+1) + '-' + str(len(reader.pages)) + '.pdf')
            writer.close()
        page_count += number_of_pages


def zad5(name, text):
    """
    Dodaje znak wodny do zdjęcia.

    :param name: (str) - nazwa/ścieżka zdjęcia
    :param text: (str) - teskt znaku wodnego
    :return: None
    """

    img = Image.open(name)
    width, height = img.size
    watermark = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # tworzy obrazek o rozmiarach zdjęcia
    watermark_draw = ImageDraw.Draw(watermark)  # inicjalizuje obiekt do rysowania na obrazku watermark
    watermark_draw.text((width / 2, height / 2), text, fill=(0, 0, 0, 128))  # rysuje tekst na obrazku watermark na
    # podanej pozycji
    watermark = watermark.rotate(45)
    img.paste(watermark, (0, 0), mask=watermark)
    img.save('watermarked_' + name)


def zad6(expression):
    """
    Wykonuje podane działanie i wypisuje je w słupku.

    :param expression: str - działanie do wykonania
    :return: None
    :raises ValueError: jeśli podano nieprawidłowy operator
    """

    operators = ['+', '-', '*', '/']
    left, right, result, operator = '', '', '', ''
    for operator in operators:
        if operator in expression:
            left, right = expression.split(operator)
            if operator == '+':
                result = int(left) + int(right)
            elif operator == '-':
                result = int(left) - int(right)
            elif operator == '*':
                result = int(left) * int(right)
            elif operator == '/':
                result = int(left) / int(right)
            break
    if result == '':
        raise ValueError('Nieprawidłowy operator')
    indentation = max(len(left), len(right), len(str(result))) + 2
    print(' ' * (indentation - len(left)) + left)
    print(operator + ' ' * (indentation - len(right) - 1) + right)
    print('-' * indentation)
    print(' ' * (indentation - len(str(result))) + str(result))


def main():
    # print(zad1(9, characters='ab'))
    # zad2("discs_list_circles.png", (100, 100), 'miniature.jpg')
    # zad3(['abab', 'cdcd'], destination='/Users/tomasz/PycharmProjects')
    zad4('test.pdf', 3)
    # zad5('discs_list_circles.png', 'watermark')
    # zad6('22000000-1')
    pass


main()
