from typing import Dict
from flask import Flask, request
from lib.create_game_id import create_game_id
from game import Game
import logging

app = Flask(__name__, static_folder='../build', static_url_path='/')

# this is to keep track of all games, key is an id, value is the game...
games: Dict[int, Game] = {}

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/api/start')
def start():
    """
    this route creates a new game id, and creates a new game, passing in the ID
    """
    id = create_game_id(games)

    games[id] = id

    # create the new game, passing in the id
    game = Game(id)

    # add the game to the dictionary of games
    games[id] = game

    # get initial deal
    game.initial_deal()

    # return game id, and cards to JS
    if game.player.value == 21:
        game.dealer.dealer_show_all()

        player_cards = game.player.cards_as_json()
        player_value = game.player.value

        dealer_cards = game.dealer.cards_as_json()
        dealer_value = game.dealer.value

        game_winner = game.get_winner()

        games[id] = None

        return {
            "status": False,
            'player': {
                "cards": player_cards,
                "value": player_value
            },
            'dealer': {
                'cards': dealer_cards,
                "value": dealer_value
            },
            "winner": game_winner
        }
    

    return {
        'status': True,
        'player': {
            "cards": game.player.cards_as_json(),
            "value": game.player.value
        },
        'dealer': {
            'cards': game.dealer.cards_as_json(),
            "value": game.dealer.value
        },
        'game_id': id,
        'winner': False
    }


@app.route('/api/game_action/<game_id>', methods = ['GET', 'POST'])
def game_action(game_id):
    game_id = int(game_id)
    if game_id not in games.keys():
        return "fatal error"

    # get action json data
    data = request.get_json()

    game = games[game_id]

    print(data)

    # call necessary functions
    # game_over true if game is over
    game_over = game.action_input(data['action'])

    if game_over == True:
        # set all cards to appear for user feedback
        game.dealer.dealer_show_all()

        player_cards = game.player.cards_as_json()
        player_value = game.player.value

        dealer_cards = game.dealer.cards_as_json()
        dealer_value = game.dealer.value

        game_winner = game.get_winner()

        games.pop(game_id)

        return {
            "status": False,
            'player': {
                "cards": player_cards,
                "value": player_value
            },
            'dealer': {
                'cards': dealer_cards,
                "value": dealer_value
            },
            "winner": game_winner
        }

    # return newly dealt cards
    return {
        'status': True, 
        'player': {
            "cards": game.player.cards_as_json(),
            "value": game.player.value
        },
        'dealer': {
            'cards': game.dealer.cards_as_json(),
            "value": game.dealer.value
        },
        'winner': False
    }

@app.route('/api/make-bet')
def make_bet():
    data = request.get_json()

    bet = data.bet

    # make call to game bet functionality here


if __name__ == '__main__':
    app.run()
