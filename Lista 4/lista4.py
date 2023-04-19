"""
    Moduł zawierający funkcje do modelowania epidemii zgodnie z modelem SEIR.
"""

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


def derivatives(y, t, N, beta, sigma, gamma):
    """
    Funkcja zwracająca pochodne dla każdej z zmiennych w modelu SEIR.

    :param y: lista z wartościami zmiennych w danym momencie czasu
    :param t: czas trwania epidemii
    :param N: liczba ludności
    :param beta: wskaźnik infekcji
    :param sigma: wskaźnik inkubacji
    :param gamma: wskaźnik wyzdrowień
    :return: dsdt, dedt, didt, drdt (tuple) - pochodne dla każdej z zmiennych
    """

    S, E, I, R = y
    dSdt = (-beta * S * I) / N
    dEdt = (beta * S * I) / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return dSdt, dEdt, dIdt, dRdt


def plotseir(N, S0, E0, I0, R0, beta, sigma, gamma):
    """
    Funkcja rysująca wykresy dla modelu SEIR z użyciem funkcji derivatives.

    :param N: liczba ludności
    :param S0: liczba osób narażonych na zarażenie
    :param E0: liczba osób w fazie inkubacji
    :param I0: liczba osób zarażonych
    :param R0: liczba osób wyzdrowiałych
    :param beta: wskaźnik infekcji
    :param sigma: wskaźnik inkubacji
    :param gamma: wskaźnik wyzdrowień
    :raises ValueError: jeśli wartości początkowe nie są poprawne
    :return: None
    """

    if N != S0 + E0 + I0 + R0 or N < 0:
        raise ValueError('Niepoprawne wartości początkowe')
    y0 = S0, E0, I0, R0
    for i in y0:
        if i < 0:
            raise ValueError('Niepoprawne wartości początkowe')

    integrated = odeint(derivatives, y0, np.linspace(0, 100, 100), args=(N, beta, sigma, gamma))
    plt.plot(integrated,
             label=(f'Susceptible, S0 = {S0}', f'Exposed, E0 = {E0}',f'Infectious, I0 = {I0}',
                    f'Recovered, R0 = {R0}')
             )
    plt.title('Przebieg epidemii zgodnie z modelem SEIR')
    plt.xlabel('Czas (dni)')
    plt.ylabel('Liczba ludności')
    plt.legend()
    plt.show()


def seir_vals(N, S0, E0, I0, R0, beta, sigma, gamma, t):
    """
    Funkcja zwracająca wartości dla modelu SEIR z użyciem funkcji derivatives.

    :param N: liczba ludności
    :param S0: liczba osób narażonych na zarażenie
    :param E0: liczba osób w fazie inkubacji
    :param I0: liczba osób zarażonych
    :param R0: liczba osób wyzdrowiałych
    :param beta: wskaźnik infekcji
    :param sigma: wskaźnik inkubacji
    :param gamma: wskaźnik wyzdrowień
    :param t: czas trwania epidemii
    :raises ValueError: jeśli wartości początkowe są niepoprawne
    :return: integrated (tuple): wartości dla każdej z zmiennych w modelu SEIR
    """

    if N != S0 + E0 + I0 + R0 or N < 0:
        raise ValueError('Niepoprawne wartości początkowe')
    y0 = S0, E0, I0, R0
    for i in y0:
        if i < 0:
            raise ValueError('Niepoprawne wartości początkowe')

    integrated = odeint(derivatives, y0, np.linspace(0, t, t), args=(N, beta, sigma, gamma))
    return integrated
