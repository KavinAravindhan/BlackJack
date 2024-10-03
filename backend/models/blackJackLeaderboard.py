class BlackjackLeaderboard(db.Model):
    _tablename_ = 'Blackjack'
    _bind_key_ = 'leaderboard_schema'  # Use the specific bind for this schema
    _table_args_ = {'schema': 'leaderboard_Schema'}

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