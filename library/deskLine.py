import numpy as np
from library.card import Card

class DeskLine:
    # Constants: maximum number of cards in a line and on the table
    MAX_LENGTH = 5
    CARDS_IN_DESK = 104

    # DeskLine class constructor
    def __init__(self, card):
        self._input_init(card)

    # Property to get the number of cards in the line
    @property
    def length(self):
        return sum(1 for item in self.cards if isinstance(item, Card))

    # Property to get the sum of penalty points in the line
    @property
    def all_points(self):
        return sum(card.points for card in self.cards if isinstance(card, Card))

    # Property to get the maximum card value in the line
    @property
    def max(self):
        return max(card.value for card in self.cards if isinstance(card, Card))

    # Property to get an array describing the line
    @property
    def describe(self):
        res = np.zeros(105, dtype=int)
        for card in self.cards:
            if isinstance(card, Card):
                res[card.value] = 1
        return res

    # Adds a card to the line or replaces the line if it is full
    def add(self, card):
        if self.length == self.MAX_LENGTH:
            return self.change(card)
        else:
            if int(card) <= self.max:
                raise ValueError("This card cannot be added as it is smaller than the maximum card.")
            self.cards[self.length] = self.check_input(card)
            return None, None

    # Replaces the line with a new one
    def change(self, card):
        res = self.cards.copy()
        points = self.all_points
        self._input_init(card)
        return res, points

    # Checks the input to accept either a Card or an integer
    def check_input(self, value):
        if isinstance(value, Card):
            return value
        elif isinstance(value, int) or isinstance(value, np.int64):
            if 0 < value <= self.CARDS_IN_DESK:
                return Card(value)
        raise ValueError(f"This is neither a card nor an integer: {value}")

    # Initializes the line with a single card
    def _input_init(self, value):
        self.cards = [self.check_input(value), None, None, None, None]

    # Property to get the values of the cards in the line
    @property
    def card_values(self):
        return [card.value if card is not None else None for card in self.cards]

    # String representation of the line
    def __str__(self):
        return f"{self.cards}"
