import unittest
from lib import DFA, NFA


class TestNFAToDFA(unittest.TestCase):
    def test_nfa_to_dfa(self):
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

        self.assertIsInstance(dfa, DFA)
        self.assertEqual(dfa.get_alphabet(), '01')
        self.assertEqual(dfa.get_states(), {
            'e', '{q0,q2}', '{q0}', '{q0,q1}'
        })
        self.assertEqual(dfa.get_initial_state(), '{q0}')
        self.assertEqual(dfa.get_final_states(), {'{q0,q2}'})
        self.assertEqual(dfa.get_transitions(), {
            '{q0}': {'0': '{q0,q1}', '1': '{q0}'},
            '{q0,q1}': {'0': '{q0,q1}', '1': '{q0,q2}'},
            '{q0,q2}': {'0': '{q0,q1}', '1': '{q0}'},
            'e': {'0': 'e', '1': 'e'}
        })


if __name__ == '__main__':
    unittest.main()
