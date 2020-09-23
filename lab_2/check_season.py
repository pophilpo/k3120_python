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

        if month_number in (12, 1, 2):
            print("Зима")
        elif month_number in (3, 4, 5):
            print("Весна")
        elif month_number in (6, 7, 8):
            print("Лето")
        else:
            print("Осень")
        break


if __name__ == "__main__":
    main()
