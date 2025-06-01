from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Game state
board = [""] * 9
current_player = "X"
winner = None

def check_winner():
    global winner
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != "":
            winner = board[a]
            return winner
    if "" not in board:
        winner = "Draw"
        return "Draw"
    return None

def ai_move():
    available = [i for i, spot in enumerate(board) if spot == ""]
    if available:
        move = random.choice(available)
        board[move] = "O"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global current_player, board, winner
    if winner:
        return jsonify({"board": board, "winner": winner, "current_player": current_player})

    data = request.get_json()
    pos = data["position"]

    if board[pos] == "" and current_player == "X":
        board[pos] = "X"
        if check_winner():
            return jsonify({"board": board, "winner": winner, "current_player": current_player})

        # AI makes a move if game not over
        ai_move()
        check_winner()
    
    return jsonify({"board": board, "winner": winner, "current_player": "X"})

@app.route("/reset", methods=["POST"])
def reset():
    global board, current_player, winner
    board = [""] * 9
    current_player = "X"
    winner = None
    return ("", 204)

if __name__ == "__main__":
    app.run(debug=True)
