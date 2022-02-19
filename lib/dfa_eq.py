from .helpers.table_eq import TableEq
from .dfa import DFA


class DFAEq:
    def __init__(self, dfa: DFA):
        self.__table = TableEq()
        self.__states_map = {}
        self.__dfa = dfa.copy()

    def __create_states_map(self, other: DFA):
        index = 0
        for state in self.__dfa.get_states():
            self.__states_map[index] = {
                'dfa': 1,
                'state_name': state,
                'is_final': state in self.__dfa.get_final_states()
            }
            index += 1

        for state in other.get_states():
            self.__states_map[index] = {
                'dfa': 2,
                'state_name': state,
                'is_final': state in other.get_final_states()
            }
            index += 1

    def __mark_trivially_non_eq_states(self):
        for state1, states in self.__table.items():
            state_map1 = self.__states_map[state1]
            for state2 in states:
                state_map2 = self.__states_map[state2]
                if state_map1['is_final'] is True and \
                        state_map2['is_final'] is False or \
                        state_map2['is_final'] is True and \
                        state_map1['is_final'] is False:
                    self.__table.set_value(state1, state2, False)

    def __get_index_from_state(self, state: str):
        for index, state_map in self.__states_map.items():
            if state_map['state_name'] == state:
                return index

    def __get_index_from_next_state(self, other: DFA, state_map, symbol: str):
        if state_map['dfa'] == 1:
            return self.__get_index_from_state(self.__dfa.get_next_state(
                state_map['state_name'], symbol
            ))

        return self.__get_index_from_state(other.get_next_state(
            state_map['state_name'], symbol
        ))

    def __states_eq(self, state1: str, state2: str, other: DFA):
        pending_states = []
        state_map1, state_map2 = self.__states_map[state1], self.__states_map[state2]
        for symbol in self.__dfa.get_alphabet():
            next_state1 = self.__get_index_from_next_state(other, state_map1, symbol)
            next_state2 = self.__get_index_from_next_state(other, state_map2, symbol)

            if self.__table.states_non_eq(next_state1, next_state2):
                return False, []
            else:
                if next_state1 != next_state2:
                    pending_states.append((next_state1, next_state2))
        return True, pending_states

    def __mark_non_eq_states(self, other: DFA):
        for state1, states in self.__table.items():
            for state2 in states:
                is_eq, pending_states = self.__states_eq(state1, state2, other)
                if is_eq:
                    self.__table.add_pending_states(
                        state1, state2, pending_states
                    )
                else:
                    self.__table.mark_states_as_non_eq(state1, state2)

    def equals(self, other: DFA) -> bool:
        self.__create_states_map(other)
        self.__table.create_table(self.__states_map)
        self.__mark_trivially_non_eq_states()
        self.__mark_non_eq_states(other)

        initial_state1 = self.__get_index_from_state(
            self.__dfa.get_initial_state()
        )

        initial_state2 = self.__get_index_from_state(other.get_initial_state())

        return self.__table.get_value(initial_state1, initial_state2) != False
