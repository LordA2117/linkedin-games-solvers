// Submitting the POST req to our endpoint will be in the form of {nums: {<number>:<coordinates>}, walls[[[point a], [point b]]]}

const nums = {};
const walls = [];
let counter = 1;
const buttons_list = [];
const directions = [
  [0, 1],
  [1, 0],
  [0, -1],
  [-1, 0],
];

function cmp_array(a, b) {
  return a[0] === b[0] && a[1] === b[1];
}

function submit_dimensions() {
  const num_rows = Number(document.querySelector("#numrows").value);
  const num_cols = Number(document.querySelector("#numcols").value);
  const zip_grid = document.querySelector(".zip-grid");
  if (
    num_rows == null ||
    num_rows == "" ||
    num_rows <= 0 ||
    num_cols == null ||
    num_cols == "" ||
    num_cols <= 0
  ) {
    alert(
      "Please fill in the rows and columns with non-zero and non-negative values",
    );
    return;
  }

  for (let i = 0; i < num_rows; i++) {
    const row = zip_grid.insertRow();
    row.classList.add(`row-${i}`);
    const button_row = [];
    for (let j = 0; j < num_cols; j++) {
      if (j == num_cols - 1) {
        const cell = row.insertCell();
        const button = document.createElement("button");
        button.innerHTML = "G";
        button.classList.add("grid-cell");
        button.classList.add(`coordinate-${i}-${j}`);
        button.addEventListener("click", () => {
          button.innerHTML = `<b>${counter}</b>`;
          const coordinate_class = button.classList[1];
          const cell_coordinates = coordinate_class.split("-");
          nums[counter] = [
            Number(cell_coordinates.at(-2)),
            Number(cell_coordinates.at(-1)),
          ];
          counter += 1;
          button.style.backgroundColor = "orange";
          // console.log(nums);
        });
        button_row.push(button);
        cell.appendChild(button);
        continue;
      }
      const cell = row.insertCell();
      const button = document.createElement("button");
      button.innerHTML = "G";
      button.classList.add("grid-cell");
      button.classList.add(`coordinate-${i}-${j}`);
      button.addEventListener("click", () => {
        button.innerHTML = `<b>${counter}</b>`;
        const coordinate_class = button.classList[1];
        const cell_coordinates = coordinate_class.split("-");
        nums[counter] = [
          Number(cell_coordinates.at(-2)),
          Number(cell_coordinates.at(-1)),
        ];
        button.style.backgroundColor = "orange";
        counter += 1;
        // console.log(nums);
      });
      button_row.push(button);
      cell.appendChild(button);
      const wall_button = document.createElement("button");
      wall_button.innerHTML = "|";
      wall_button.classList.add("grid-wall-vertical");
      wall_button.classList.add(`wall-${i}-${j}`);
      wall_button.addEventListener("click", () => {
        const wall_coordinate = wall_button.classList[1].split("-");
        walls.push([
          [Number(wall_coordinate.at(-2)), Number(wall_coordinate.at(-1))],
          [Number(wall_coordinate.at(-2)), Number(wall_coordinate.at(-1)) + 1],
        ]);
        wall_button.style.backgroundColor = "black";
        wall_button.style.color = "white";
        // console.log(walls);
      });
      const wall_cell = row.insertCell();
      wall_cell.appendChild(wall_button);
    }
    buttons_list.push(button_row);
    if (i != num_rows - 1) {
      const wall_row = zip_grid.insertRow();
      for (let k = 0; k < num_cols; k++) {
        if (k == num_cols - 1) {
          const wall_btn = document.createElement("button");
          wall_btn.innerHTML = "—";
          wall_btn.classList.add("grid-wall-horizontal");
          wall_btn.classList.add(`wall-${i}-${k}`);
          wall_btn.addEventListener("click", () => {
            const wall_coordinate = wall_btn.classList[1].split("-");
            walls.push([
              [Number(wall_coordinate.at(-2)), Number(wall_coordinate.at(-1))],
              [
                Number(wall_coordinate.at(-2)) + 1,
                Number(wall_coordinate.at(-1)),
              ],
            ]);
            // console.log(walls);
            wall_btn.style.backgroundColor = "black";
            wall_btn.style.color = "white";
          });
          const wall_cell_vert = wall_row.insertCell();
          wall_cell_vert.appendChild(wall_btn);
          continue;
        }
        const wall_btn = document.createElement("button");
        wall_btn.innerHTML = "—";
        wall_btn.classList.add("grid-wall-horizontal");
        wall_btn.classList.add(`wall-${i}-${k}`);
        wall_btn.addEventListener("click", () => {
          const wall_coordinate = wall_btn.classList[1].split("-");
          walls.push([
            [Number(wall_coordinate.at(-2)), Number(wall_coordinate.at(-1))],
            [
              Number(wall_coordinate.at(-2)) + 1,
              Number(wall_coordinate.at(-1)),
            ],
          ]);
          // console.log(walls);
          wall_btn.style.backgroundColor = "black";
          wall_btn.style.color = "white";
        });
        const wall_cell_vert = wall_row.insertCell();
        wall_cell_vert.appendChild(wall_btn);
        const dummy_btn = document.createElement("button");
        dummy_btn.innerHTML = "  ";
        dummy_btn.classList.add("dummy");
        dummy_btn.classList.add("hidden");
        const dummy_cell = wall_row.insertCell();
        dummy_cell.appendChild(dummy_btn);
      }
    }
  }
}

