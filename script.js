//When window loads, set the board position.
window.onload = function () {
  path = window.location.pathname
  board = createBoard();
  is_game_over = false;
  jQuery.get("/current_board_state", (response) => board.position(response));
  c = 0;
  if (path != "/player") {
    document.getElementById("nextMove").onclick = () => {
      var bd = document.getElementById("bDepth");
      var wd = document.getElementById("wDepth");
      if (c % 2 == 0) {
        selfPlay(wd.value, "w");
      } else {
        selfPlay(bd.value, "b");
      }
      c += 1;
      if (is_game_over) {
        alert("Game is over.");
        return false;
      }
    };
    document.getElementById("start").onclick = () => {
      var d = document.getElementById("wDepth");
      selfPlay(d.value);
      document.getElementById("start").display = "none";
    };
  }
};

function get_board_orientation() {
  return board.orientation;
}

function get_history(moves) {
  var history_element = $('#history').empty();
  history_element.empty();
  for (var i = 0; i < moves.length; i += 2) {
    history_element.append('<span>' + moves[i] + ' ' + ( moves[i + 1] ? moves[i + 1] : ' ') + '</span><br>')
  }
  history_element.scrollTop(history_element[0].scrollHeight);
};

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
  
  jQuery.get(
    "/move",
    {
      source: get_pos(source),
      target: get_pos(target),
      promotion: p,
      depth: d.value,
    },
    function (response) {
      board.position(response);
    }
  );

  jQuery.get("/past_moves", function (response) {
    console.log(response)
    response = response.substring(2, response.length-2);
    response = response.split("', '");
    console.log(response)
    // response.forEach(function(part, index) {
    //   this[index] = this[index].substring(1, this[index].length-1);
    // }, response);
    get_history(response)
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

function selfPlay(d, p) {
  if (p == "w") {
    // White Move
    jQuery.get(
      "/selfplay",
      {
        depth: d,
        player: "w"
      },
      function (response) {
        board.position(response);
      }
    );
  } else {
    // Black Move
    jQuery.get(
      "/selfplay",
      {
        depth: d,
        player: "b"
      },
      function (response) {
        board.position(response);
      }
    );
  }
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
  
  if (page == "/ai") {
    type = "PlayervsAI";
  } else if (page == "/player") {
    type = "PlayervsPlayer";
    colour = "white";
  } else {
    type = document.getElementById("type").value;
    colour = document.getElementById("colour").value;
  }

  is_game_over = false;
  board = null;
  if (type == "PlayervsPlayer") {
    document.getElementById("ai").style.display = "none";
    document.getElementById("start").style.display = "none";
    document.getElementById("reset").style.display = "none";
    document.getElementById("colour").style.display = "none";
    document.getElementById("white").style.display = "none";
    document.getElementById("black").style.display = "none";
    document.getElementById("nextMove").style.display = "none";

  } else if (type == "PlayervsAI") {
    if (colour == "black") {
      document.getElementById("ai").removeAttribute("style");
      document.getElementById("start").removeAttribute("style");
      document.getElementById("reset").removeAttribute("style");
      document.getElementById("colour").removeAttribute("style");
      document.getElementById("white").removeAttribute("style");
      document.getElementById("black").removeAttribute("style");
      document.getElementById("nextMove").removeAttribute("style");
    } else {
      document.getElementById("start").style.display = "none";
    }
  } else {
    board = new Chessboard("board", {
      position: "start",
      orientation: colour,
    });
    document.getElementById("black").removeAttribute("style");
    document.getElementById("white").removeAttribute("style");
    document.getElementById("nextMove").removeAttribute("style");
    document.getElementById("start").style.display = "none";
    jQuery.get("/reset", (response) => board.position(response));
    // Player vs AI
  } else if (type == "PlayervsAI") {
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
    document.getElementById("nextMove").style.display = "none";
    jQuery.get("/reset", (response) => board.position(response));
    // Player vs Player
  } else if (type == "PlayervsPlayer") {
    board = new Chessboard("board", {
      draggable: true,
      snapSpeed: 0,
      orientation: colour,
      position: "start",
    });
    // document.getElementById("AIvsAI").style.display = "none";
    jQuery.get("/reset", (response) => board.position(response));
  }
  return board;
}
