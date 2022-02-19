import unittest
from lib import DFA, InvalidSymbolError


class TestDFA(unittest.TestCase):
    def setUp(self):
        # Automata: Odd numbers of 1s
        self.automata = DFA(
            alphabet='01',
            states={'q0', 'q1'},
            initial_state='q0',
            final_states={'q1'},
            transitions={
                'q0': {'0': 'q0', '1': 'q1'},
                'q1': {'0': 'q1', '1': 'q0'},
            }
        )

    def test_correctly_instantiated_when_parameters_are_passed_in_the_constructor(self):
        """Should be correctly instantiated when parameters are passed in the constructor"""
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

        self.assertIsInstance(automata, DFA)
        self.assertEqual(automata.get_alphabet(), '01')
        self.assertEqual(automata.get_states(), {'q0', 'q1'})
        self.assertEqual(automata.get_initial_state(), 'q0')
        self.assertEqual(automata.get_final_states(), {'q1'})
        self.assertEqual(automata.get_transitions(), {
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q1', '1': 'q0'},
        })

    def test_instantiated_correctly_when_data_is_passed_by_methods(self):
        """Should be instantiated correctly when data is passed ​​by methods"""
        automata = DFA()
        automata.add_alphabet('01')
        automata.add_state('q0')
        automata.add_state('q1')
        automata.add_initial_state('q0')
        automata.add_final_state("q1")
        automata.add_transition('q0', 'q0', '0')
        automata.add_transition('q0', 'q1', '1')
        automata.add_transition('q1', 'q1', '0')
        automata.add_transition('q1', 'q0', '1')

        self.assertIsInstance(automata, DFA)
        self.assertEqual(automata.get_alphabet(), '01')
        self.assertEqual(automata.get_states(), {'q0', 'q1'})
        self.assertEqual(automata.get_initial_state(), 'q0')
        self.assertEqual(automata.get_final_states(), {'q1'})
        self.assertEqual(automata.get_transitions(), {
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q1', '1': 'q0'},
        })

    def test_return_to_the_next_state_correctly(self):
        """Should be return to the next state correctly"""
        self.assertEqual(
            self.automata.get_next_state('q0', '1'), 'q1'
        )

        with self.assertRaises(InvalidSymbolError):
            self.automata.get_next_state('q1', '9')

    def test_accepted_when_the_word_is_valid(self):
        """Should be accepted when the word is valid"""
        self.assertTrue(self.automata.accepted('0001011'))

    def test_rejection_when_the_word_is_invalid(self):
        """Should be rejection when the word is invalid"""
        self.assertFalse(self.automata.accepted('00101'))

    def test_copy(self):
        copy = self.automata.copy()

        self.assertIsNot(self.automata, copy)
        self.assertEqual(copy.get_states(), self.automata.get_states())
        self.assertEqual(copy.get_alphabet(), self.automata.get_alphabet())
        self.assertEqual(
            copy.get_transitions(), self.automata.get_transitions()
        )
        self.assertEqual(
            copy.get_initial_state(), self.automata.get_initial_state()
        )
        self.assertEqual(
            copy.get_final_states(), self.automata.get_final_states()
        )


if __name__ == '__main__':
    unittest.main()
