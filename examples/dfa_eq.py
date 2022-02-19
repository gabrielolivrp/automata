import os
import sys
sys.path.append(os.path.normpath(os.getcwd()))
from lib import DFA, DFAEq

if __name__ == '__main__':
    automata1 = DFA(
        alphabet='ab',
        states={'1', '2', '3'},
        initial_state='1',
        final_states={'2'},
        transitions={
            '1': {'a': '3', 'b': '2'},
            '2': {'a': '1', 'b': '2'},
            '3': {'a': '3', 'b': '2'},
        }
    )

    automata2 = DFA(
        alphabet='ab',
        states={'4', '5'},
        initial_state='4',
        final_states={'5'},
        transitions={
            '4': {'a': '5', 'b': '4'},
            '5': {'a': '4', 'b': '5'},
        }
    )

    print(DFAEq(automata1).equals(automata2))

