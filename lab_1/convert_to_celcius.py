def convert_temperature(x):

    return (x-32)/1.8


def main():

    while True:

        user_input = input("Введите значение для конвертации\n")

        try:
            user_input = float(user_input)
            print(convert_temperature(user_input))
            break
        except ValueError:
            print("Введите действительное число\n")
            continue


if __name__ == "__main__":
    main()

