#!/usr/bin/env python3

def parse_input(user_input):

    if user_input == "q":
        return "Exit"

    allowed_operations = [ "+", "-", "*", "/" ]

    split_input = user_input.split(" ")

    if len(split_input) != 3:
        return False

    x, operation, y = split_input

    if not x.isdigit() or not y.isdigit() or operation not in allowed_operations:
        return False

    return (float(x), float(y), operation)


def sum(x, y):
    return x + y

def diff(x, y):
    return x - y

def product(x, y):
    return x*y

def quotient(x, y):

    if y == 0:
        return "Err"
    return x / y


def main():

    input_method_message = "Формат ввода: x [+, -, *, /] y. Пример Ввода: 1 + 2; \n"
    print(input_method_message)

    while True:

        print("_"* 40 + "\n")
        user_input = input().strip()

        user_input = parse_input(user_input)

        if not user_input:
            print("Ошибка Ввода! \n")
            print(input_method_message)
            continue

        if user_input == "Exit":
            break

        x, y, operation = user_input

        if operation == "+":
            result = sum(x, y)
        elif operation == "-":
            result = diff(x, y)
        elif operation == "*":
            result = product(x, y)
        else:
            result = quotient(x, y)


        if result == "Err":
            print("Деление на ноль запрещено\n")
        else:
            print(result)


if __name__ == "__main__":
    main()
