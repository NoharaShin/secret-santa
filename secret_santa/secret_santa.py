"""
Module to determine randomly (given a list of participants) the pairs of present giver-receiver of a Secret Santa.
The list of participants should be a pandas DataFrame.
Determining the pairs of present giver-receiver can be made over 6 exclusion criteria at most,
i.e. the name of the participants plus uo to 5 more additional exclusion criteria.
"""
import random

import pandas as pd

from models.santa_pair import SantaPair


def shuffle(participants: pd.DataFrame, simple_mode: bool = True, criteria: int = None) -> list:
    """
    Shuffle randomly the participants to determine gift giver-receiver pairs.
    :param participants: Pandas DataFrame listing out the participants to the Secret Santa.
    :param simple_mode: Value of the participants shuffle mode. If set to `True`, the simple shuffle is selected
        and the giver-receiver pairs are determined based on participant names only, else the shuffle is made
        based on the team and department.
    :param criteria: Number of criteria over which to perform the shuffle. The default value is None and in that case,
        the number of criteria is inferred from the number of columns of the `participants` DataFrame
        (i.e. the column `name` plus all the remaining columns). If provided, the value of `criteria`
        must be lower than 5. If `simple_mode` is set to True, `criteria` is not taken into consideration as
        the shuffle is going to be made over the column `name` only.
    :return: The list of named tuples `SantaPair` representing a pair of gift giver and his/her respective receiver.
    """
    participants = _rename_columns(participants)

    if simple_mode:
        givers, receivers = _shuffle_by_name(participants)
    else:
        if criteria < 0 or criteria > 5:
            raise ValueError(f"Wrong value for argument `criteria`: expected positive number lower or equal to 5, "
                             f"got {criteria} instead.")

        criteria = len(participants.columns) if not criteria else criteria
        givers, receivers = _shuffle_by_criteria(participants, criteria)

    return [SantaPair(*pair) for pair in list(zip(givers, receivers))]


def _shuffle_by_name(participants: pd.DataFrame) -> (list, list):
    """
    Internal function to shuffle randomly the participants by name and determine gift giver-receiver pairs.
    :param participants: Pandas DataFrame listing out the participants to the Secret Santa.
    :return: The list of named tuples `SantaPair` representing a pair of gift giver and his/her respective receiver.
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


def _shuffle_by_criteria(participants: pd.DataFrame, criteria: int) -> (list, list):
    """
    Internal function to shuffle randomly the participants by name and other citeria (and determine gift giver-receiver pairs.
    :param participants: Pandas DataFrame listing out the participants to the Secret Santa.
    :return: The list of named tuples `SantaPair` representing a pair of gift giver and his/her respective receiver.
    """
    givers, receivers = list(), list()
    for index, participant in participants.iterrows():
        if participant["name"] not in givers:
            givers.append(participant["name"])

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
    Internal function to rename or add a header to the participants pandas DataFrame. Used by the function
    _shuffle_by_criteria().
    :param participants: DataFrame of all the participants to the Secret Santa.
    :return: The input DataFrame with a new header.
    """
    new_columns = {participants.columns[0]: "name"}
    for i in range(1, len(participants.columns)):
        new_columns[participants.columns[i]] = f"criterion-{i}"

    return participants.rename(columns=new_columns)
