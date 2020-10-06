def read_list():
    
    user_input = list()
    print("Введите числа")

    while True:

        input_number = input()
        if not input_number.isdigit():
            break

        user_input.append(int(input_number))
    return user_input



def main():

    input_list = read_list()

    mean_value = sum(input_list) / len(input_list)

    print(f"Среднее значение списка {mean_value}")


if __name__ == "__main__":
    main()



