import numpy as np

class Card:
    """
    Card class to represent playing cards.
    """

    def __init__(self, value):
        """
        Initializes a Card object.

        Parameters:
            value (int): The value of the card.

        Raises:
            ValueError: If the value is not an integer or not in the range 0-104.
        """
        if not (isinstance(value, int) or isinstance(value, np.int64)):
            print(f"{value} is of type {type(value)}")
            raise ValueError("Value must be an integer")

        if value < 0 or value > 104:
            raise ValueError("Value must be in the range 0-104")

        self.value = value
        self._set_points()

    def _set_points(self):
        """
        Private method to set the point value of the card.
        """
        if self.value == 55:
            self.points = 7
        elif self.value % 11 == 0:
            self.points = 5
        elif self.value % 10 == 0:
            self.points = 3
        elif self.value % 5 == 0:
            self.points = 2
        elif self.value == 0:
            self.points = 0
        else:
            self.points = 1

    def __str__(self):
        """
        Returns a string representation of the Card object.

        Returns:
            str: The value of the card.
        """
        return f"{self.value}"

    def __repr__(self):
        """
        Returns a string representation of the Card object for use in lists.

        Returns:
            str: The value of the card.
        """
        return self.__str__()

    def __int__(self):
        """
        Converts the Card object to an integer.

        Returns:
            int: The value of the card.
        """
        return self.value
