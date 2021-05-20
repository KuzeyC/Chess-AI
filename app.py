#!/usr/bin/env python
import chess
import chess.svg
from board import Board
from flask import Flask, request, make_response, render_template

app = Flask(__name__)
game = Board()
moves = []

# Flask route for home page.


@app.route('/')
def index():
    game = Board()
    moves.clear()
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/ai')
def ai():
    game = Board()
    moves.clear()
    return render_template("ai.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/bots')
def bots():
    return render_template("bots.html")


@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")


@app.route('/player')
def player():
    game = Board()
    moves.clear()
    return render_template("player.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/updates')
def updates():
    return render_template("updates.html")


@app.route("/reset")
def reset():
    game.board.reset()
    moves.clear()
    return make_response(game.board.fen())


# Return if the game is over or not.
@app.route('/is_game_over')
def is_game_over():
    return str(game.board.is_game_over())


# Return current board state.
@app.route('/current_board_state')
def current_board_state():
    return make_response(game.board.fen())

# Return current board pgn.


@app.route('/past_moves')
def past_moves():
    return make_response(str(moves))


# Flask route for moving the pieces.
@app.route('/move')
def move():
    # print(game.board.piece_map())
    # Get the source and target of the piece moved by a request.
    source = int(request.args.get('source'))
    target = int(request.args.get('target'))
    depth = int(request.args.get('depth'))
    ai = request.args.get('ai')
    # Create a san board state move with source and target.
    move = chess.Move(
        source, target, promotion=chess.QUEEN if request.args.get('promotion') == "true" else None)
    print("User's Move: " + str(move))
    if move in list(game.board.legal_moves):
        try:
            moves.append(game.board.san(move))
            game.board.push(move)

            comp_move = game.comp_move(depth, ai)
            moves.append(game.board.san(comp_move))
            game.board.push(comp_move)
        except Exception as e:
            print(e)

    # Return response.
    return make_response(game.board.fen())


@app.route('/selfplay')
def self_play_move():
    depth = int(request.args.get('depth'))
    player = request.args.get('player')
    ai = request.args.get('ai')
    print(depth, player, ai)
    try:
        comp_move = game.comp_move(depth, ai)
        moves.append(game.board.san(comp_move))
        game.board.push(comp_move)
    except Exception as e:
        print(e)

    # Return response.
    return make_response(game.board.fen())


# Create new Flask Application.
if __name__ == '__main__':
    app.run(debug=True)
