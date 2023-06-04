from flask import Flask, render_template, request, redirect, url_for
import random
app = Flask(__name__)
winning_point = 20
current_player = None


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn = False
        self.running_score = 0


players = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_game', methods=['POST'])
def new_game():
    global players
    player1 = Player(request.form['player1_name'])
    player2 = Player(request.form['player2_name'])
    players = [player1, player2]
    players[0].turn = True
    for player in players:
        player.score = 0
    return redirect(url_for('game'))


@app.route('/game', methods=['GET', 'POST'])
def game():
    global players
    current_player = get_current_player()
    dice_value = 0
    # if current_player is None:  # 如果当前玩家为空，则选择第一个玩家
    #     current_player = players[0]
    if request.method == 'POST':
        # print(request.form)
        choice = request.form['choice']
        if choice == 'roll':
            dice_value = RollDice()
            if dice_value == 1:
                current_player.running_score = 0
                current_player.score = 0
                switch_turn()
                current_player = get_current_player()  # 更新当前玩家
            else:
                current_player.score += dice_value
                current_player.running_score = current_player.score  # 试一下
                if current_player.score >= winning_point:
                    # current_player.running_score = current_player.score  # 试一下
                    return redirect(url_for('winner'))
                else:
                    return render_template('game.html', players=players, current_player=current_player, dice_value=dice_value)

        elif choice == 'hold':
            switch_turn()
            current_player = get_current_player()
            current_player.score = current_player.running_score
            current_player.running_score = 0  # reset running score to 0 after holding
            if current_player.score >= winning_point:
                current_player.running_score = current_player.score  # 试一下
                return redirect(url_for('winner'))
    # return render_template('game.html', players=players, current_player=current_player)
        return render_template('game.html', players=players, current_player=current_player, dice_value=dice_value)
    else:
        # dice_value = 0  # just add for testing reset dice value to 0 after holding
        return render_template('game.html', players=players, current_player=current_player)


@app.route('/winner')
def winner():
    global players
    winner_player = get_current_player()
    return render_template('winner.html', winner=winner_player)


@app.route('/exit')
def exit():
    global players
    players = []
    return redirect(url_for('index.html'))


def RollDice():
    dice_value = random.randint(1, 6)
    return dice_value


def get_current_player():
    for player in players:
        if player.turn:
            return player

# hold switch


def switch_turn():
    global players
    current_player = get_current_player()
    current_player_index = players.index(current_player)
    current_player.turn = False
    next_player_index = (current_player_index + 1) % len(players)
    next_player = players[next_player_index]
    next_player.turn = True
    # current_player = get_current_player()


if __name__ == '__main__':
    app.run(debug=True)
