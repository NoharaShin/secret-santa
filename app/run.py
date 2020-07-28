import os
from pathlib import Path

import pandas as pd

import secret_santa


if __name__ == "__main__":
    input_path = os.path.abspath(os.path.join(Path().resolve().parent, 'data', 'example.csv'))
    participants = pd.read_csv(input_path)

    santa_pairs = secret_santa.shuffle(participants, False)
    givers, receivers = list(), list()
    for santa_pair in santa_pairs:
        givers.append(santa_pair.giver)
        receivers.append(santa_pair.receiver)

    print(givers)
    print(receivers)
