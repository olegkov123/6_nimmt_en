import numpy as np
from random import shuffle

from library.player import Player
from library.desk import Desk
from library.deskLine import DeskLine
from library.card import Card

class Environment:
    """
    Environment Class: Represents the game environment.
    """

    def __init__(self, players: int):
        """
        Constructor for the Environment class.
        """
        self.desk = None  # The game desk/table
        self.players = None  # List of players
        self.old_cards = None  # Cards that have already been played
        self.COUNT_PLAYERS = players  # Number of players
        self.reset()  # Initialize the game

    def reset(self):
        """
        Method to initialize/reset the game state.
        """
        # Create and shuffle a deck of cards
        deck_of_cards = list(range(1, 105))
        shuffle(deck_of_cards)

        # Initialize the list of used cards
        self.old_cards = np.zeros(105, dtype=int)

        # Initialize players with selected cards
        self.players = []
        for _ in range(self.COUNT_PLAYERS):
            selected_values = [deck_of_cards.pop() for _ in range(10)]
            self.players.append(Player(selected_values))

        # Initialize the game desk
        desk_lines = [DeskLine(deck_of_cards.pop()) for _ in range(4)]
        self.desk = Desk(desk_lines)

        # Return the initial state
        input_shape = np.vstack([self.desk.describe, self.old_cards])
        return input_shape, [player.cards for player in self.players]

    def step(self, cards):
        """
        Method to perform a step in the game.
        """
        done = False
        info = ""
        rewards = np.zeros(self.COUNT_PLAYERS)
        sorted_cards = sorted(cards)

        # Players place their cards and get a response from the desk
        for card in sorted_cards:
            player_index = cards.index(card)
            self.players[player_index].play_card(card)
            penalty_line, penalty_orders = self.desk.add_card(card)

            # If the player had to pick up a line, penalty points are accounted for
            if penalty_orders is not None:
                self.players[player_index].add_points(penalty_orders)
                rewards[player_index] = -penalty_orders
                self._add_old_cards(penalty_line)

        # Check if it's the last step of the game
        remaining_cards = np.sum(self.players[0].cards)
        if remaining_cards < 1:
            done = True
            points = np.array(self._create_points_list())
            rewards = (points - np.amin(points)) * -1

        # Gather game state information
        input_shape = np.vstack([self.desk.describe, self.old_cards])
        return input_shape, [player.cards for player in self.players], rewards, done, info

    def _add_old_cards(self, cards):
        """
        Add used cards to the list.
        """
        for card in cards:
            if isinstance(card, Card):
                self.old_cards[card.value] = 1

    def _create_points_list(self):
        """
        Create a list of penalty points for each player.
        """
        return [player.points for player in self.players]

    def __repr__(self):
        """
        String representation of the game state.
        """
        res = "===================================\n"
        for i, player in enumerate(self.players):
            res += f"Player {i}: {player}\n"
        res += "===================================\n"
        res += "Desk:\n"
        res += str(self.desk)
        return res
