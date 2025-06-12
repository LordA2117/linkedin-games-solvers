from functools import lru_cache
from time import perf_counter

board = (
    "-------",
    "-------",
    "-------",
    "-------",
    "-------",
    "-------",
    "-------",
)

numbered_nodes = {
    (0, 0): 3,
    (0, 6): 1,
    (1, 1): 2,
    (2, 3): 6,
    (2, 5): 7,
    (4, 1): 5,
    (4, 3): 4,
    (5, 5): 9,
    (6, 0): 10,
    (6, 6): 8,
}

walls = [
    [(0, 4), (1, 4)],
    [(0, 3), (1, 3)],
    [(1, 2), (1, 3)],
    [(2, 1), (3, 1)],
    [(2, 2), (3, 2)],
    [(2, 2), (2, 3)],
    [(2, 5), (2, 6)],
    [(3, 0), (3, 1)],
    [(3, 4), (4, 4)],
    [(3, 5), (4, 5)],
    [(3, 5), (3, 6)],
    [(4, 0), (4, 1)],
    [(4, 3), (4, 4)],
    [(5, 2), (6, 2)],
    [(5, 3), (6, 3)],
    [(5, 3), (5, 4)],
]


def find_start(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "1":
                return (i, j)
    return ()


@lru_cache(maxsize=None)
def get_coordinates(board):
    coords = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            coords.add((i, j))

    return coords


def get_neighbours(square, board):
    R = len(board)
    C = len(board[0])

    r, c = square

    neighbours = []

    if r - 1 in range(R):
        neighbours.append((r - 1, c))

    if r + 1 in range(R):
        neighbours.append((r + 1, c))

    if c - 1 in range(C):
        neighbours.append((r, c - 1))

    if c + 1 in range(C):
        neighbours.append((r, c + 1))

    return tuple(neighbours)


def check_path(path, numbered_nodes):
    path_order = []
    for i in path:
        if i in numbered_nodes:
            path_order.append(numbered_nodes[i])

    if all(path_order[i] < path_order[i + 1] for i in range(len(path_order) - 1)):
        return True

    return False


def check_walls(path, walls):
    for i in walls:
        for j in range(len(path) - len(i) + 1):
            if path[j : j + len(i)] == i:
                return True
    return False


def dfs(start, end, board, numbered_nodes, walls):
    visited_dict = {}
    for i in get_coordinates(board):
        visited_dict[i] = 0

    stack = [(start, [start], numbered_nodes[start])]
    paths = []

    while stack:
        node, path, last_visited_node = stack.pop()
        # print(node, path)

        if node == end:
            if (
                len(path) == len(board) * len(board[0])
                and check_path(path, numbered_nodes)
                and not check_walls(path, walls)
            ):
                return path
            paths.append(path)
            continue

        for i in get_neighbours(node, board):
            # This was my old solution, I'm going to leave the functions there so that you can take a crack at why this is not a very good solution

            # if (
            #     i not in path
            #     and check_path(path, numbered_nodes)
            #     and not check_walls(path, walls)
            # ):
            #     stack.append((i, path + [i]))

            new_path = path + [i]

            if i not in path:
                if [path[-1], i] not in walls and [i, path[-1]] not in walls:
                    if i not in numbered_nodes:
                        stack.append((i, new_path, last_visited_node))
                    else:
                        if numbered_nodes[i] == last_visited_node + 1:
                            stack.append((i, new_path, last_visited_node + 1))

    return paths


def render(board, numbered_nodes, path):
    for i in range(len(board)):
        string = ""
        for j in range(len(board[i])):
            if (i, j) in path:
                if (i, j) in numbered_nodes:
                    string += f"{str(numbered_nodes[(i, j)]):<5}"
                else:
                    string += f"{'x':<5}"
            else:
                string += f"{'-':<5}"
        print(string)


# test case 2
# board = (
#     "------",
#     "------",
#     "------",
#     "------",
#     "------",
#     "------",
# )
#
# numbered_nodes = {
#     (0, 0): 1,
#     (0, 1): 12,
#     (0, 4): 10,
#     (1, 3): 11,
#     (2, 0): 4,
#     (2, 4): 9,
#     (3, 3): 2,
#     (3, 5): 8,
#     (4, 0): 5,
#     (4, 2): 3,
#     (4, 4): 7,
#     (5, 3): 6,
# }
#
# walls = []

start = perf_counter()
paths = dfs(
    min(numbered_nodes, key=numbered_nodes.get),
    max(numbered_nodes, key=numbered_nodes.get),
    board,
    numbered_nodes,
    walls,
)

end = perf_counter()

render(board, numbered_nodes, paths)
print("****************************************************\n")
print(paths)
print(f"Found valid path in {end-start}s")
