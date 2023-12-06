import numpy as np
from library.deskLine import DeskLine


class Desk:
    # Constructor of the Desk class
    def __init__(self, desklines: list[DeskLine]):
        self.desklines = desklines  # Initialize the lines on the desk

    # Method for adding a card to one of the lines
    def add_card(self, card):
        index = self._index_for_add(card)  # Find the index of the line to add the card to
        if index is None:
            # TODO: Add mechanism for line selection (possibly neural network)
            return self.desklines[self._minimum_points_index()].change(card)  # Modify the line with the minimum points
        else:
            return self.desklines[index].add(card)  # Add the card to the selected line

    # Returns a list of the maximum values for each line
    def _max_values(self):
        return [line.max for line in self.desklines]

    # Returns a list of the number of points in each line
    def _points(self):
        return [line.all_points for line in self.desklines]

    # Returns the index of the line with the minimum number of points
    def _minimum_points_index(self):
        points = self._points()
        return points.index(min(points))

    # Returns the index of the line where the card can be added, or None if none exists
    def _index_for_add(self, card):
        max_values = self._max_values()
        values_less_card = [item for item in max_values if item < int(card)]
        if values_less_card:
            return max_values.index(max(values_less_card))
        else:
            return None

    # Property that returns the description of the desk
    @property
    def describe(self):
        return np.vstack([line.describe for line in self.desklines])

    # String representation of the object
    def __repr__(self):
        return str([str(line) for line in self.desklines])
