def factorial(n):

    # 0! = 1
    if n <= 1:
        return 1
    
    return n*factorial(n-1)

def main():

    while True:
        
        try:
            n = int(input("Введите n\n"))

            if n < 0:
                print("Введите целое неотрицательное число\n")
                continue
            
            print(factorial(n))
            break


        except:
            print("Введите целое неотрицательное число\n")
            continue


if __name__ == "__main__":
    main()
