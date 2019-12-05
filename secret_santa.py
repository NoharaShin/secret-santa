"""Class to determines randomly the giver-receiver pairs of a Secret Santa event given a list of participants."""

import random

import pandas as pd


class SecretSanta(object):
    def __init__(self, participants_path=None):
        if participants_path:
            self.load_participants(participants_path)
        else:
            self.participants = participants_path

    def load_participants(self, filepath):
        """
        Read the CSV file located at the provided path, load it as a pandas DataFrame
        and assign it to the member `participants` of the class.
        :param filepath: Absolute path to the CSV file containing the list of participants.
        :type filepath: str
        """
        self.participants = pd.read_csv(filepath)

    def shuffle(self, simple_mode=True):
        """
        Shuffle randomly the participants to determine gift giver-receiver pairs.
        :param simple_mode: Value of the participants shuffle mode. If set to `True`, the simple shuffle mode is
            selected and the giver-receiver pairs are determined based on participant names only, else the shuffle
            is made based on external parameters such as the team, affinity between participants, etc...
        :type simple_mode: bool
        """
        if simple_mode:
            return self._shuffle_by_name()

    def _shuffle_by_name(self):
        participants = self.participants['name']
        givers = []
        receivers = []

        for participant in participants:
            if participant not in givers:
                givers.append(participant)

            try:
                receiver = random.choice(list(set(participants) - set(receivers) - {participant}))
                receivers.append(receiver)
            except IndexError:
                # This exception is raised when there is no more gift receiver to assign to the last giver but itself.
                # In this case, we need to switch randomly the last receiver (which is the giver) with another one.
                temp = random.choice(receivers)
                receivers[receivers.index(temp)] = participant
                receivers.append(temp)

        return givers, receivers
