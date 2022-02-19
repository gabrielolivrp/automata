from collections import deque
from .exceptions import FinalStatesError, InitialStateError, InvalidStateError, InvalidSymbolError, MissingStateError
from .fa import FA


class DFA(FA):
    def __init__(self, alphabet: str = '', states: set = set(), transitions: dict = {},
                 initial_state: str = '', final_states: set = set()):
        FA.__init__(self, alphabet, states, transitions,
                    initial_state, final_states)

    def add_initial_state(self, state: str) -> None:
        if state not in self._states:
            raise InitialStateError

        self._initial_state = state

    def add_transition(self, _from: str, to: str, symbol: str) -> None:
        if symbol not in self._alphabet:
            raise InvalidSymbolError
        if _from not in self._states or to not in self._states:
            raise InvalidStateError

        if _from not in self._transitions:
            self._transitions[_from] = {}
        self._transitions[_from][symbol] = to

    def get_next_state(self, state: str, symbol: str) -> str:
        if symbol not in self._alphabet:
            raise InvalidSymbolError
        if state not in self._states:
            raise InvalidStateError

        if state in self._transitions and symbol in self._transitions[state]:
            return self._transitions[state][symbol]
        raise MissingStateError

    def read_input(self, _input: str) -> str:
        if not self._initial_state:
            raise InitialStateError

        current_state = self._initial_state
        for symbol in _input:
            current_state = self.get_next_state(current_state, symbol)
        return current_state

    def accepted(self, _input: str) -> bool:
        if not self._final_states:
            raise FinalStatesError

        return self.read_input(_input) in self._final_states

    def complement(self):
        new_dfa = self.__dfa.copy()
        new_dfa._final_states = self.__dfa.get_states() - self.__dfa.get_final_states()
        return new_dfa

    @staticmethod
    def from_nfa(nfa):
        table = {}
        new_initial_state = DFA.stringify_states_sorted(
            nfa.get_initial_state()
        )
        table[new_initial_state] = {}

        state_queue = deque()

        state_queue.append(new_initial_state)
        states_checked = []
        while state_queue:
            current_state = state_queue.popleft()
            states_checked.append(current_state)
            state_unstringfy = DFA.unstringify_states(current_state)
            transitions = {}
            for symbol in nfa.get_alphabet():
                next_states = set()
                for state in state_unstringfy:
                    next_states |= nfa.get_next_states(state, symbol)
                transitions[symbol] = DFA.stringify_states_sorted(next_states)

            table[current_state] = transitions
            for state in transitions.values():
                if state not in states_checked and state != '{}':
                    state_queue.append(state)

        new_dfa = DFA(alphabet=nfa.get_alphabet())
        for state in table.keys():
            new_dfa.add_state(state)
            for final_state in nfa.get_final_states():
                if final_state in state:
                    new_dfa.add_final_state(state)

        new_dfa.add_state('e')
        new_dfa.add_initial_state(new_initial_state)

        for state, transitions in table.items():
            for symbol, to_state in transitions.items():
                new_dfa.add_transition(
                    state, 'e' if to_state == '{}' else to_state, symbol)
        for symbol in new_dfa.get_alphabet():
            new_dfa.add_transition('e', 'e', symbol)
        return new_dfa
