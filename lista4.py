from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


def derivatives(y, t, N, beta, sigma, gamma):
    """
    Funkcja zwracająca pochodne dla każdej z zmiennych w modelu SEIR.

    :param y:
    :param t:
    :param N:
    :param beta:
    :param sigma:
    :param gamma:
    :return:
    """

    S, E, I, R = y
    dSdt = (-beta * S * I) / N
    dEdt = (beta * S * I) / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return dSdt, dEdt, dIdt, dRdt


def plotseir(N, S0, E0, I0, R0, beta, sigma, gamma):
    """
    Funkcja rysująca wykresy dla modelu SEIR.

    :param N:
    :param S0:
    :param E0:
    :param I0:
    :param R0:
    :param beta:
    :param sigma:
    :param gamma:
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
