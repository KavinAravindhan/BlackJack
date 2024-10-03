from typing import Dict
from flask import Flask, request, jsonify
from lib.create_game_id import create_game_id
from game import Game
from flask_sqlalchemy import SQLAlchemy
# from models import BlackjackGameSession
# import pymysql
# pymysql.install_as_MySQLdb()
# from models.credentials_User import Credentials
# from models.blacJack_Leaderboard import BlackjackLeaderboard
import logging

app = Flask(__name__, static_folder='../build', static_url_path='/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Ronitt:ceaser2720@casino-mysql-db.cuzrmwzagzwy.us-east-1.rds.amazonaws.com/GameSession_Schema'

app.config['SQLALCHEMY_BINDS'] = {
    'user_schema': 'mysql+pymysql://Ronitt:ceaser2720@casino-mysql-db.cuzrmwzagzwy.us-east-1.rds.amazonaws.com/User_Schema',
    'leaderboard_schema': 'mysql+pymysql://Ronitt:ceaser2720@casino-mysql-db.cuzrmwzagzwy.us-east-1.rds.amazonaws.com/leaderboard_Schema'
}


app.config['SQL_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print("\n DATABASE CONNECTION ESTABLISHED SUCCESSFULLY \n")

class BlackjackGameSession(db.Model):
    __tablename__ = 'Blackjack'
    __table_args__ = {'schema': 'GameSession_Schema'}  # Define schema

    Session_id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255))
    Bet_Amount = db.Column(db.Float)

    def _init_(self, Session_id, Username, Bet_Amount):
        self.Session_id = Session_id
        self.Username = Username
        self.Bet_Amount = Bet_Amount

    def to_dict(self):
        return {
            'Session_id': self.Session_id,
            'Username': self.Username,
            'Bet_Amount': self.Bet_Amount
        }
    
class BlackjackLeaderboard(db.Model):
    __tablename__ = 'Blackjack'
    __bind_key__ = 'leaderboard_schema'  # Use the specific bind for this schema
    __table_args__ = {'schema': 'leaderboard_Schema'}

    Score = db.Column(db.Integer)
    Username = db.Column(db.String(255), primary_key=True)
    Name = db.Column(db.String(255))

    def _init_(self, Score, Username, Name):
        self.Score = Score
        self.Username = Username
        self.Name = Name

    def to_dict(self):
        return {
            'Score': self.Score,
            'Username': self.Username,
            'Name': self.Name
        }
    
class Credentials(db.Model):
    __tablename__ = 'Credentials'
    __bind_key__ = 'user_schema'  # Use the specific bind for this schema
    __table_args__ = {'schema': 'User_Schema'}

    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, nullable=False)

    def _init_(self, username, password, name, balance):
        self.username = username
        self.password = password
        self.name = name
        self.balance = balance

    def to_dict(self):
        return {
            'userID': self.userID,
            'username': self.username,
            'name': self.name,
            'balance': self.balance
        }

@app.route('/blackjack/sessions', methods=['GET'])
def get_blackjack_sessions():
    sessions = BlackjackGameSession.query.all()
    return jsonify([session.to_dict() for session in sessions])

@app.route('/users/credentials', methods=['GET'])
def get_credentials():
    users = Credentials.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/blackjack/leaderboard', methods=['GET'])
def get_blackjack_leaderboard():
    leaderboard = BlackjackLeaderboard.query.all()
    return jsonify([entry.to_dict() for entry in leaderboard])

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
