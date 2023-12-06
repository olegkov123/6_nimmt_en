import numpy as np

class Player:
    """Player class for a card game. Manages the cards and points for a player."""

    def __init__(self, cards: list):
        """
        Player class constructor. Takes a list of cards as an argument.

        Parameters:
        - cards (list): The list of cards that the player starts with.
        """
        if len(cards) != 10:
            raise ValueError("The player must have 10 cards.")  # Raise exception if the card count is not 10.

        # Initialize an array of zeros for the cards (0 denotes absence of a card).
        self.cards = np.zeros(105, dtype=int)

        # Set the value 1 for indices corresponding to the card numbers in the player's hand.
        for item in cards:
            self.cards[item] = 1

        # Store and sort the list of cards in the player's hand.
        self.hand = cards
        self.hand.sort()

        # Initialize the player's points to 0.
        self.points = 0

    def play_card(self, value: int):
        """
        Method to play a card.

        Parameters:
        - value (int): The card value to be played.
        """
        self.cards[value] = 0  # Set the corresponding index in the cards array to 0.
        self.hand[self.hand.index(value)] = None  # Remove the played card from the player's hand.

    def add_points(self, points: int):
        """
        Method to add points to the player.

        Parameters:
        - points (int): The points to be added.
        """
        self.points += points

    @property
    def cards_count(self) -> int:
        """
        Property to get the count of cards in the player's hand.

        Returns:
        - int: The number of cards in the player's hand.
        """
        return np.sum(self.cards)

    def describe(self) -> np.ndarray:
        """
        Method to describe the player's cards array (useful for debugging).

        Returns:
        - np.ndarray: The player's cards array.
        """
        return self.cards

    def __str__(self) -> str:
        """
        Method to represent the object as a string.

        Returns:
        - str: A string representation of the object.
        """
        return str([i for i, value in enumerate(self.cards) if value])

    def __repr__(self) -> str:
        """
        Method to represent the object when outputting a list of objects.

        Returns:
        - str: A string representation of the object.
        """
        return self.__str__()
