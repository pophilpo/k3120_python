#!/usr/bin/env python


def fib_recursive(n):

    if n <= 1:
        return n
    return(fib_recursive(n-1) + fib_recursive(n-2))


def fib_iterative(n):

    x, y = 0, 1

    for i in range(0, n):

        x, y = y, x + y

    return x


def main():

    n = 10

    print(fib_recursive(n))
    print(fib_iterative(n))


if __name__ == "__main__":
    main()
