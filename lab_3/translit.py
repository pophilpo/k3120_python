def main():
    
    # Данные две строки взяты из интернета
    symbols = ("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ", "abvgdeejzijklmnoprstufhzcss_y`euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y`EUA")

    map_dict = dict()
    map_dict[" "] = " "

    for russian_letter, eng_letter in zip(symbols[0], symbols[1]):

        if eng_letter == "_":
            map_dict[russian_letter] = ""
            continue

        map_dict[russian_letter] = eng_letter


    
    user_input = input("Введите строку\n")

    result = list()

    for char in user_input:
        result.append(map_dict[char])

    result = "".join(result)
    print(result)


if __name__ == "__main__":
    main()


