import sys


class Bed:
    """
    Class representing beds. Stores its name, length and width along with its
    compatibility.
    """

    def __init__(self, name, x, y, compatibility):
        self.name = name
        self.x = x
        self.y = y
        self.persons_compatible = compatibility

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
    Class representing beds. Stores their name and minimum length and width
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
        beds_set1 = list(map((lambda x: (Bed(x.split()[0], float(x.split()[1]), float(x.split()[2]), int(x.split()[3])
                                             ))), beds_set1))

        # Create a list of second set of Person objects storing their
        # x,y coordinates and names
        persons_set2 = lines[size_persons1+size_beds1:size_persons1+size_beds1+size_persons2]
        persons_set2 = list(map((lambda x: (Person(x.split()[0], float(x.split()[1]), float(x.split()[2])))),
                                persons_set2))

        # Create a list of second set of Bed objects storing their
        # x,y coordinates and names
        beds_set2 = lines[size_persons1+size_beds1+size_persons2:size_persons1+size_beds1+size_persons2+size_beds2]
        beds_set2 = list(map((lambda x: (Bed(x.split()[0], float(x.split()[1]), float(x.split()[2]), int(x.split()[3])
                                             ))), beds_set2))

    return persons_set1, beds_set1, persons_set2, beds_set2


def merge(left_persons, left_beds, right_beds):
    """
    Merges the two sets together by calculating the compatibility of each bed in right_beds with each person in
    left_persons.
    :param left_persons: Subset of persons left of the vertical line
    :param left_beds: Subset of beds left of the vertical line
    :param right_beds: Subset of beds right of the vertical line
    :return: The merged beds with updated compatibility
    """

    persons_length = len(left_persons)
    beds_length = len(right_beds)

    # Pointer keeping track of the left persons
    persons_pointer = 0
    # Pointer keeping track of the right beds
    beds_pointer = 0

    num_compatible = 0

    while persons_pointer < persons_length and beds_pointer < beds_length:
        person = left_persons[persons_pointer]
        bed = right_beds[beds_pointer]

        # If bed's width greater than minimum person's
        # width. Then it is compatible with them and all of the
        # persons that came before it. Move to the next person
        if bed.get_y() >= person.get_y():
            num_compatible += 1
            persons_pointer += 1

        # Else set compatibility and move to the next bed
        else:
            current_compatibility = bed.get_compatibility()
            bed.set_compatibility(num_compatible + current_compatibility)
            beds_pointer += 1

    # If we ran out of left persons, set the compatibility of remaining
    # right beds to the one before it
    if beds_pointer < beds_length:
        for bed in right_beds[beds_pointer:]:
            bed.set_compatibility(bed.get_compatibility() + num_compatible)

    # Merge two sets and return
    return left_beds + right_beds


def print_results(beds):
    for bed in beds:
        print('{} {}'.format(bed.get_name(), bed.get_compatibility()))


def __main__():
    filename = sys.argv[1]
    nodes = read_file(filename)
    beds = merge(nodes[0], nodes[1], nodes[3])
    print_results(beds)


__main__()