const solve_button = document.querySelector("#solve");

solve_button.addEventListener("click", async () => {
  if (Object.keys(nums).length === 0) {
    alert("Please build the board first");
    return;
  }
  const num_rows = Number(document.querySelector("#numrows").value);
  const num_cols = Number(document.querySelector("#numcols").value);
  const response = await fetch("/solve_zip", {
    credentials: "same-origin",
    mode: "same-origin",
    method: "post",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      rows: num_rows,
      cols: num_cols,
      walls: walls,
      nums: nums,
    }),
  });
  const json_res = await response.json();
  console.log(json_res);
  // console.log(buttons_list);
  const solution = json_res.solution;
  if (solution.length === 0) {
    alert("No solution found");
    return;
  }
  // /\d/.test(document.querySelector('.coordinate-0-2').innerHTML) returns whether a number is in the innerHTML or not
  let i = 0;
  let j = i + 1;
  while (j < solution.length) {
    const curr_pt = solution[i];
    const next_pt = solution[j];
    const direction = [next_pt[0] - curr_pt[0], next_pt[1] - curr_pt[1]];
    const coordinate_selector = `.coordinate-${curr_pt[0]}-${curr_pt[1]}`;
    if (
      /\d/.test(document.querySelector(coordinate_selector).innerHTML) === false
    ) {
      if (cmp_array(direction, directions[0])) {
        document.querySelector(coordinate_selector).innerHTML = "<b>→</b>";
      } else if (cmp_array(direction, directions[1])) {
        document.querySelector(coordinate_selector).innerHTML = "<b>↓</b>";
      } else if (cmp_array(direction, directions[2])) {
        document.querySelector(coordinate_selector).innerHTML = "<b>←</b>";
      } else {
        document.querySelector(coordinate_selector).innerHTML = "<b>↑</b>";
      }
    } else if (
      /\d/.test(document.querySelector(coordinate_selector).innerHTML) === true
    ) {
      if (cmp_array(direction, directions[0])) {
        document.querySelector(coordinate_selector).innerHTML += "<b>→</b>";
      } else if (cmp_array(direction, directions[1])) {
        document.querySelector(coordinate_selector).innerHTML += "<b>↓</b>";
      } else if (cmp_array(direction, directions[2])) {
        document.querySelector(coordinate_selector).innerHTML += "<b>←</b>";
      } else {
        document.querySelector(coordinate_selector).innerHTML += "<b>↑</b>";
      }
    }
    // console.log(i, j);
    i = i + 1;
    j = j + 1;
  }
});

function reset_grid() {
  window.location.reload();
}

const dim_submit = document.querySelector("#submit-dimensions");
dim_submit.addEventListener("click", submit_dimensions);

const reset_dims = document.querySelector("#reset-dimensions");
reset_dims.addEventListener("click", reset_grid);

// NOTE: wall-0-0 for horizontal wall will mean that you add (0,0) and (1,0) to walls, similarly for vertical we'll add (0,0) and (0,1)
