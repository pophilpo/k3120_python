def is_unique(string):

    seen = list()

    for char in string:
        if char in seen:
            return False
        seen.append(char)

    return True


def main():

    # Это вряд ли оптимальное решение, но в таких маленьких диапозонах работает быстро.
    # От самого маленького счастливого числа до самого большого.

    for number in range(1023, 9876 + 1):
        number = str(number)

        if is_unique(number):
            print(number, end=" ")


if __name__ == "__main__":
    main()
