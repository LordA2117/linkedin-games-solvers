from pprint import pprint
from flask import Flask, jsonify, render_template, request
from utils.queens import solve
from utils.zip import dfs

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/queens", methods=["GET"])
def queens():
    if request.method == "GET":
        return render_template("queens.html")


@app.route("/solve_queens", methods=["POST"])
def queens_solve():
    if request.method == "POST":
        queen_coords = set()
        coordinates = request.get_json(force=True)
        coordinates = dict(coordinates)
        board_dimension = int(coordinates["dimension"])
        board = [[0] * board_dimension for _ in range(board_dimension)]
        region_board = [["X"] * board_dimension for _ in range(board_dimension)]
        for k, v in coordinates["board_colors"].items():
            coords = k.split(",")
            # print(coords)
            region_board[int(coords[0])][int(coords[1])] = v
        region_board = tuple(tuple(_) for _ in region_board)
        # pprint(board)
        # pprint(region_board)
        solution = solve(board, region_board)
        if not solution:
            return jsonify({"error": "No Solution"})
        for i in range(len(solution)):
            for j in range(len(solution[i])):
                if board[i][j]:
                    queen_coords.add((i, j))
        # pprint(solution)
        # print(queen_coords)
        return jsonify({"solution": list(queen_coords)})


@app.route("/zip", methods=["GET"])
def zip():
    if request.method == "GET":
        return render_template("zip.html")


@app.route("/solve_zip", methods=["POST"])
def zip_solve():
    data = request.json
    # print(data)
    num_rows = data["rows"]
    num_cols = data["cols"]
    walls = data["walls"]
    nums = data["nums"]

    nums_and_coords = {}

    for key in nums:
        nums_and_coords[tuple(nums[key])] = int(key)
    # print(nums_and_coords)

    for i in walls:
        for j in range(len(i)):
            i[j] = tuple(i[j])

    # print(walls)

    board = tuple("-" * num_cols for _ in range(num_rows))
    # print(board)

    paths = dfs(
        min(nums_and_coords, key=nums_and_coords.get),
        max(nums_and_coords, key=nums_and_coords.get),
        board,
        nums_and_coords,
        walls,
    )

    print(paths)

    return jsonify({"solution": paths})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
