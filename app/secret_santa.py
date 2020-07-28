"""
Module to determine randomly (given a list of participants) the pairs of present giver-receiver of a Secret Santa.
The list of participants should be a pandas DataFrame.
"""
import random

import pandas as pd

from models.santa_pair import SantaPair


def shuffle(participants: pd.DataFrame, simple_mode: bool = True) -> list:
    """
    Shuffle randomly the participants to determine gift giver-receiver pairs.
    :param participants: Pandas DataFrame listing out the participants to the Secret Santa.
    :param simple_mode: Value of the participants shuffle mode. If set to `True`, the simple shuffle is selected
        and the giver-receiver pairs are determined based on participant names only, else the shuffle is made
        based on the team and department.
    :return: The list of named tuples `SantaPair` representing a pair of gift giver and his/her respective receiver.
    """
    participants = _rename_columns(participants)
    givers, receivers = _shuffle_by_name(participants) if simple_mode else _shuffle_by_criteria(participants)

    return [SantaPair(*pair) for pair in list(zip(givers, receivers))]


def _shuffle_by_name(participants: pd.DataFrame) -> (list, list):
    """
    :param participants: Pandas DataFrame listing out the participants to the Secret Santa.
    :return:
    """
    participants = participants["name"]
    givers, receivers = list(), list()

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


def _shuffle_by_criteria(participants: pd.DataFrame):
    """

    :param participants: Pandas DataFrame listing out the participants to the Secret Santa.
    :return:
    """
    givers, receivers = list(), list()
    for index, participant in participants.iterrows():
        if participant["name"] not in givers:
            givers.append(participant["name"])

        criteria = 2
        potential_receivers = []
        while not potential_receivers or criteria == 0:
            potential_receivers = _get_potential_receivers(participants, participant, criteria)
            potential_receivers = list(set(potential_receivers) - set(receivers) - {participant["name"]})
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


def _get_potential_receivers(participants: pd.DataFrame, participant: pd.Series, criteria: int) -> pd.Series:
    """
    Return the list of names of the potential gift receivers for the provided participant considering the different
    number of criteria ('Team' and 'Department'). The sorting of the criteria between brackets
    illustrates the importance of each criterion over the others by descending order.
    :param participant: The participant of the SecretSanta for whom to determine the list of possible receivers.
    :param criteria: Number of criteria to consider to determine the list of possible receivers for the participant.
    :return: The names of all the possible gift receivers for the provided participant.
    """
    if criteria == 5:
        return participants.loc[
            (participants["criterion-5"] != participant["criterion-5"])
            & (participants["criterion-4"] != participant["criterion-4"])
            & (participants["criterion-3"] != participant["criterion-3"])
            & (participants["criterion-2"] != participant["criterion-2"])
            & (participants["criterion-1"] != participant["criterion-1"])]["name"]
    if criteria == 4:
        return participants.loc[
            (participants["criterion-4"] != participant["criterion-4"])
            & (participants["criterion-3"] != participant["criterion-3"])
            & (participants["criterion-2"] != participant["criterion-2"])
            & (participants["criterion-1"] != participant["criterion-1"])]["name"]
    if criteria == 3:
        return participants.loc[
            (participants["criterion-3"] != participant["criterion-3"])
            & (participants["criterion-2"] != participant["criterion-2"])
            & (participants["criterion-1"] != participant["criterion-1"])]["name"]
    if criteria == 2:
        return participants.loc[
            (participants["criterion-2"] != participant["criterion-2"])
            & (participants["criterion-1"] != participant["criterion-1"])]["name"]
    else:
        return participants.loc[(participants["criterion-1"] != participant["criterion-1"])]["name"]


def _rename_columns(participants: pd.DataFrame) -> pd.DataFrame:
    """

    :param participants:
    :return:
    """
    new_columns = {participants.columns[0]: "name"}
    for i in range(1, len(participants.columns)):
        new_columns[participants.columns[i]] = f"criterion-{i}"

    return participants.rename(columns=new_columns)
