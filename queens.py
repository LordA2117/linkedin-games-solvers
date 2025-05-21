from pprint import pprint
from itertools import chain
from functools import lru_cache

# Simply based on the solution for n queens problem

# Now the board will be something like this
test_region_board = (
    ("A", "A", "B", "C"),
    ("A", "B", "B", "C"),
    ("A", "B", "B", "C"),
    ("A", "A", "C", "C"),
)


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

    if r - 1 in range(R) and c - 1 in range(C):
        neighbours.append((r - 1, c - 1))

    if r + 1 in range(R) and c + 1 in range(C):
        neighbours.append((r + 1, c + 1))

    if r + 1 in range(R) and c - 1 in range(C):
        neighbours.append((r + 1, c - 1))

    if r - 1 in range(R) and c + 1 in range(C):
        neighbours.append((r - 1, c + 1))

    return tuple(neighbours)


@lru_cache(maxsize=None)
def get_region(region_letter, region_board):
    queue = [(0, 0)]
    seen = set()
    region = []
    while len(queue) > 0:
        point = queue.pop(0)
        if point in seen:
            continue
        neighbours = get_neighbours(point, region_board)
        for i in neighbours:
            if region_board[i[0]][i[1]] == region_letter:
                region.append(i)
            queue.append(i)
        seen.add(point)

    return tuple(set(region))


# Tests
# pprint(test_region_board)
# print(get_region("A", test_region_board))
# print(get_region("B", test_region_board))
# print(get_region("C", test_region_board))


def get_unique_regions(board):
    return tuple(set(chain.from_iterable(board)))


# Tests
# print(get_unique_regions(test_region_board))


def is_safe(square, board, region_board) -> bool:
    R = len(board)
    C = len(board[0])
    r, c = square  # Row and column number of the square on the normal board

    # Check for safe column
    for i in range(R):
        if i == r:
            continue
        if board[i][c] == "Q":
            return False

    # Check for safe row
    for i in range(C):
        if i == c:
            continue
        if board[r][i] == "Q":
            return False

    # Check adjacent squares
    for neighbour in get_neighbours(square, board):
        if board[neighbour[0]][neighbour[1]] == "Q":
            return False

    # Check regions
    letter = region_board[r][c]
    region_area = get_region(letter, region_board)
    for x, y in region_area:
        if board[x][y] == "Q":
            return False

    return True


# TODO: Finish the game tmrw (if you have time, otherwise do after crypto)
def solveUtil(board, region_board, column_number, number_of_queens):
    # number of queens will be the number of regions
    if column_number >= number_of_queens:
        return True

    for i in range(number_of_queens):
        if is_safe((i, column_number), board, region_board):
            board[i][column_number] = "Q"

            if solveUtil(board, region_board, column_number + 1, number_of_queens):
                return True

            board[i][column_number] = 0

    return False


def printBoard(board, region_board):
    for i in range(len(board)):
        string = ""
        row = board[i]
        for j in range(len(row)):
            if board[i][j] == "Q":
                string += "Q "
            else:
                string += "◙ "
        print(string)


def solve():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]

    region_board = (
        ("P", "X", "X", "X", "X", "L", "L", "L"),
        ("P", "X", "X", "X", "X", "X", "X", "X"),
        ("P", "X", "X", "G", "X", "X", "X", "X"),
        ("X", "X", "X", "G", "G", "G", "X", "X"),
        ("X", "X", "X", "E", "E", "G", "X", "X"),
        ("X", "E", "E", "E", "O", "O", "X", "Y"),
        ("X", "X", "X", "X", "X", "O", "X", "Y"),
        ("B", "B", "B", "X", "O", "O", "X", "Y"),
    )

    if solveUtil(board, region_board, 0, 8) == False:
        print("Sorry no sol")
    else:
        printBoard(board, region_board)


solve()
