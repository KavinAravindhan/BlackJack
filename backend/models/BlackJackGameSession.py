from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BlackjackGameSession(db.Model):
    _tablename_ = 'Blackjack'
    _table_args_ = {'schema': 'GameSession_Schema'}  # Define schema

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