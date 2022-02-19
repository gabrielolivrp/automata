import os
import sys
sys.path.append(os.path.normpath(os.getcwd()))
from lib import NFA

if __name__ == '__main__':
    nfa_epsilon = NFA(
        alphabet='ab',
        states={'q0', 'q1', 'q2', 'q3', 'q4'},
        transitions={
            'q0': {'': {'q1', 'q2'}},
            'q1': {'a': {'q3'}},
            'q2': {'a': {'q1'}, 'b': {'q4'}, '': {'q3'}},
            'q3': {'a': {'q1'}, 'b': {'q1', 'q2'}},
            'q4': {'a': {'q4'}, 'b': {'q2'}}

        },
        initial_state={'q0'},
        final_states={'q1'}
    )

    nfa = NFA.from_nfa_epsilon(nfa_epsilon)

    print(nfa)
