import sys


print("Nazwa wywołanego skryptu to", sys.argv[0])
if len(sys.argv) > 1:
    print("Argumenty wywołania:")
    for arg in sys.argv[1:]:
        print(arg)
else:
    print("Brak argumentów")