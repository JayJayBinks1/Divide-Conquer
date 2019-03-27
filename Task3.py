import sys


class Bed:
    """
    Class representing beds. Stores its name, length and width along with its
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

    def increment_compatibility(self):
        self.persons_compatible += 1


class Person:
    """
    Class representing persons. Stores their name and minimum length and width
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
    Reads the x and y coordinate for each person and bed. Returns
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
        # x and ycoordinates and names
        persons = lines[1:amount_persons+1]
        persons = list(map((lambda x: (Person(x.split()[0], float(x.split()[1]), float(x.split()[2])))), persons))

        # Create a list of Bed objects storing their
        # x and y coordinates and names
        beds = lines[amount_persons+1: len(lines)]
        beds = list(map((lambda x: (Bed(x.split()[0], float(x.split()[1]), float(x.split()[2])))), beds))

    return persons, beds


def merge(left_nodes, right_nodes, coordinate):
    """
    Merges two lists of nodes in ascending order
    of their x or y coordinates.
    :param left_nodes: Left nodes to be sorted
    :param right_nodes: Right nodes to be sorted
    :param coordinate: The coordinate (x or y) to compare the nodes with
    :return: Merged list
    """

    left_length = len(left_nodes)
    right_length = len(right_nodes)

    # Initialise pointers to track positions in both lists
    left_pointer = 0
    right_pointer = 0

    merged_list = list()

    while left_pointer < left_length and right_pointer < right_length:

        left_node = left_nodes[left_pointer]
        right_node = right_nodes[right_pointer]

        # If the left node <= right node, add it to the merge list
        # and increment the left pointer.
        if coordinate == 'x' and left_node.get_x() <= right_node.get_x():
            merged_list.append(left_node)
            left_pointer += 1

        elif coordinate == 'y' and left_node.get_y() <= right_node.get_y():
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
    if left_pointer < left_length:
        merged_list.extend(left_nodes[left_pointer:])
    elif right_pointer < right_length:
        merged_list.extend(right_nodes[right_pointer:])

    return merged_list


def sort_two(node1, node2, coordinate):
    """
    Returns a list of the two nodes.
    If node1 <= node2, node1 is the first element.
    If node1 > node2, node2 is the second element.
    Compares the nodes by x or y coordinate, specified by coordinate.
    :param node1: First node
    :param node2: Second node
    :param coordinate: The coordinate (x or y) to compare the nodes with
    :return: List of sorted nodes
    """

    if coordinate == 'x' and node1.get_x() <= node2.get_x():
        return [node1, node2]

    elif coordinate == 'y' and node1.get_y() <= node2.get_y():
        return [node1, node2]

    return [node2, node1]


def merge_sort(nodes, coordinate):
    """
    Sorts nodes by ascending order of x or y coordinate.
    Uses recursive merge sort.
    :param nodes: Nodes to be sorted
    :param coordinate: The x or y coordinate to sort by
    :return: List of sorted nodes
    """

    # if nodes has 1 or no elements, return nodes
    if len(nodes) <= 1:
        return nodes

    # If nodes has 2 elements, sort them
    if len(nodes) < 3:
        return sort_two(nodes[0], nodes[1], coordinate)

    # Else, divide in two and recurse
    half_point = len(nodes)//2
    left_nodes = nodes[:half_point]
    right_nodes = nodes[half_point:len(nodes)]

    left_nodes = merge_sort(left_nodes, coordinate)
    right_nodes = merge_sort(right_nodes, coordinate)

    # merge the lists and return them
    return merge(left_nodes, right_nodes, coordinate)


def divide(nodes, x):
    """
    Divide step of divid and conquer. Divides a list of nodes into two sets based on a vertical line denoted by an x
    coordinate.
    :param nodes: List of nodes to be divided
    :param x: x coordinate of the vertical line
    :return: tuple containing two divided lists
    """

    # TODO Deal with non-distinct cases

    left_list = list()
    right_list = list()

    for node in nodes:
        if node.get_x() <= x:
            left_list.append(node)
        else:
            right_list.append(node)

    return left_list, right_list


