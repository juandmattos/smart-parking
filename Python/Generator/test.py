import sys

print(sys.argv)

try:
    num = sys.argv[1]
    print(num)
except IndexError:
    print("El parametro no existe")
    num = "4"
