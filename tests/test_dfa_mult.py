import unittest
from lib import DFA, DFAMult


class TestDFAMult(unittest.TestCase):
    def setUp(self):
        self.dfa1 = DFA(
            alphabet='ab',
            states={'1', '2'},
            initial_state='1',
            final_states={'1'},
            transitions={
                '1': {'a': '2', 'b': '1'},
                '2': {'a': '1', 'b': '2'},
            }
        )

        self.dfa2 = DFA(
            alphabet='ab',
            states={'3', '4'},
            initial_state='3',
            final_states={'3'},
            transitions={
                '3': {'a': '3', 'b': '4'},
                '4': {'a': '4', 'b': '3'},
            }
        )

    def test_union(self):
        dfa_union = DFAMult(self.dfa1).union(self.dfa2)

        self.assertIsInstance(dfa_union, DFA)
        self.assertEqual(dfa_union.get_alphabet(), 'ab')
        self.assertEqual(dfa_union.get_states(), {
            '{1,4}', '{1,3}', '{2,4}', '{2,3}'
        })
        self.assertEqual(dfa_union.get_initial_state(), '{1,3}')
        self.assertEqual(dfa_union.get_final_states(), {
            '{1,4}', '{1,3}', '{2,3}'
        })
        self.assertEqual(dfa_union.get_transitions(), {
            '{1,4}': {'a': '{2,4}', 'b': '{1,3}'},
            '{1,3}': {'a': '{2,3}', 'b': '{1,4}'},
            '{2,4}': {'a': '{1,4}', 'b': '{2,3}'},
            '{2,3}': {'a': '{1,3}', 'b': '{2,4}'},
        })

    def test_difference(self):
        dfa_difference = DFAMult(self.dfa1).difference(self.dfa2)
        self.assertIsInstance(dfa_difference, DFA)
        self.assertEqual(dfa_difference.get_alphabet(), 'ab')
        self.assertEqual(dfa_difference.get_states(), {
            '{1,4}', '{1,3}', '{2,4}', '{2,3}'
        })
        self.assertEqual(dfa_difference.get_initial_state(), '{1,3}')
        self.assertEqual(dfa_difference.get_final_states(), {
            '{1,4}'
        })
        self.assertEqual(dfa_difference.get_transitions(), {
            '{1,4}': {'a': '{2,4}', 'b': '{1,3}'},
            '{1,3}': {'a': '{2,3}', 'b': '{1,4}'},
            '{2,4}': {'a': '{1,4}', 'b': '{2,3}'},
            '{2,3}': {'a': '{1,3}', 'b': '{2,4}'},
        })

    def test_intersection(self):
        dfa_intersection = DFAMult(self.dfa1).intersection(self.dfa2)
        self.assertIsInstance(dfa_intersection, DFA)
        self.assertEqual(dfa_intersection.get_alphabet(), 'ab')
        self.assertEqual(dfa_intersection.get_states(), {
            '{1,4}', '{1,3}', '{2,4}', '{2,3}'
        })
        self.assertEqual(dfa_intersection.get_initial_state(), '{1,3}')
        self.assertEqual(dfa_intersection.get_final_states(), {
            '{1,3}'
        })
        self.assertEqual(dfa_intersection.get_transitions(), {
            '{1,4}': {'a': '{2,4}', 'b': '{1,3}'},
            '{1,3}': {'a': '{2,3}', 'b': '{1,4}'},
            '{2,4}': {'a': '{1,4}', 'b': '{2,3}'},
            '{2,3}': {'a': '{1,3}', 'b': '{2,4}'},
        })


if __name__ == '__main__':
    unittest.main()
