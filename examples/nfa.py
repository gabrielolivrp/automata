import os
import sys
sys.path.append(os.path.normpath(os.getcwd()))
from lib import NFA

if __name__ == '__main__':
    automata = NFA(
        alphabet='01',
        states={'q0', 'q1', 'q2'},
        transitions={
            'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
            'q1': {'1': {'q2'}},
        },
        initial_state={'q0'},
        final_states={'q2'}
    )

    print(automata.accepted('000101'))
