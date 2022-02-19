from collections import deque
from .fa import FA
from .exceptions import FinalStatesError, InitialStateError, InvalidStateError, InvalidSymbolError, InvalidSymbolError


class NFA(FA):
    def __init__(self, alphabet: str = '', states: set = set(), transitions: dict = {},
                 initial_state: set = set(), final_states: set = set()):
        super().__init__(alphabet, states, transitions, initial_state, final_states)

    def add_initial_state(self, state: str) -> None:
        if state not in self._states:
            raise InitialStateError

        self._initial_state.add(state)

    def add_transition(self, _from: str, to: str, symbol: str) -> None:
        if symbol not in self._alphabet and symbol != '':
            raise InvalidSymbolError
        if _from not in self._states or to not in self._states:
            raise InvalidStateError

        if _from not in self._transitions:
            self._transitions[_from] = {}
        if symbol not in self._transitions[_from]:
            self._transitions[_from][symbol] = set()

        self._transitions[_from][symbol].add(to)

    def get_next_states(self, state: str, symbol: str, with_epsilon=True) -> set:
        if symbol not in self._alphabet and (with_epsilon and symbol != ''):
            raise InvalidSymbolError
        if state not in self._states:
            raise InvalidStateError

        next_states = set()
        if state in self._transitions:
            if symbol in self._transitions[state]:
                next_states |= self._transitions[state][symbol]
            if with_epsilon is True and '' in self._transitions[state]:
                for state_e in self._transitions[state]['']:
                    next_states |= self.get_next_states(state_e, symbol)
        return next_states

    def read_input(self, _input: str) -> set:
        if not self._initial_state:
            raise InitialStateError

        current_states = self._initial_state
        for symbol in _input:
            next_states = set()
            for state in current_states:
                next_states |= self.get_next_states(state, symbol)
            current_states = next_states
            if not current_states:
                break
        return current_states

    def accepted(self, _input: str) -> bool:
        if not self._final_states:
            raise FinalStatesError

        return (self.read_input(_input) & self._final_states) != set()

    def eclose(self, state):
        states = set({state})
        if state in self._transitions and '' in self._transitions[state]:
            for state2 in self._transitions[state]['']:
                states |= self.eclose(state2)

        return states

    @staticmethod
    def from_nfa_epsilon(nfa_epsilon):
        def eclose_of_states(states):
            eclose = set()
            for state in states:
                eclose |= nfa_epsilon.eclose(state)
            return eclose

        def nexts_of_states(states, symbol):
            nexts = set()
            for state in states:
                nexts |= nfa_epsilon.get_next_states(
                    state, symbol, with_epsilon=False
                )
            return nexts

        map_states = {}
        for state in sorted(nfa_epsilon.get_states()):
            map_states[state] = {}
            eclose = set(sorted(nfa_epsilon.eclose(state)))

            for symbol in sorted(nfa_epsilon.get_alphabet()):
                nexts_states = set(sorted(nexts_of_states(eclose, symbol)))
                nexts_states_eclose = set(
                    sorted(eclose_of_states(nexts_states))
                )
                map_states[state][symbol] = nexts_states_eclose

        new_nfa = NFA(alphabet=nfa_epsilon.get_alphabet())
        new_nfa._states = nfa_epsilon.get_states().copy()
        new_nfa._final_states = nfa_epsilon.get_final_states().copy()
        new_nfa._initial_state = nfa_epsilon.get_initial_state().copy()

        for state in new_nfa.get_states():
            for symbol in new_nfa.get_alphabet():
                for to in map_states[state][symbol]:
                    new_nfa.add_transition(state, to, symbol)

        return new_nfa
