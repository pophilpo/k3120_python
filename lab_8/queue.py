class Country:

    def __init__(self, name, capital, population):
        self.name = name
        self.capital = capital
        self.population = population

    def __eq__(self, other):

        return self.name == other.name

    def __str__(self):

        return f"(Country: {self.name} | Capital: {self.capital} | Population: {self.population})"



class Node:

    def __init__(self, data, nextnode=None):
        self.contained_object = data
        self.next = nextnode
    def __str__(self):

        return str(self.contained_object)



class MyQueue:

    def __init__(self, head=None):
        self.head = head

    def add(self, obj):

        new_node = Node(obj)
        new_node.next = self.head
        self.head = new_node

    def remove(self, data):

        current_node = self.head
        prev_node = None

        while current_node is not None:
            if current_node.contained_object == data:
                if prev_node is not None:
                    prev_node.next = current_node.next
                else:
                    self.head = current_node.next
                return 
            else:
                prev_node = current_node
                current_node = current_node.next
        return


    def __str__(self):

        if self.head == None:
            return "Empty LinkedList"

        result = list()
        template = "[{}]"
        current = self.head

        result.append(template.format(current))

        while current.next:
            current = current.next
            result.append(template.format(current))

        return " --> ".join(result)

    def clear(self):
        self.__init__()

    def to_list(self):
        result = list()

        if self.head == None:
            return result
        current = self.head
        result.append(current)
        while current.next:
            current = current.next
            result.append(current)


        return result




def main():

    nums_queue = MyQueue()

    nums_queue.add(4)
    nums_queue.add(3)
    nums_queue.add(5)
    nums_queue.add(123)
    nums_queue.add(4)

    print("_"*40)
    print("Numbers Queue")

    print(nums_queue)
    print("Deleting number 5")
    nums_queue.remove(5)
    print(nums_queue)


    print("_"*40)
    print("Countires Queue")

    Russia = Country("Russia", "Moscow", 152000000)
    Moldova = Country("Moldova", "Kishinev", 2913000)
    Canada = Country("Canada", "Ottava", 37600000)

    countries = MyQueue()
    countries.add(Russia)
    countries.add(Moldova)
    countries.add(Canada)

    print(countries)

    print("Deleting country Moldova")
    countries.remove(Moldova)
    print(countries)




if __name__ == "__main__":
    main()
