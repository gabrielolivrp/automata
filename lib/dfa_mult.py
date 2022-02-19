from .dfa import DFA
from .exceptions import FinalStatesError


class DFAMult:
    def __init__(self, dfa: DFA):
        self.__dfa = dfa.copy()

    def union(self, other: DFA) -> DFA:
        return self._multiply(
            other,
            fn_select_final_states=lambda state1_is_final, state2_is_final: state1_is_final or state2_is_final
        )

    def intersection(self, other: DFA) -> DFA:
        return self._multiply(
            other,
            fn_select_final_states=lambda state1_is_final, state2_is_final: state1_is_final and state2_is_final
        )

    def difference(self, other: DFA) -> DFA:
        return self._multiply(
            other,
            fn_select_final_states=lambda state1_is_final, state2_is_final: state1_is_final and not state2_is_final
        )

    def _multiply(self, other: DFA, fn_select_final_states) -> DFA:
        assert self.__dfa.get_alphabet() == other.get_alphabet()

        new_dfa = DFA(alphabet=self.__dfa.get_alphabet())
        for state1 in self.__dfa.get_states():
            for state2 in other.get_states():
                new_state = DFA.stringify_states_unsorted((state1, state2))
                new_dfa.add_state(new_state)
                if fn_select_final_states(
                    state1 in self.__dfa.get_final_states(),
                    state2 in other.get_final_states()
                ):
                    new_dfa.add_final_state(new_state)
                if state1 in self.__dfa.get_initial_state() and state2 in other.get_initial_state():
                    new_dfa.add_initial_state(new_state)
        for state in new_dfa.get_states():
            state1, state2 = DFA.unstringify_states(state)
            for symbol in self.__dfa.get_alphabet():
                next_state1 = self.__dfa.get_next_state(state1, symbol)
                next_state2 = other.get_next_state(state2, symbol)
                new_next_state = DFA.stringify_states_unsorted(
                    (next_state1, next_state2)
                )
                new_dfa.add_transition(state, new_next_state, symbol)
        return new_dfa
