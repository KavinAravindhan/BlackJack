class Credentials(db.Model):
    _tablename_ = 'Credentials'
    _bind_key_ = 'user_schema'  # Use the specific bind for this schema
    _table_args_ = {'schema': 'User_Schema'}

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