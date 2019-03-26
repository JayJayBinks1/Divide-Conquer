import sys


class Bed:
    """
    Class representing beds. Stores its name and length along with its
    compatibility.
    """

    def __init__(self, name, x):
        self.name = name
        self.x = x
        self.persons_compatible = 0

    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def set_compatibility(self, persons_compatible):
        self.persons_compatible = persons_compatible

    def get_compatibility(self):
        return self.persons_compatible


class Person:
    """
    Class representing beds. Stores their name and minimum length
    for compatibility with a bed.
    """

    def __init__(self, name, x):
        self.name = name
        self.x = x

    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x


def read_file(filename):
    """
    Reads the x coordinate for each person and bed. Returns
    a list of Bed and Person classes containing said x coordinate.
    :param filename: Name of the file
    :return: Tuple containing lists of Beds and Persons
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Read the first line containing number of
        # beds and persons
        amount_persons = int(lines[0])

        # Create a list of Person objects storing their
        # x coordinates and names
        persons = lines[1:amount_persons+1]
        persons = list(map((lambda x: (Person(x.split()[0], float(x.split()[1])))), persons))

        # Create a list of Bed objects storing their
        # x coordinates and names
        beds = lines[amount_persons+1: len(lines)]
        beds = list(map((lambda x: (Bed(x.split()[0], float(x.split()[1])))), beds))

    return persons, beds


def merge(left_nodes, right_nodes):
    """
    Merges two lists of nodes in ascending order
    of their x coordinates.
    :param left_nodes: Left nodes to be sorted
    :param right_nodes: Right nodes to be sorted
    :return: Merged list
    """

    left_length = len(left_nodes)
    right_length = len(right_nodes)

    # Initialise pointers to track positions in
    # both lists
    left_pointer = 0
    right_pointer = 0

    merged_list = list()

    while left_pointer < left_length and right_pointer < right_length:

        left_node = left_nodes[left_pointer]
        right_node = right_nodes[right_pointer]

        # If the left node <= right node, add it to the merge list
        # and increment the left pointer.
        if left_node.get_x() <= right_node.get_x():
            merged_list.append(left_node)
            left_pointer += 1

        # Else add right node to merge list and
        # increment the right pointer.
        else:
            merged_list.append(right_node)
            right_pointer += 1

    # If one list was larger than the other
    # add the remaining elements in the larger list
    # to the merged list
    if left_pointer < right_pointer:
        merged_list.extend(left_nodes[left_pointer:])
    else:
        merged_list.extend(right_nodes[right_pointer:])

    return merged_list


def sort_two(node1, node2):
    """
    Returns a list of the two nodes.
    If node1 <= node2, node1 is the first element.
    If node1 > node2, node2 is the second element.
    :param node1: First node
    :param node2: Second node
    :return: List of sorted nodes
    """

    if node1.get_x() <= node2.get_x():
        return [node1, node2]

    return [node2, node1]


def merge_sort(nodes):
    """
    Sorts nodes by ascending order of x coordinate.
    Uses recursive merge sort.
    :param nodes: Nodes to be sorted
    :return: List of sorted nodes
    """

    # if nodes has 1 or no elements, return nodes
    if len(nodes) <= 1:
        return nodes

    # If nodes has 2 elements, sort them
    if len(nodes) < 3:
        return sort_two(nodes[0], nodes[1])

    # Else, divide in two and recurse
    half_point = len(nodes)//2
    left_nodes = nodes[:half_point]
    right_nodes = nodes[half_point:len(nodes)]

    left_nodes = merge_sort(left_nodes)
    right_nodes = merge_sort(right_nodes)

    # merge the lists and return them
    return merge(left_nodes, right_nodes)


def calculate_compatibility(persons, beds):
    """
    Calculates the compatibility of each bed
    by comparing its dimensions to each person's
    minimal requirements. Returns None if unequal amount
    of persons and beds.
    :param persons: Sorted list of person objects
    :param beds: Sorted list of bed objects
    :return: Bed objects with updated compatibility. None if
    beds and persons are unequal.
    """

    if len(beds) != len(persons):
        return None

    # Initialise pointers to track positions in
    # both lists
    persons_pointer = 0
    beds_pointer = 0

    num_compatible = 0

    while persons_pointer < len(persons) and beds_pointer < len(beds):
        person = persons[persons_pointer]
        bed = beds[beds_pointer]

        # If bed's length greater than minimum person's
        # length. Then it is compatible with them and all of the
        # persons that came before it. Move to the next person
        if bed.get_x() >= person.get_x():
            num_compatible += 1
            persons_pointer += 1

        # Else set compatibility and move to the next bed
        else:
            bed.set_compatibility(num_compatible)
            beds_pointer += 1

    # If we ran out of persons, set the compatibility of remaining
    # beds to the one before it
    if beds_pointer < persons_pointer:
        map((lambda bed: bed.set_compatibility(num_compatible)), beds[beds_pointer:])

    return beds


def print_compatibility(beds):
    """
    Prints the results
    NOTE: This is an O(n^2) operation just to print to screen,
    it is NOT a part of my algorithm
    """
    n = 1
    while n <= len(beds):
        for bed in beds:
            if bed.get_name()[1] == str(n):
                print("{} {}".format(bed.get_name(), bed.get_compatibility()))
                n += 1


def __main__():
    filename = sys.argv[1]
    nodes = read_file(filename)

    sorted_persons = merge_sort(nodes[0])
    sorted_beds = merge_sort(nodes[1])

    compatible_beds = calculate_compatibility(sorted_persons, sorted_beds)
    print_compatibility(compatible_beds)

__main__()