//When window loads, set the board position.
window.onload = function () {
  path = window.location.pathname
  board = createBoard();
  is_game_over = false;
  jQuery.get("/current_board_state", (response) => board.position(response));
};

function get_board_orientation() {
  return board.orientation;
}

// This function creates a table for the moves.
function createTable(moves) {
  // console.log(moves)
  $("#history thead").remove();
  $("#history tbody").remove();
  var table = document.getElementById('history');

  var tableHead = document.createElement('thead');
  var tr = document.createElement('tr');
  var th = document.createElement('th');
  th.appendChild(document.createTextNode("White"))
  tr.appendChild(th)
  var th = document.createElement('th');
  th.appendChild(document.createTextNode("Black"))
  tr.appendChild(th)
  tableHead.appendChild(tr)
  table.appendChild(tableHead)

  if (moves.length == 0 || moves == undefined || moves == "[]" || moves == "") {
    return;
  }

  var tableBody = document.createElement('tbody');
  for (var i = 0; i < moves.length; i+=2) {
    var tr = document.createElement('tr');
    var td = document.createElement('td');
    td.appendChild(document.createTextNode(moves[i]))
    tr.appendChild(td)

    var nextMove = moves[i+1]
    if (nextMove != undefined) {
      var td = document.createElement('td');
      td.appendChild(document.createTextNode(nextMove))
      tr.appendChild(td)
    }
    tableBody.appendChild(tr);
  }
  table.appendChild(tableBody)
}

//Rows for the chess board. Position of the pieces 0-63.
function get_pos(s) {
  return 8 * (parseInt(s[1]) - 1) + "abcdefgh".indexOf(s[0]);
}

//Using jquery to request position of the source and the target of the move and using the response to make a move.
function onDrop(source, target, piece, newPos, oldPos, orientation) {
  if (source == target) {
    return;
  }
  var p =
    (orientation == "white" &&
      target.charAt(1) == "8" &&
      piece.charAt(1) == "P") ||
    (orientation == "black" &&
      target.charAt(1) == "1" &&
      piece.charAt(1) == "P");

  if (orientation == "white") {
    d = document.getElementById("bDepth");
  } else {
    d = document.getElementById("wDepth");
  }
  ai = document.getElementById("aiChoice");
  // console.log(ai.value)
  
  jQuery.get(
    "/move",
    {
      source: get_pos(source),
      target: get_pos(target),
      promotion: p,
      depth: d.value,
      ai: ai.value
    },
    function (response) {
      board.position(response);
    }
  );

  jQuery.get("/past_moves", function (response) {
    response = response.substring(2, response.length-2);
    response = response.split("', '");
    // console.log(response)
    createTable(response)
  });

  isGameOver();
}

//When a piece is beginning to be dragged.
function onDragStart(source, piece, position, orientation) {
  if (orientation == "black" && piece.search(/^w/) !== -1) return false;
  if (orientation == "white" && piece.search(/^b/) !== -1) return false;

  if (is_game_over) {
    alert("Game is over.");
    return false;
  }
}

function selfPlay(d, p, aiType) {
  // Black Move
  jQuery.get(
    "/selfplay",
    {
      depth: d,
      player: p,
      ai: aiType
    },
    function (response) {
      board.position(response);
    }
  );
}

// Check if the game is over or not function.
function isGameOver() {
  jQuery.get("/is_game_over", function (response) {
    if (response == "True") {
      is_game_over = true;
    }
  });
}

// Creating the board function.
function createBoard() {
  var page = window.location.pathname;
  var colour = null;
  var type = null
  var ai = null
  is_game_over = false;
  board = null;
  
  if (page == "/ai") {
    type = "PlayervsAI";
  } else if (page == "/player") {
    type = "PlayervsPlayer";
    colour = "white";
  } else {
    type = document.getElementById("type").value;
    colour = document.getElementById("colour").value;
    ai = document.getElementById("aiChoice").value
  }

  // AI vs AI
  if (type == "AIvsAI") {
    
    document.getElementById("start").onclick = () => {
      var d = document.getElementById("wDepth");
      selfPlay(d.value);
      document.getElementById("start").style.display = "none";
      if (type == "AIvsAI") {
        document.getElementById("nextMove").removeAttribute("style");
      }
    };

    c = 0;
    document.getElementById("nextMove").onclick = () => {
      if (is_game_over) {
        alert("Game is over.");
        return false;
      }
      if (c % 2 == 0) {
        var wd = document.getElementById("wDepth");
        selfPlay(wd.value, "w");
      } else {
        var bd = document.getElementById("bDepth");
        selfPlay(bd.value, "b");
      }
      c += 1;
    };

    document.getElementById("ai").removeAttribute("style");
    document.getElementById("start").removeAttribute("style");
    document.getElementById("reset").removeAttribute("style");
    document.getElementById("colour").removeAttribute("style");
    document.getElementById("white").removeAttribute("style");
    document.getElementById("black").removeAttribute("style");
    document.getElementById("nextMove").style.display = "none";
    board = new Chessboard("board", {
      position: "start",
      orientation: colour,
    });
    jQuery.get("/reset", (response) => board.position(response));
    // Player vs AI
  } else if (type == "PlayervsAI") {
    
    document.getElementById("start").onclick = () => {
      var d = document.getElementById("wDepth");
      selfPlay(d.value);
      document.getElementById("start").style.display = "none";
      if (type == "AIvsAI") {
        document.getElementById("nextMove").removeAttribute("style");
      }
    };
    document.getElementById("ai").removeAttribute("style");
    document.getElementById("reset").removeAttribute("style");
    document.getElementById("colour").removeAttribute("style");
    document.getElementById("nextMove").style.display = "none";
    board = new Chessboard("board", {
      draggable: true,
      onDrop: onDrop,
      snapSpeed: 0,
      onDragStart: onDragStart,
      orientation: colour,
      position: "start",
    });
    // Black pieces
    if (colour == "black") {
      document.getElementById("black").style.display = "none";
      document.getElementById("white").removeAttribute("style");
      document.getElementById("start").removeAttribute("style");
    } else {
      document.getElementById("black").removeAttribute("style");
      document.getElementById("white").style.display = "none";
      document.getElementById("start").style.display = "none";
    }
    jQuery.get("/reset", (response) => board.position(response));
    // Player vs Player
  } else if (type == "PlayervsPlayer") {
    board = new Chessboard("board", {
      draggable: true,
      snapSpeed: 0,
      orientation: colour,
      position: "start",
    });
  }
  resetBoard();
  return board;
}

function resetBoard() {
  jQuery.get("/reset", (response) => board.position(response));
  createTable([])
}
