class TableEq:
    def __init__(self):
        self.__table = {}

    def items(self):
        return self.__table.items()

    def create_table(self, states):
        sorted_states = sorted(states)
        for index, state1 in enumerate(sorted_states):
            self.__table[state1] = {}
            for state2 in sorted_states[:index]:
                self.__table[state1][state2] = None

    def has(self, state1, state2):
        return state1 in self.__table and state2 in self.__table[state1]

    def states_non_eq(self, state1, state2):
        return self.get_value(state1, state2) is False

    def get_value(self, state1, state2):
        if self.has(state1, state2):
            return self.__table[state1][state2]
        elif self.has(state2, state1):
            return self.__table[state2][state1]

    def set_value(self, state1, state2, value):
        if self.has(state1, state2):
            self.__table[state1][state2] = value
        elif self.has(state2, state1):
            self.__table[state2][state1] = value

    def mark_states_as_non_eq(self, state1, state2):
        pending_states = self.get_value(state1, state2)
        self.set_value(state1, state2, False)
        if type(pending_states) == list:
            for pending_state in pending_states:
                self.mark_states_as_non_eq(
                    pending_state[0], pending_state[1])

    def add_pending_states(self, state1, state2, pending_states):
        for pending_state in pending_states:
            value = self.get_value(pending_state[0], pending_state[1])
            if type(value) == list:
                value.append((state1, state2))
            elif value is None:
                value = [(state1, state2)]
            self.set_value(pending_state[0], pending_state[1], value)
