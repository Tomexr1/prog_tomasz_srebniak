"""
    Moduł z funkcją rysującą wykresy dla modelu SEIR.
"""

import sys
from lista4 import plotseir


if __name__ == '__main__':
    if len(sys.argv) < 9:
        print('Usage: python3 seir_wrapper.py N S0 E0 I0 R0 beta sigma gamma')
        exit(1)
    N, S0, E0, I0, R0 = map(int, sys.argv[1:6])
    beta, sigma, gamma = map(float, sys.argv[6:])
    plotseir(N, S0, I0, E0, R0, beta, sigma, gamma)
