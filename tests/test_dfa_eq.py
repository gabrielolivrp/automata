import unittest
from lib import DFA, DFAEq


class TestDFAEq(unittest.TestCase):
    def test_automata_must_be_equivalent(self):
        dfa1 = DFA(
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

        self.assertTrue(DFAEq(dfa1).equals(dfa1))

    def test_automata_must_not_be_equivalent(self):
        dfa1 = DFA(
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

        dfa2 = DFA(
            alphabet='ab',
            states={'4', '5'},
            initial_state='4',
            final_states={'5'},
            transitions={
                '4': {'a': '5', 'b': '4'},
                '5': {'a': '4', 'b': '5'},
            }
        )

        self.assertFalse(DFAEq(dfa1).equals(dfa2))


if __name__ == '__main__':
    unittest.main()
