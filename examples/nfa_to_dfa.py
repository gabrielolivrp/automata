import os
import sys
sys.path.append(os.path.normpath(os.getcwd()))
from lib import NFA, DFA

if __name__ == '__main__':
    nfa = NFA(
        alphabet='01',
        states={'q0', 'q1', 'q2'},
        transitions={
            'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
            'q1': {'1': {'q2'}},
        },
        initial_state={'q0'},
        final_states={'q2'}
    )

    dfa = DFA.from_nfa(nfa)

    print(dfa)
