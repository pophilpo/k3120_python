
def print_primes(n):

    for number in range(n+1):

        if is_prime(number):
            print(number, end=" ")



def is_prime(n):

    if n <= 1:
        return False

    elif n <= 3:

        return True
    
    # Проверять на делимость можно до квадратного корня n.
    end = int(n ** 0.5) + 1

    for i in range(2, end):
        if n % i == 0:
            return False

    return True


def main():

    while True:

        try:
            n = int(input("Введите n\n"))
            print_primes(n)
            break

            if n < 0:
                print("Введите натуральное число\n")
                continue

        except:
            print("Введите натуральное число\n")
            continue


if __name__ == "__main__":
    main()
