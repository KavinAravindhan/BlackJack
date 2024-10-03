# deck class

import random
from card import Card

# list containing the suits
suitsList = ["Spades", "Clubs", "Diamonds", "Hearts"]


class Deck:

    # initializer
    def __init__(self):
        # empty array to hold cards
        self.cards = []
        self.buildDeck()

    # create a deck of cards using Card class
    def buildDeck(self):
        # iterate through suits and then values 2 - 14
        for s in suitsList:
            for i in range(2, 15):
                # anything 10 or higher is automatically a 10
                if i <= 9:
                    self.cards.append(Card(s, i))
                # any card that is an 11 is automatically and Ace
                # Ace card will be handled in player class
                elif i == 11:
                    self.cards.append(Card(s, "Ace"))
                else:
                    self.cards.append(Card(s, 10))

    # randomly deal a single card
    def deal(self):
        # get a random card using a random index
        randIndex = random.randrange(len(self.cards))
        dealtCard = self.cards[randIndex]

        # remove that card from the deck
        self.cards.remove(dealtCard)

        # return (deal) the randomly selected card
        return dealtCard
