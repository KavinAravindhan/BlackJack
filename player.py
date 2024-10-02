import json

from card import Card

# player class


class Player:

    def __init__(self, dealer: bool) -> None:
        # self.player = Player
        self.cards = []
        self.is_dealer = dealer
        self.value = 0

    def add_card(self, card: Card):
        if self.is_dealer == True and len(self.cards) == 0:
            card.change_visiblity(True)
        elif self.is_dealer == True and len(self.cards) > 0:
            card.change_visiblity(False)

        self.cards.append(card)

        # If card is Ace add 11
        if (card.value == "Ace"):
            self.value += 11
            # If that would lead to player busting, turn it to 1 instead
            if self.value > 21:
                self.value -= 10
        # Every other card
        else:
            self.value += card.value

    def cards_as_json(self):
        # handle change in react
        return [card.json() for card in self.cards]

    def dealer_show_all(self):
        """
        this function sets the dealers first card to be visible, and all cards insvisible
        """
        if self.is_dealer == True:
            for card in self.cards:
                card.change_visiblity(True)

