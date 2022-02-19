import os
import sys
sys.path.append(os.path.normpath(os.getcwd()))
from lib import DFA, DFAMult


if __name__ == '__main__':
    automata1 = DFA(
        alphabet='ab',
        states={'1', '2'},
        initial_state='1',
        final_states={'1'},
        transitions={
            '1': {'a': '2', 'b': '1'},
            '2': {'a': '1', 'b': '2'},
        }
    )

    automata2 = DFA(
        alphabet='ab',
        states={'3', '4'},
        initial_state='3',
        final_states={'3'},
        transitions={
            '3': {'a': '3', 'b': '4'},
            '4': {'a': '4', 'b': '3'},
        }
    )

    print("=> Automata 1")
    print(automata1)

    print("=> Automata 2")
    print(automata2)

    print("=> Intersection")
    print(DFAMult(automata1).intersection(automata2))

    print("=> Union")
    print(DFAMult(automata1).union(automata2))

    print("=> Difference")
    print(DFAMult(automata1).difference(automata2))

    print("=> Complement")
    print(automata1.complement())
