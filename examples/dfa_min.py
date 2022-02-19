import os
import sys
sys.path.append(os.path.normpath(os.getcwd()))
from lib import DFA, DFAMin

if __name__ == '__main__':
    automata = DFA(
        alphabet='ab',
        states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5'},
        initial_state='q0',
        final_states={'q0', 'q4', 'q5'},
        transitions={
            'q0': {'a': 'q2', 'b': 'q1'},
            'q1': {'a': 'q1', 'b': 'q0'},
            'q2': {'a': 'q4', 'b': 'q5'},
            'q3': {'a': 'q5', 'b': 'q4'},
            'q4': {'a': 'q3', 'b': 'q2'},
            'q5': {'a': 'q2', 'b': 'q3'},
        }
    )

    new_dfa = DFAMin(automata).minify()

    print(automata)
    print(new_dfa)
