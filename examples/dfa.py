import os
import sys
sys.path.append(os.path.normpath(os.getcwd()))
from lib import DFA

if __name__ == '__main__':
    automata = DFA(
        alphabet='01',
        states={'q0', 'q1'},
        initial_state='q0',
        final_states={'q1'},
        transitions={
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q1', '1': 'q0'},
        }
    )

    print(automata.accepted('0001011'))
