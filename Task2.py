import sys


class Bed:
    """
    Class representing beds. Stores its name and length along with its
    compatibility.
    """

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.persons_compatible = 0

    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def set_compatibility(self, persons_compatible):
        self.persons_compatible = persons_compatible

    def get_compatibility(self):
        return self.persons_compatible


class Person:
    """
    Class representing beds. Stores their name and minimum length
    for compatibility with a bed.
    """

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y


def read_file(filename):
    """
    Reads file with two sets of persons and beds. Reads the x and y coordinate for
    each person and bed. Also reads the current compatibility of each bed. Returns
    two lists each of Beds and Persons, one for each set.
    :param filename: Name of the file
    :return: Tuple containing lists of Beds and Persons
    """
    with open(filename, 'r') as file:
        # Read the first line containing number of
        # beds and persons
        amount_persons = int(file.readline())
        size_persons1 = int(file.readline())
        size_beds1 = int(file.readline())
        size_persons2 = amount_persons - size_persons1
        size_beds2 = amount_persons - size_beds1

        lines = file.readlines()

        # Create a list of first set of Person objects storing their
        # x,y coordinates and names
        persons_set1 = lines[:size_persons1]
        persons_set1 = list(map((lambda x: (Person(x.split()[0], float(x.split()[1]), float(x.split()[2])))),
                                persons_set1))

        # Create a list of first set of Bed objects storing their
        # x,y coordinates and names
        beds_set1 = lines[size_persons1:size_persons1+size_beds1]
        beds_set1 = list(map((lambda x: (Person(x.split()[0], float(x.split()[1]), float(x.split()[2])))),
                                beds_set1))

        # Create a list of second set of Person objects storing their
        # x,y coordinates and names
        persons_set2 = lines[size_persons1+size_beds1:size_persons1+size_beds1+size_persons2]
        persons_set2 = list(map((lambda x: (Person(x.split()[0], float(x.split()[1]), float(x.split()[2])))),
                                persons_set2))

        # Create a list of second set of Bed objects storing their
        # x,y coordinates and names
        beds_set2 = lines[size_persons1+size_beds1+size_persons2:size_persons1+size_beds1+size_persons2+size_beds2]
        beds_set2 = list(map((lambda x: (Person(x.split()[0], float(x.split()[1]), float(x.split()[2])))),
                             beds_set2))

    return persons_set1, beds_set1, persons_set2, beds_set2


def __main__():
    filename = sys.argv[1]
    nodes = read_file(filename)


__main__()