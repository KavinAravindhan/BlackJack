class Card:
    
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.visible = True
    
    def change_visiblity(self, visibility):
        self.visible = visibility
     
    def to_string(self):
        s = str(self.value) + " of " + self.suit
        return s

    def json(self):
        """
        returns array of card info, index 0 being value, index 1 being suit
        """
        return [
            self.value,
            self.suit,
            self.visible
        ]
