def main():

    while True:

        month_number = input("Введите номер месяца \n")

        try:
            month_number = int(month_number)
        except ValueError:
            print("Введите целое число от 1 до 12")
            continue

        if month_number <= 0 or month_number > 12:
            print("Введите целое число от 1 до 12")
            continue

        if month_number == 12 or month_number == 1 or month_number == 2:
            print("Зима")
        elif month_number == 3 or month_number == 4 or month_number == 5:
            print("Весна")
        elif month_number == 6 or month_number == 7 or month_number == 8:
            print("Лето")
        else:
            print("Осень")
        break


if __name__ == "__main__":
    main()




