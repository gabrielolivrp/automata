import copy
import xml.etree.ElementTree as ET
from .exceptions import FinalStatesError


class FA:
    def __init__(self, alphabet: str = '', states: set = set(), transitions: dict = {},
                 initial_state = None, final_states: set = set()):
        self._alphabet = alphabet
        self._transitions = copy.deepcopy(transitions)
        self._states = states.copy()
        self._initial_state = initial_state
        self._final_states = final_states.copy()

    def add_state(self, state: str) -> None:
        self._states.add(state)

    def get_states(self) -> set:
        return self._states

    def add_alphabet(self, alphabet: str) -> None:
        self._alphabet = alphabet

    def get_alphabet(self) -> str:
        return self._alphabet

    def get_initial_state(self):
        return self._initial_state

    def add_final_state(self, state: set) -> None:
        if state not in self._states:
            raise FinalStatesError

        self._final_states.add(state)

    def get_final_states(self) -> set:
        return self._final_states

    def get_transitions(self) -> dict:
        return self._transitions

    def remove_state(self, state: str):
        self._states.remove(state)

    def remove_transitions(self, state: str):
        del self._transitions[state]

    def remove_final_states(self, state: str):
        self._final_states.remove(state)

    def to_jflap(self, path: str):
        id, states = 0, {}
        root = ET.Element('structure')
        ET.SubElement(root, 'type').text = 'fa'
        automaton = ET.SubElement(root, 'automaton')
        y = 200
        for state in self._states:
            states[state] = str(id)
            xml_state = ET.SubElement(
                automaton, 'state', id=str(id), name=state)
            ET.SubElement(xml_state, 'x').text = '200'
            ET.SubElement(xml_state, 'y').text = str(y)
            if state in self._initial_state:
                ET.SubElement(xml_state, 'initial')
            if state in self._final_states:
                ET.SubElement(xml_state, 'final')
            id += 1
            y += 200
        for state, transitions in self._transitions.items():
            for read, to in transitions.items():
                if type(to) == set:
                    for t in to:
                        xml_transition = ET.SubElement(automaton, 'transition')
                        ET.SubElement(xml_transition,
                                      'from').text = states[state]
                        ET.SubElement(xml_transition, 'to').text = states[t]
                        ET.SubElement(xml_transition, 'read').text = read
                else:
                    xml_transition = ET.SubElement(automaton, 'transition')
                    ET.SubElement(xml_transition, 'to').text = states[to]
                    ET.SubElement(xml_transition, 'from').text = states[state]
                    ET.SubElement(xml_transition, 'read').text = read

        xml_string = ET.tostring(root)
        file = open(path, 'wb')
        file.write(b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
        file.write(xml_string)
        file.close()

    def from_jflap(self, path: str):
        states = {}
        alphabet = set()
        transitions = []

        root = ET.parse(path).getroot()
        for child in root[1]:
            if child.tag == 'state':
                state_name = child.attrib['name']
                state_id = child.attrib['id']
                states[state_id] = {
                    'name': state_name,
                    'final': child.find('final') is not None,
                    'initial': child.find('initial') is not None
                }
            if child.tag == 'transition':
                _to, _from = child.find('to').text,   \
                    child.find('from').text

                if child.find('read').text:
                    _read = child.find('read').text
                else:
                    _read = ''

                transitions.append({
                    'to': _to,
                    'from': _from,
                    'read': _read,
                })
                alphabet.add(_read)

        self.add_alphabet(''.join(alphabet))

        for _, state in states.items():
            self.add_state(state['name'])
            if state['final'] is True:
                self.add_final_state(state['name'])
            if state['initial'] is True:
                self.add_initial_state(state['name'])

        for transition in transitions:
            self.add_transition(
                states[transition['from']]['name'],
                states[transition['to']]['name'],
                transition['read']
            )

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        string = 'AF(S, A, T, I, F): \n'

        string += f'  S = {self._states}\n'

        string += f'  A = {set(self._alphabet)}\n'

        string += '  T = [ \n'
        for state, transitions in self._transitions.items():
            for symbol, to in transitions.items():
                to = f'\'{to}\'' if type(to) != set else to
                string += f'    (\'{state}\', \'{symbol}\') --> {to}, \n'
        string += '  ]\n'

        string += f'  I = {self._initial_state}\n'

        string += f'  F = {self._final_states}\n'

        return string

    @staticmethod
    def stringify_states_unsorted(states):
        return f'{{{",".join(states)}}}'

    @staticmethod
    def stringify_states_sorted(states):
        return f'{{{",".join(sorted(states))}}}'

    @staticmethod
    def unstringify_states(state):
        return state[1:-1].split(',')
