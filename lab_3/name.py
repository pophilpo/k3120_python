def main():



    surname, name, patronymic = input("Введите данные в формате: ФАМИЛИЯ ИМЯ ОТЧЕСТВО.\n").strip().split(" ")

    result = surname + " " + name[0] + "." + patronymic[0] + "."
    print(result)


if __name__ == "__main__":
    main()
