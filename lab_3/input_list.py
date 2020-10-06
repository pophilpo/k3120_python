def read_list():
    
    user_input = list()
    print("Введите числа")

    while True:

        input_number = input()
        if not input_number.isdigit():
            break

        user_input.append(input_number)
    return user_input




def main():
    print(len(read_list()))


if __name__ == "__main__":
    main()


