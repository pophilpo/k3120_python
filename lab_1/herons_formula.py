def heron(a, b, c):

    p = (a + b + c) / 2
    s = (p * (p - a) * (p - b) * (p - c)) ** (0.5)

    return s


def main():

    while True:

        try:

            a, b, c = map(
                float, input("Введите стороны треугольника через пробел\n").split(" ")
            )

            # Очень некрасиво
            # Проверяю все ли стороны положительны и возможен ли такой треугольник вовсе.
            if a > 0 and b > 0 and c > 0 and c < a + b and b < a + c and a < c + b:
                print(heron(a, b, c))
                break

        except ValueError:
            pass

        print(
            "Введие три ПОЛОЖИТЕЛЬНЫХ действительных числа при которых выполняется НЕРАВЕНСТВО ТРЕУГОЛЬНИКА"
        )


if __name__ == "__main__":
    main()
