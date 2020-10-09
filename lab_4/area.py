#!/usr/bin/env python3

class Point:

    def __init__(self, x, y):

        self.x = x
        self.y = y


class Triangle:

    def __init__(self, a, b, c):

        self.a = a
        self.b = b
        self.c = c


    def area(self):

        # S = 0.5 * | (x2-x1)(y3-y1) - (x3-x1)(y2-y1) |
        area = 0.5 * abs((self.b.x - self.a.x) * (self.c.y - self.a.y) - (self.c.x - self.a.x) * (self.b.y - self.a.y))

        return area



def main():

    points = list()

    # Предполагается, что пятиугольник выпуклый
    print("Введите координаты точки в формате x y. Пример ввода: 1.12 8 \n")

    while len(points) < 5:

        user_input = input()

        x, y = map(float, user_input.split(" "))

        points.append(Point(x, y))


    triangle_1 = Triangle(points[0], points[1], points[2])
    triangle_2 = Triangle(points[2], points[3], points[4])
    triangle_3 = Triangle(points[0], points[2], points[4])

    result = triangle_1.area() + triangle_2.area() + triangle_3.area()

    print(f"Площадь заданного пятиугольника: {result}")


if __name__ == "__main__":
    main()
