def main():

    name = input("Введите имя\n")

    age = input("Введите возраст\n")

    sex = input("Введите пол в формате муж\жен\n")

    checklist = ["муж", "жен"]

    age_checklist = [2,3,4]



    try:
        age = int(age)

    except ValueError:
        print("Неверно введены данные. Возраст должен быть целым числом >= 0. Пол в формате муж\жен\n")

    if age < 0 or sex not in checklist:
        
        print("Неверно введены данные. Возраст должен быть целым числом >= 0. Пол в формате муж\жен\n")

    else:

        if sex == "муж":
            prefix_1 = "Его"
            prefix_2 = "Ему"

        else:
            prefix_1 = "Её"
            prefix_2 = "Ей"

        # Сам придумал какой то странный случай.
        if age == 0:
            age_string = "полных лет."

        elif age >=5 and age <=20:
            age_string = "лет."

        # Если возраст заканчивается на [2, 3, 4] - "года", если на 1 - "год", иначе - "лет".
        else:
            if age % 10 in age_checklist:
                age_string = "года."
            elif age % 10 == 1:
                age_string = "год."
            else:
                age_string = "лет."

        result = f"{prefix_1} зовут {name}. {prefix_2} {age} {age_string}"
        print(result)


if __name__ == "__main__":
    main()

