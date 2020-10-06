def main():

    alphabet = "AБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    # ['A', 'Б', ...]
    alphabet = list(alphabet)

    result = list()

    for i in range(0, 33):

        result.append(alphabet[:i+1])

    print(*result, sep="\n")



if __name__ == "__main__":
    main()

