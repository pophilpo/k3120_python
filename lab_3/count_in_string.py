def main():

    user_input = input("Введите строку\n")

    # Считает все ЦИФРЫ. Отрицательные и двухзначные ЧИСЛА будут считаться неправильно.
    numbers = [ int(num) for num in user_input if num.isdigit() ]

    print(sum(numbers))


if __name__ == "__main__":
    main()


