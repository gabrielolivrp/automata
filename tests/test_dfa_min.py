import unittest
from lib import DFA, DFAMin


class TestDFAMin(unittest.TestCase):
    def test_automaton_minification_must_be_correct(self):
        dfa = DFA(
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

        new_dfa = DFAMin(dfa).minify()

        self.assertIsInstance(new_dfa, DFA)
        self.assertEqual(new_dfa.get_alphabet(), 'ab')
        self.assertEqual(new_dfa.get_states(), {
            'q0', 'q1', '{q2,q3}', '{q4,q5}'
        })
        self.assertEqual(new_dfa.get_initial_state(), 'q0')
        self.assertEqual(new_dfa.get_final_states(), {'{q4,q5}', 'q0'})
        self.assertEqual(new_dfa.get_transitions(), {
            'q0': {'a': '{q2,q3}', 'b': 'q1'},
            'q1': {'a': 'q1', 'b': 'q0'},
            '{q2,q3}': {'a': '{q4,q5}', 'b': '{q4,q5}'},
            '{q4,q5}': {'a': '{q2,q3}', 'b': '{q2,q3}'}
        })


if __name__ == '__main__':
    unittest.main()
