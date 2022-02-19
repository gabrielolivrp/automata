import unittest
from lib import NFA


class TestEpsilonNFAToNFA(unittest.TestCase):
    def test_epsilon_nfa_to_nfa(self):
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

        self.assertIsInstance(nfa, NFA)
        self.assertEqual(nfa.get_alphabet(), 'ab')
        self.assertEqual(nfa.get_states(), {
            'q2', 'q0', 'q3', 'q1', 'q4'
        })
        self.assertEqual(nfa.get_initial_state(), {'q0'})
        self.assertEqual(nfa.get_final_states(), {'q1'})
        self.assertEqual(nfa.get_transitions(), {
            'q2': {'a': {'q1'}, 'b': {'q2', 'q4', 'q3', 'q1'}},
            'q0': {'a': {'q3', 'q1'}, 'b': {'q2', 'q4', 'q3', 'q1'}},
            'q3': {'a': {'q1'}, 'b': {'q2', 'q3', 'q1'}},
            'q1': {'a': {'q3'}},
            'q4': {'a': {'q4'}, 'b': {'q2', 'q3'}},
        })


if __name__ == '__main__':
    unittest.main()
