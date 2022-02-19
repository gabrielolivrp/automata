import os
import sys
sys.path.append(os.path.normpath(os.getcwd()))
from lib import NFA

if __name__ == '__main__':
    automata = NFA(
        states={'q0', 'q1', 'q2'},
        alphabet='ab',
        transitions={
            'q0': {'a': {'q1'}},
            'q1': {'a': {'q1'}, '': {'q2'}},
            'q2': {'b': {'q0'}}
        },
        initial_state={'q0'},
        final_states={'q1'}
    )

    print(automata.accepted('aba'))