def calculate_compatibility(persons, bed):
    """
    Calculates the compatibility of the bed against each person in persons
    :param persons: List of persons
    :param bed: The bed
    :return: Bed with updated compatibility
    """
    for person in persons:
        if bed.get_x() >= person.get_x() and bed.get_y() >= person.get_y():
            bed.increment_compatibility()
    return bed


def conquer(left_persons, left_beds, right_beds):
    """
    Conquer step to divide and conquer. Computes the compatibility of the right subset of beds with the left subset of
    persons, then merges the left and right beds/
    :param left_persons: Left subset of persons
    :param left_beds: Left subset of beds
    :param right_beds: Right subset of beds
    :return: right_beds with updated compatibility
    """

    # Initialise pointers to track positions in both lists
    persons_pointer = 0
    beds_pointer = 0

    num_compatible = 0

    while persons_pointer < len(left_persons) and beds_pointer < len(right_beds):
        person = left_persons[persons_pointer]
        bed = right_beds[beds_pointer]

        # If the person is compatible with the bed (i.e. bed's width is >= person's minimum width)
        # Then increase that bed's compatibility and move to the next person
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
    if beds_pointer < persons_pointer:
        for bed in right_beds[beds_pointer:]:
            bed.set_compatibility(bed.get_compatibility() + num_compatible)

    return merge(left_beds, right_beds, 'y')


def divide_and_conquer(sorted_persons_y, sorted_beds_y, sorted_nodes_x):
    """
    Recursive divide and conquer algorithm to compute the compatibility of each bed.
    Divides the y sorted beds in half by x coordinate.
    :param sorted_persons_y: Persons sorted by y coordinate
    :param sorted_beds_y: Beds sorted by y coordinate
    :param sorted_nodes_x: Persons and Beds sorted by x coordinate
    :return: sorted_beds_y with updated compatibilities
    """

    # If subset contains no persons or beds, return the list of beds
    # Returns empty list if no beds
    if len(sorted_persons_y) == 0 or len(sorted_beds_y) == 0:
        return sorted_beds_y

    if len(sorted_beds_y) == 1:
        sorted_beds_y[0] = calculate_compatibility(sorted_persons_y, sorted_beds_y[0])
        return sorted_beds_y

    # Split sorted_beds_x roughly in half and find the middle x coordinate
    left_nodes_x = sorted_nodes_x[:len(sorted_nodes_x)//2]
    right_nodes_x = sorted_nodes_x[len(sorted_nodes_x)//2:]
    middle_x_coordinate = left_nodes_x[-1].get_x()

    # Split beds and persons by the middle x coordinate and recurse
    left_beds, right_beds = divide(sorted_beds_y, middle_x_coordinate)
    left_persons, right_persons = divide(sorted_persons_y, middle_x_coordinate)
    left_beds = divide_and_conquer(left_persons, left_beds, left_nodes_x)
    right_beds = divide_and_conquer(right_persons, right_beds, right_nodes_x)

    # Compute the compatibility of right side of beds with left side of persons
    # Merge left and right beds and return
    conquered_beds = conquer(left_persons, left_beds, right_beds)
    return conquered_beds


def print_result(beds):
    """
    Prints the result
    :param beds: Beds to print
    """
    for bed in beds:
        print("{} {}".format(bed.get_name(), bed.get_compatibility()))


def __main__():
    filename = sys.argv[1]
    nodes = read_file(filename)

    # Sort persons and beds by y coordinate in separate lists
    sorted_persons_y = merge_sort(nodes[0], 'y')
    sorted_beds_y = merge_sort(nodes[1], 'y')
    # Sort both persons and beds by x coordinate in the same list
    joined_nodes = nodes[0] + nodes[1]
    sorted_nodes_x = merge_sort(joined_nodes, 'x')

    compatible_beds = divide_and_conquer(sorted_persons_y, sorted_beds_y, sorted_nodes_x)
    print_result(compatible_beds)


__main__()
