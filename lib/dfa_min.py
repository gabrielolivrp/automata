from itertools import combinations
from collections import deque
from typing import Tuple
from .helpers.table_eq import TableEq
from .dfa import DFA


class DFAMin:
    def __init__(self, dfa: DFA):
        self.__table = TableEq()
        self.__dfa = dfa.copy()

    def __remove_unreachable_states(self):
        reachable = self.__reachable_states_from_initial_state()
        unreachable = self.__dfa.get_states() - reachable
        for state in unreachable:
            self.__dfa.remove_state(state)
            self.__dfa.remove_transitions(state)
            if state in self.__dfa.get_final_states():
                self.__dfa.remove_final_states(state)

    def __reachable_states_from_initial_state(self):
        reachable = set({self.__dfa.get_initial_state()})
        pending = deque({self.__dfa.get_initial_state()})
        transitions = self.__dfa.get_transitions()
        while pending:
            state = pending.popleft()
            for _, next_state in transitions[state].items():
                if next_state not in reachable:
                    reachable.add(next_state)
                    pending.append(next_state)
        return reachable

    def __mark_trivially_non_eq_states(self):
        for state1, states in self.__table.items():
            for state2 in states:
                if state1 in self.__dfa.get_final_states() and state2 not in self.__dfa.get_final_states() or \
                        state2 in self.__dfa.get_final_states() and state1 not in self.__dfa.get_final_states():
                    self.__table.set_value(state1, state2, False)

    def __states_eq(self, state1: str, state2: str) -> Tuple[bool, list]:
        pending_states = []
        for symbol in self.__dfa.get_alphabet():
            next_state1 = self.__dfa.get_next_state(state1, symbol)
            next_state2 = self.__dfa.get_next_state(state2, symbol)
            if self.__table.states_non_eq(next_state1, next_state2):
                return False, []
            else:
                if next_state1 != next_state2:
                    pending_states.append((next_state1, next_state2))

        return True, pending_states

    def __mark_non_eq_states(self):
        for state1, states in self.__table.items():
            for state2 in states:
                is_eq, pending_states = self.__states_eq(state1, state2)
                if is_eq:
                    self.__table.add_pending_states(
                        state1, state2, pending_states
                    )
                else:
                    self.__table.mark_states_as_non_eq(state1, state2)


    def minify(self) -> DFA:
        self.__remove_unreachable_states()
        self.__table.create_table(self.__dfa.get_states())
        self.__mark_trivially_non_eq_states()
        self.__mark_non_eq_states()

        pair_of_eq_states = []
        for state1, states in self.__table.items():
            for state2 in states:
                value = self.__table.get_value(state1, state2)
                if value is None or type(value) == list:
                    pair_of_eq_states.append({state1, state2})

        pair_of_eq_states = self._transitivity_states(pair_of_eq_states)
        new_states = self.__dfa.get_states().copy()
        new_transitions = self.__dfa.get_transitions().copy()
        new_initial_state = self.__dfa.get_initial_state()
        new_final_states = self.__dfa.get_final_states().copy()

        for eq_states in pair_of_eq_states:
            new_name = DFA.stringify_states_sorted(eq_states)

            if new_initial_state in eq_states:
                new_initial_state = new_name

            for final_state in self.__dfa.get_final_states():
                if final_state in eq_states:
                    new_final_states.remove(final_state)
                    new_final_states.add(new_name)

            for eq_state in eq_states:
                new_states.remove(eq_state)
                del new_transitions[eq_state]

            for _, transitions in new_transitions.items():
                removes = []
                for symbol, transition in transitions.items():
                    if transition in eq_states:
                        removes.append(symbol)

                for remove in removes:
                    transitions[remove] = new_name

            new_states.add(new_name)
            new_transitions[new_name] = {}

        for symbol in self.__dfa.get_alphabet():
            for eq_states in pair_of_eq_states:
                new_name = DFA.stringify_states_sorted(eq_states)
                to = set()
                for state in eq_states:
                    to.add(self.__dfa.get_next_state(state, symbol))

                index = 0
                find = False
                to = set(sorted(to))
                for eq_states2 in pair_of_eq_states:
                    if (to & eq_states2) != set():
                        find = True
                        break
                    index += 1
                if find:
                    to_stringfy = DFA.stringify_states_sorted(
                        pair_of_eq_states[index]
                    )
                    new_transitions[new_name][symbol] = to_stringfy
                else:
                    if len(to) == 1:
                        new_transitions[new_name][symbol] = list(to)[0]

        return DFA(
            states=new_states,
            transitions=new_transitions,
            final_states=new_final_states,
            initial_state=new_initial_state,
            alphabet=self.__dfa.get_alphabet()
        )

    @staticmethod
    def _transitivity_states(states):
        stable = False
        while not stable:                        # loop until no further reduction is found
            stable = True
            for s, t in combinations(states, 2):
                if s & t:                        # do the states intersect ?
                    s |= t                       # move items from t to s
                    t ^= t                       # empty t
                    stable = False
            states = list(filter(None, states))  # added list() for python 3
        return states
