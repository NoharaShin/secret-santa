"""Class representing a pair of present giver and its respective receiver."""


class SantaPair(object):
    def __init__(self, giver: str, receiver: str):
        """
        :param giver: Name of the person giving the present.
        :param receiver: Name of the person receiving the present.
        """
        self.giver = giver
        self.receiver = receiver
