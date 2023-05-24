from random import uniform


class Vector:
    """
    Klasa reprezentująca wektory na płaszczyźnie.

    ...

    Atrybuty
    --------
    size : int
        rozmiar wektora
    values : list
          lista wartości wektora

    Metody
    ------
    __init__(size=3)
        inicjalizuje wektor o podanym rozmiarze
    generate_values()
        generuje losowe wartości wektora
    load_values(vals)
        wczytuje wartości wektora z listy
    __add__(other)
        dodaje wektory
    __sub__(other)
        odejmuje wektory
    __mul__(scalar)
        mnoży wektor przez skalar
    __rmul__(scalar)
        mnoży wektor przez skalar
    leng()
        zwraca długość wektora
    sum()
        zwraca sumę wartości wektora
    scalar_product(other)
        zwraca iloczyn skalarny wektora z podanym wektorem
    __str__()
        zwraca string z wartościami wektora
    __getitem__(item)
        zwraca wartość wektora o podanym indeksie
    __contains__(item)
        sprawdza czy wektor zawiera podaną wartość
    """

    def __init__(self, size=3):
        """
        Tworzy wektor o podanym rozmiarze i wartościach równych 0.

        :param size: int - rozmiar wektora
        :return: None
        """
        self.size = size
        self.values = []
        for _ in range(size):
            self.values.append(0)

    def generate_values(self):
        """
        Generuje losowe wartości dla wektora.

        :return: None
        """

        self.values = [uniform(1, 10) for _ in range(self.size)]

    def load_values(self, vals):
        """
        Wczytuje wartości wektora z listy.

        :param vals: list - lista wartości wektora
        :return: None
        :raises TypeError: jeśli podana lista nie ma odpowiedniej długości
        """

        if type(vals) == list and len(vals) == self.size:
            for i in range(self.size):
                self.values[i] = vals[i]
        else:
            raise TypeError("Nie podano listy lub podana lista nie ma odpowiedniej długości.")

    def __add__(self, other):
        """
        Dodaje wektory.

        :param other: Vector - wektor do dodania
        :return: Vector
        :raises ValueError: jeśli wektory mają różne rozmiary
        """

        if self.size != other.size:
            raise ValueError("Wektory mają różne rozmiary.")
        else:
            self.load_values([self.values[i]+other.values[i] for i in range(self.size)])
            return self

    def __sub__(self, other):
        """
        Odejmuje wektory.

        :param other: Vector - wektor do odjęcia
        :return: Vector
        :raises ValueError: jeśli wektory mają różne rozmiary
        """

        if self.size != other.size:
            raise ValueError("Wektory mają różne rozmiary.")
        else:
            self.load_values([self.values[i]-other.values[i] for i in range(self.size)])
            return self

    def __mul__(self, scalar):
        """
        Mnoży wektor przez skalar.

        :param scalar:  int or float - skalar do pomnożenia
        :return: Vector
        """

        if type(scalar) != int and type(scalar) != float:
            raise TypeError
        else:
            self.load_values([self.values[i]*scalar for i in range(self.size)])
            return self

    def __rmul__(self, scalar):
        """
        Mnoży wektor przez skalar.

        :param scalar:  int or float - skalar do pomnożenia
        :return: Vector
        """

        if type(scalar) != int and type(scalar) != float:
            raise TypeError
        else:
            self.load_values([self.values[i]*scalar for i in range(self.size)])
            return self

    def length(self):
        """
        Zwraca długość wektora.

        :return: length (float)
        """

        return sum([self.values[i]**2 for i in range(self.size)])**0.5

    def sum(self):
        """
        Zwraca sumę wartości wektora.

        :return: sum (int or float)
        """

        return sum(self.values)

    def scalar_product(self, other):
        """
        Zwraca iloczyn skalarny wektora z podanym wektorem.

        :param other: Vector - wektor do pomnożenia
        :return: Vector
        :raises ValueError: jeśli wektory mają różne rozmiary
        """

        if self.size != other.size:
            raise ValueError
        else:
            return sum([self.values[i]*other.values[i] for i in range(self.size)])

    def __str__(self):
        """
        Zwraca string z wartościami wektora.

        :return: str
        """

        return str(self.values)

    def __getitem__(self, index):
        """
        Zwraca wartość wektora w podanym indeksie.

        :param index: int - indeks
        :return: value (int or float)
        """

        return self.values[index]

    def __contains__(self, value):
        """
        Sprawdza czy wektor zawiera podaną wartość.

        :param value: int or float - wartość szukana
        :return: bool
        """

        return value in self.values


if __name__ == "__main__":
    wek1 = Vector()
    wek2 = Vector()
    print(f'Wartości wektorów wek1 i wek2: {wek1.values}, {wek2.values}')
    wek1.generate_values()
    print(f'Wek1 po wygenerowaniu nowych wartości: {wek1}')
    wek2.load_values([1, 2, 3])
    print(f'Wek2 po wczytaniu nowych wartości: {wek2}')
    print(f'Wek1 po dodaniu wek2: {wek1+wek2}')
    print(f'Wek1 po odjęciu wek2: {wek1-wek2}')
    print(f'Wek1 pomnożony przez 2: {wek1*2}')
    print(f'Długość wek1: {wek1.length()}')
    print(f'Suma wartości wek1: {wek1.sum()}')
    print(f'Iloczyn skalarny wek1 i wek2: {wek1.scalar_product(wek2)}')
    print(f'Wartość wek1 w indeksie 1: {wek1[1]}')
    print(f'Czy wek2 zawiera wartość 1: {1 in wek2}. Czy wek2 zawiera wartość 5: {5 in wek2}')
