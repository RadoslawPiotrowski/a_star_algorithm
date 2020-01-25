import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

PATCH_SIZE = 1
N = 10


class Node:
    g_val = 0
    h_val = 0
    is_visited = False
    point = []

    def __init__(self, point, end_point):
        self.point = point
        self.h_val = calculate_distance(point, end_point)

    def calculate_f(self):
        return self.g_val + self.h_val

    def calculate_g_val(self):
        pass

    def calculate_h_val(self):
        pass

    def get_att(self):
        return self.point, round(self.h_val, 2), round(self.g_val, 2), round(self.calculate_f(), 2), self.is_visited


def calculate_distance(point_1, point_2):
    dist = math.sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)
    return dist


def node_is_valid(cand_point, open_set, closed_set, actual_node):
    if (cand_point[0] < 0 or cand_point[1] < 0) and (cand_point[0] > N or cand_point[1] > N):
        return False
    if cand_point in [node.point for node in open_set]:
        return False
    if cand_point == actual_node.point:
        return False
    if cand_point in [node.point for node in closed_set]:
        return False
    return True


# UŻYWANA TYLKO PRZY INICJALIZACJI
def add_open_nodes(actual_node, open_set, board, closed_set):
    for i in range(3):
        for j in range(3):

            candidate_point = [actual_node.point[0] - 1 + i, actual_node.point[1] - 1 + j]
            if node_is_valid(candidate_point, open_set, closed_set, actual_node):
                open_set.append(board[candidate_point[0]][candidate_point[1]])


def node_is_valid_iteration(cand_point, actual_node):
    if (cand_point[0] < 0 or cand_point[1] < 0) and (cand_point[0] > N or cand_point[1] > N):
        return False
    if cand_point == actual_node.point:
        return False
    return True


# UŻYWANA W ITERACJACH
def get_neighbours_node(actual_node, board):
    neighbours = []

    for i in range(3):
        for j in range(3):
            candidate_point = [actual_node.point[0] - 1 + i, actual_node.point[1] - 1 + j]
            if node_is_valid_iteration(candidate_point, actual_node):
                neighbours.append(board[candidate_point[0]][candidate_point[1]])

    return neighbours


def add_to_closed_set(node, closed_set):
    node.is_visited = True
    closed_set.append(node)


def remove_node_from_open_set(node, open_set):
    idx = open_set.index(node)
    open_set.pop(idx)


def calculate_init_g_values(open_set, start_point):
    for node in open_set:
        node.g_val = calculate_distance(start_point, node.point)


def get_node_with_lowest_f_val(open_set):
    minimal_value = 1000
    best_node = open_set[0]

    for node in open_set:
        if node.calculate_f() < minimal_value:
            minimal_value = node.calculate_f()
            best_node = node
    return best_node


def main():

    start_point = [0, 8]
    end_point = [1, 2]
    path = []
    board = []

    for i in range(N):
        temp_array = []
        for j in range(N):
            node = Node([i, j], end_point)
            temp_array.append(node)
        board.append(temp_array)

    # Zbiór odwiedzonych punktów w postaci obiektów Node
    closed_set = []

    # Zbiór punktów dodanych do analizy w obiektów Node
    open_set = []

    # Inicjalizacja
    actual_node = board[start_point[0]][start_point[1]]
    final_node = board[end_point[0]][end_point[1]]

    # Dodajemy do open_set Wszystkie nody wokół początku
    add_open_nodes(actual_node, open_set, board, closed_set)
    # Dodajemy Node startowy do ścieżki
    path.append(board[start_point[0]][start_point[1]])
    # Dodajemy Node startowy closed_set
    add_to_closed_set(path[0], closed_set)

    # Dla każdego punktu z open_setu kalkulkujemy jego odległość od początkowego punktu
    calculate_init_g_values(open_set, start_point)

    print("Open_set: ", [node.get_att() for node in open_set])
    print("Closed_set: ", [node.get_att() for node in closed_set])
    i = 1
    while open_set:

        print("ITERACJA: ", i)
        # szukamy w open_secie najlepszego Noda z najniższym kosztem
        actual_node = get_node_with_lowest_f_val(open_set)

        print("Aktualny Node: ", actual_node.get_att())
        remove_node_from_open_set(actual_node, open_set)

        # Zbieramy wszystkich możliwych sąsiądów
        neighbours = get_neighbours_node(actual_node, board)

        for node in neighbours:
            # Warunek Końca
            if node is final_node:
                print("ŚCIEŻKA ZNALEZIONA")
                path.append(actual_node)
                path.append(node)
                print("PATH: ", [node.get_att() for node in path])
                exit(0)

            # Obliczamy wartość g_value każdego z sąsiadów
            node.g_val = actual_node.g_val + calculate_distance(node.point, actual_node.point)

            if node in open_set:
                # Jeśli aktualnie policzona wartość f sąsiada jest większa od tej, którą już znamy to omijamy
                if node.calculate_f() > open_set[open_set.index(node)].calculate_f():
                    continue
            if node in closed_set:
                # Jeśli aktualnie policzona wartość f sąsiada jest większa od tej, którą już znamy to omijamy
                if node.calculate_f() > closed_set[closed_set.index(node)].calculate_f():
                    continue
            open_set.append(node)

        closed_set.append(actual_node)
        actual_node.is_visited = True
        path.append(actual_node)
        i += 1

        print("Open_set: ", [node.get_att() for node in open_set])
        print("Closed_set: ", [node.get_att() for node in closed_set])


if __name__ == "__main__":
    main()
