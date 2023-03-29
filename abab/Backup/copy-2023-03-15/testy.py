def zad6(expression):
    """
    Wykonuje podane działanie i wypisuje je w słupku.

    :param expression: str - działanie do wykonania
    :return: None
    :raises ValueError: jeśli podano nieprawidłowy operator
    """

    operators = ['+', '-', '*', '/']
    left, right, result, operator = ' ', ' ', ' ', ' '
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
    if result == ' ':
        raise ValueError('Nieprawidłowy operator')
    indentation = max(len(left), len(right), len(str(result))) + 2
    print(' ' * (indentation - len(left)) + left)
    print(operator + ' ' * (indentation - len(right) - 1) + right)
    print('-' * indentation)
    print(' ' * (indentation - len(str(result))) + str(result))

zad6('312')