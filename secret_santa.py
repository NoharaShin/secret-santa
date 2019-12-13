"""Class to determines randomly the giver-receiver pairs of a Secret Santa event given a list of participants."""

import random
from collections import namedtuple

import pandas as pd

SantaPair = namedtuple('SantaPair', 'Giver Receiver')


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
            is made based on the company, team, department and floor.
        :type simple_mode: bool
        :return: The list of named tuples `SantaPair` representing a pair of gift giver and his/her respective receiver.
        :rtype: list of SantaPair
        """
        if simple_mode:
            givers, receivers = self._shuffle_by_name()
        else:
            givers, receivers = self._shuffle_by_criteria()

        return [SantaPair(*pair) for pair in list(zip(givers, receivers))]

    def _shuffle_by_name(self):
        participants = self.participants['Name']
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

    def _shuffle_by_criteria(self):
        givers = []
        receivers = []

        for index, participant in self.participants.iterrows():
            if participant['Name'] not in givers:
                givers.append(participant['Name'])

            criteria = 4
            potential_receivers = []
            while not potential_receivers or criteria == 0:
                potential_receivers = self._get_potential_receivers(participant, criteria)
                potential_receivers = list(set(potential_receivers) - set(receivers) - {participant['Name']})
                criteria -= 1

            try:
                receiver = random.choice(potential_receivers)
                receivers.append(receiver)
            except IndexError:
                # This exception is raised when there is no more gift receiver to assign to the last giver but itself.
                # In this case, we need to switch randomly the last receiver (which is the giver) with another one.
                temp = random.choice(receivers)
                receivers[receivers.index(temp)] = participant
                receivers.append(temp)

        return givers, receivers

    def _get_potential_receivers(self, participant, criteria):
        """
        Return the list of names of the potential gift receivers for the provided participant considering the different
        number of criteria ('Company', 'Team', 'Department' and 'Floor'). The sorting of the criteria between brackets
        illustrates the importance of each criterion over the others by descending order.
        :param participant: The participant of the SecretSanta for whom to determine the list of possible receivers.
        :type participant: pandas.core.series.Series
        :param criteria: Number of criteria to consider to determine the list of possible receivers for the participant.
        :type criteria: int
        :return: The names of all the possible gift receivers for the provided participant.
        :rtype: pandas.core.series.Series
        """
        if criteria == 4:
            return self.participants.loc[
                (self.participants['Company'] != participant['Company'])
                & (self.participants['Team'] != participant['Team'])
                & (self.participants['Department'] != participant['Department'])
                & (self.participants['Floor'] != participant['Floor'])]['Name']
        elif criteria == 3:
            # Same company
            return self.participants.loc[
                (self.participants['Team'] != participant['Team'])
                & (self.participants['Department'] != participant['Department'])
                & (self.participants['Floor'] != participant['Floor'])]['Name']
        elif criteria == 2:
            # Same floor
            return self.participants.loc[
                (self.participants['Team'] != participant['Team'])
                & (self.participants['Department'] != participant['Department'])]['Name']
        else:
            # Same department
            return self.participants.loc[(self.participants['Team'] != participant['Team'])]['Name']
