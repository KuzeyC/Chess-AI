"use strict";

//When window loads, set the board position.
window.onload = function () {
  board = createBoard();
  is_game_over = false;
  jQuery.get("/current_board_state", function (response) {
    return board.position(response);
  });
}; //Rows for the chess board. Position of the pieces 0-63.


function get_pos(s) {
  return 8 * (parseInt(s[1]) - 1) + "abcdefgh".indexOf(s[0]);
} //Using jquery to request position of the source and the target of the move and using the response to make a move.


function onDrop(source, target, piece, newPos, oldPos, orientation) {
  if (source == target) {
    return;
  }

  var p = orientation == "white" && target.charAt(1) == "8" && piece.charAt(1) == "P" || orientation == "black" && target.charAt(1) == "1" && piece.charAt(1) == "P";
  jQuery.get("/move", {
    source: get_pos(source),
    target: get_pos(target),
    promotion: p
  }, function (response) {
    board.position(response);
  });
  isGameOver();
} //When a piece is beginning to be dragged.


function onDragStart(source, piece, position, orientation) {
  if (orientation == "black" && piece.search(/^w/) !== -1) return false;
  if (orientation == "white" && piece.search(/^b/) !== -1) return false; // getLegalMoves();

  if (is_game_over) {
    alert("Game is over.");
    return false;
  }
}

function selfPlay() {
  function selfPlayMove() {
    jQuery.get("/selfplay", function (response) {
      return board.position(response);
    });
    isGameOver();
  }

  window.setTimeout(selfPlayMove, 500);
} // Check if the game is over or not function.


function isGameOver() {
  jQuery.get("/is_game_over", function (response) {
    if (response == "True") {
      is_game_over = true;
    }
  });
} // Creating the board function.


function createBoard() {
  var colour = document.forms["colourForm"]["colour"].value;
  var type = document.forms["gameType"]["type"].value;
  console.log(colour);
  console.log(type);
  is_game_over = false;
  board = null;

  if (type == "AIvsAI") {
    board = new Chessboard("board", {
      position: "start",
      orientation: colour
    });
    jQuery.get("/reset", function (response) {
      return board.position(response);
    }); // selfPlay();
  } else if (type == "PlayervsAI" || type == "PlayervsPlayer") {
    board = new Chessboard("board", {
      draggable: true,
      onDrop: onDrop,
      snapSpeed: 0,
      onDragStart: onDragStart,
      orientation: colour,
      position: "start"
    });
    jQuery.get("/reset", function (response) {
      return board.position(response);
    });
  }

  return board;
}