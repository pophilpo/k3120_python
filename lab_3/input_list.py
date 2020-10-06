def main():

    user_input = list()
    print("Введите числа")

    while True:

        input_number = input()
        if not input_number.isdigit():
            break

        user_input.append(input_number)

    print(len(user_input))


if __name__ == "__main__":
    main()


