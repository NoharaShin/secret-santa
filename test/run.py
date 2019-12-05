import os

from secret_santa import SecretSanta

if __name__ == '__main__':
    input_path = os.path.abspath(os.path.join('', 'test', 'input', 'participants.csv'))
    santa = SecretSanta(input_path)
    for i in range(100):
        givers, receivers = santa.shuffle()
        print(givers, receivers)
