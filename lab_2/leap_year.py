def leap_year_check(x):

    if x % 4 == 0 and x % 100 != 0 or x % 400 == 0:
        print("Данный год является високосным\n")
    else:
        print("Данный год НE является високосным\n")


def main():

    while True:
        try:
            year = int(input("Введите год\n"))

            if year < 0:
                print("Введите целое ПОЛОЖИТЕЛЬНОЕ число\n")
                continue

            leap_year_check(year)
            break

        except ValueError:
            print("Введите целое ПОЛОЖИТЕЛЬНОЕ число\n")
            continue

if __name__ == "__main__":
    main()
