import os

from secret_santa import SecretSanta

if __name__ == '__main__':
    input_path = os.path.abspath(os.path.join('', 'test', 'input', 'participants.csv'))
    santa = SecretSanta(input_path)

    santa_pairs = santa.shuffle(simple_mode=False)
    givers = [santa_pair.Giver for santa_pair in santa_pairs]
    receivers = [santa_pair.Receiver for santa_pair in santa_pairs]

    print(santa_pairs)
    print(givers)
    print(receivers)
