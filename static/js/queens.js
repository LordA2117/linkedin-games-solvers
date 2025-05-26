const color_obj = {};

function clearChessBoard() {
  const chessboard = document.querySelector("#chessboard");
  while (chessboard.firstChild) {
    chessboard.removeChild(chessboard.lastChild);
  }
}

function createChessBoard(dim) {
  const chessboard = document.querySelector("#chessboard");
  for (let i = 0; i < dim; i++) {
    const row = chessboard.insertRow();
    row.classList.add(`row-${i}`);

    for (let j = 0; j < dim; j++) {
      const cell = row.insertCell();
      const button = document.createElement("button");
      button.classList.add("cell");
      button.classList.add(`coordinate-${i}${j}`);
      button.innerHTML = "E";
      button.addEventListener("click", () => {
        const colorValue = document.querySelector("#region-color").value;
        button.style.backgroundColor = colorValue;
        const classes = button.classList;
        const coordinates = [
          Number(classes[1].at(-2)),
          Number(classes[1].at(-1)),
        ];
        color_obj[coordinates] = colorValue;
        // console.log(color_obj);
      });

      cell.appendChild(button);
      // cell.style.border = "1px solid black";
      // cell.style.width = "4px";
      // cell.style.height = "4px";
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector("#dim-submit");

  const reset_button = document.querySelector("#reset-color");
  reset_button.addEventListener("click", () => {
    const color_buttons = document.querySelectorAll(".cell");
    for (let i = 0; i < color_buttons.length; i++) {
      color_buttons[i].style.backgroundColor = "";
    }
    // Reset the color obj
    for (var member in color_obj) delete color_obj[member];
    console.log(color_obj);
  });

  button.addEventListener("click", () => {
    const dim = Number(document.querySelector("#numrows").value);
    if (dim == null || dim == "" || dim <= 0) {
      alert("Please fill the dimensions");
    } else {
      console.log(typeof dim);
      clearChessBoard(); // https://stackoverflow.com/questions/3955229/remove-all-child-elements-of-a-dom-node-in-javascript
      createChessBoard(dim);
    }
  });

  const solve_button = document.querySelector("#solve");
  solve_button.addEventListener("click", async () => {
    const dim = Number(document.querySelector("#numrows").value);
    const response = await fetch("/solve_queens", {
      credentials: "same-origin",
      mode: "same-origin",
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        dimension: dim,
        board_colors: color_obj,
      }),
    });
    const res = await response.json();
    const cells = document.querySelectorAll(".cell");
    if (Boolean(res.error)) {
      alert(res.error);
    }
    await console.log(res);
    const sol = res.solution;
    for (let i = 0; i < cells.length; i++) {
      const cell = cells[i];
      const classes = cell.classList;
      const coordinates = [
        Number(classes[1].at(-2)),
        Number(classes[1].at(-1)),
      ];
      for (let j = 0; j < sol.length; j++) {
        if (sol[j][0] === coordinates[0] && sol[j][1] === coordinates[1]) {
          cell.innerHTML = "<b>Q</b>";
        }
      }
    }
  });
});
