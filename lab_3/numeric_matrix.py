def construct(m, n):

    result = list()

    for x in range(1, m+1):

        row = list()

        for y in range(1, n+1):

            row.append(x**y)
        result.append(row)
    return result


def main():


    m, n = map(int, input("Введите M N через пробел.\n").split(" "))

    result = construct(m, n)
    print(*result, sep="\n")


if __name__ == "__main__":
    main()
    


