from deck import Deck
from player import Player

"""
Game class represents a game of blackjack
"""


class Game():
    def __init__(self, id) -> None:
        self.id = id
        self.player = Player(dealer=False)
        self.dealer = Player(dealer=True)
        self.deck = Deck()
        self.game_over = False

    def initial_deal(self):
        player_card1 = self.deck.deal()
        player_card2 = self.deck.deal()

        dealer_card1 = self.deck.deal()
        dealer_card2 = self.deck.deal()

        self.player.add_card(player_card1)
        self.player.add_card(player_card2)

        self.dealer.add_card(dealer_card1)
        self.dealer.add_card(dealer_card2)
    
    def action_input(self, action):
        """
        returns true if game over, false if game not over
        """
        # dealer action
        if self.dealer.value < 17:
            new_card = self.deck.deal()
            self.dealer.add_card(new_card)

        if action == "hit":
            new_card = self.deck.deal()
            self.player.add_card(new_card)
        elif action == "stay":
            while self.dealer.value < 17:
                new_card = self.deck.deal()
                self.dealer.add_card(new_card)
            return True
        else:
            return "error occurred"

        # check game conditions
        game_over = self.check_game_over()

        # if we haven't returned, game is not over, continue game flow
        return game_over

    def check_game_over(self):
        # check if player over 21
        if self.player.value > 21 or self.dealer.value > 21:
            return True

        else:
            return False

    def get_winner(self):
        """This function returns the winner of the game"""
        self.game_over = True

        # Player over 21 and dealer 21 or under
        if self.player.value > 21 and self.dealer.value <= 21:
            return "dealer"
        # Dealer over 21 and player 21 or under
        if self.dealer.value > 21 and self.player.value <= 21:
            return "player"
        if self.player.value == 21 and self.dealer.value < self.player.value:
            return "player"
        if self.dealer.value == 21 and self.player.value < self.dealer.value:
            return "dealer"
        # Both dealer and player over 21
        if self.dealer.value > 21 and self.player.value > 21:
            return "tie"
        # Dealer and player same value
        if self.dealer.value == self.player.value:
            return "tie"
        # Dealer higher value
        if self.dealer.value > self.player.value:
            return "dealer"
        # Player higher value
        if self.dealer.value < self.player.value:
            return "player"

    def get_cards(self):
        return {
            "player": self.player.cards_as_json(),
            "dealer": self.dealer.cards_as_json()
        }
