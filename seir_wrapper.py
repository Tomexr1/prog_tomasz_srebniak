import argparse
from lista4 import plotseir


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', type=int, help='Wielkość populacji')
    parser.add_argument('-S0', type=int, help='Liczba osób zdrowych')
    parser.add_argument('-E0', type=int, help='Liczba osób w fazie inkubacji')
    parser.add_argument('-I0', type=int, help='Liczba osób zarażonych')
    parser.add_argument('-R0', type=int, help='Liczba osób wyzdrowiałych')
    parser.add_argument('-beta', type=float, help='Wskaźnik infekcji', default=1.34)
    parser.add_argument('-sigma', type=float, help='Wskaźnik inkubacji', default=0.19)
    parser.add_argument('-gamma', type=float, help='Wskaźnik wyzdrowień', default=0.34)
    args = parser.parse_args()
    # handling not given arguments
    if args.N is None:
        if args.S0 is None:  # N i S0 nie są podane
            sum_of_gotten_values = sum(arg for arg in (args.E0, args.I0, args.R0) if arg is not None)
            if sum_of_gotten_values != 0:
                args.N = 100 * sum_of_gotten_values
                args.S0 = args.N - sum_of_gotten_values
                # uzupełnienie brakujących wartości zerami
                args.E0, args.I0, args.R0 = (0 if arg is None else arg for arg in (args.E0, args.I0, args.R0))
            else:  # N, S0, E0, I0, R0 nie są podane
                args.N, args.S0, args.E0, args.I0, args.R0 = 1000, 999, 1, 0, 0
        else:  # S0 jest podane, N - nie
            sum_of_gotten_values = args.S0 + sum(arg for arg in (args.E0, args.I0, args.R0) if arg is not None)
            args.N = sum_of_gotten_values
            # uzupełnienie brakujących wartości zerami
            args.E0, args.I0, args.R0 = (0 if arg is None else arg for arg in (args.E0, args.I0, args.R0))
    elif args.S0 is None:  # N jest podane, ale S0 - nie
        sum_of_gotten_values = sum(arg for arg in (args.E0, args.I0, args.R0) if arg is not None)
        args.S0 = args.N - sum_of_gotten_values  # dopełnia S0 do N
        # uzupełnienie brakujących wartości zerami
        args.E0, args.I0, args.R0 = (0 if arg is None else arg for arg in (args.E0, args.I0, args.R0))
    else:  # N i S0 są podane
        sum_of_gotten_values = sum(arg for arg in (args.E0, args.I0, args.R0) if arg is not None)
        if sum_of_gotten_values + args.S0 == args.N:  # podane wartości sumują się do N
            # uzupełnienie brakujących wartości zerami
            args.E0, args.I0, args.R0 = (0 if arg is None else arg for arg in (args.E0, args.I0, args.R0))
        else:  # podane wartości nie sumują się do N
            difference = args.N - args.S0 - sum_of_gotten_values
            args.E0 = args.E0 if args.E0 is not None else difference
            sum_of_gotten_values = sum(arg for arg in (args.E0, args.I0, args.R0) if arg is not None)
            if sum_of_gotten_values + args.S0 == args.N:  # różnica wpisana do E0
                args.I0, args.R0 = (0 if arg is None else arg for arg in (args.I0, args.R0))
            elif sum_of_gotten_values + args.S0 != args.N:  # nadal nie sumują się do N
                args.I0 = args.I0 if args.I0 is not None else difference
                sum_of_gotten_values = sum(arg for arg in (args.E0, args.I0, args.R0) if arg is not None)
                if sum_of_gotten_values + args.S0 == args.N:  # różnica wpisana do I0
                    args.R0 = 0 if args.R0 is None else args.R0
                elif sum_of_gotten_values + args.S0 != args.N:  # nadal nie sumują się do N - wpisana do R0
                    args.R0 = difference
    #  rysowanie wykresu
    # print(args)
    plotseir(args.N, args.S0, args.E0, args.I0, args.R0, args.beta, args.sigma, args.gamma)
