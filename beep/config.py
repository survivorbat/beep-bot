import functools
from abc import abstractmethod, ABCMeta
from typing import List, Optional

from beep.notes import key_notes


class BeepParseError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class Note:
    def __init__(self, note: str, start: float, end: float) -> None:
        self.note = note
        self.start = start
        self.end = end


class _AbstractBeep:
    def __init__(self) -> None:
        self._prolongs = 0

    def prolong(self) -> None:
        self._prolongs += 1

    @abstractmethod
    def add_note(self, note: str) -> None:
        pass

    @abstractmethod
    def get_notes(self, start: int) -> Optional[List]:
        pass

    def length(self) -> int:
        return 1 + self._prolongs


class _SilentBeep(_AbstractBeep):
    def add_note(self, note: str) -> None:
        pass

    def get_notes(self, start: int) -> Optional[List]:
        return [None] * self._prolongs


class _BeepSingle(_AbstractBeep):
    def __init__(self) -> None:
        super().__init__()
        self._note = None

    def add_note(self, note: str) -> None:
        self._note = note

    def get_notes(self, start: int) -> Optional[List]:
        return [
            Note(note=self._note, start=start, end=start + (self._prolongs + 1))
        ]


class _BeepGroup(_AbstractBeep):
    def __init__(self) -> None:
        super().__init__()
        self._notes = []

    def add_note(self, note: str) -> None:
        self._notes.append(note)

    def get_notes(self, start: int) -> Optional[List]:
        result = []
        increment = (self._prolongs + 1) / len(self._notes)

        for i, entry in enumerate(self._notes):
            if entry == '_':
                _ensure_not_first(self._notes)
                result[-1].end += increment
                continue

            if entry == '-':
                continue

            note = Note(
                note=key_notes[entry.lower()],
                start=start+i*increment,
                end=start+i*increment+increment
            )
            result.append(note)

        return result


class _BeepChord(_AbstractBeep):
    def __init__(self) -> None:
        super().__init__()
        self._notes = []

    def add_note(self, note: str) -> None:
        self._notes.append(note)

    def get_notes(self, start: int) -> Optional[List]:
        result = []

        for i, entry in enumerate(self._notes):
            note = Note(
                note=key_notes[entry.lower()],
                start=start,
                end=start+(self._prolongs + 1),
            )
            result.append(note)

        return result


def _ensure_not_first(notes: List[_AbstractBeep]) -> None:
    if len(notes) == 0:
        raise BeepParseError('misplaced _, no notes came before it')


# TODO: Refactor this if possible

def _parse_input_notes(characters: str) -> List[Note]:
    beeps: List[_AbstractBeep] = []

    sequence: Optional[_BeepGroup] = None
    chord: Optional[_BeepChord] = None

    for character in characters:
        if character == '-':
            beeps.append(_SilentBeep())
            continue

        if character == '[' and sequence is not None:
            raise BeepParseError('Unexpected [ found, you already have another bracket open')

        if character == ']' and sequence is None:
            raise BeepParseError('Unexpected ] found, you need to use a [ first')

        if character == ')' and chord is None:
            raise BeepParseError('Unexpected ) found, you need to use a ( first')

        if character == '(' and chord is not None:
            raise BeepParseError('Unexpected ( found, you already have another bracket open')

        if character == '[':
            sequence = _BeepGroup()
            continue

        if character == '(':
            chord = _BeepChord()
            continue

        if character == ']' and sequence is not None:
            beeps.append(sequence)
            sequence = None
            continue

        if character == ')' and chord is not None:
            beeps.append(chord)
            chord = None
            continue

        if sequence is not None and chord is not None:
            sequence.add_note(character)
            chord.add_note(character)
            continue

        if sequence is not None:
            sequence.add_note(character)
            continue

        if chord is not None:
            chord.add_note(character)
            continue

        if character == '_':
            _ensure_not_first(beeps)
            beeps[-1].prolong()
            continue

        single_beep = _BeepSingle()
        single_beep.add_note(key_notes[character.lower()])
        beeps.append(single_beep)

    result = []
    note_index = 0
    for beep in beeps:
        entry = beep.get_notes(note_index)

        # Skip dashes
        if None in entry:
            note_index += beep.length()
            continue

        result = result + entry
        note_index += beep.length()

    return result


class BeepConfig:
    def __init__(self, notes_input: str, instrument: str) -> None:
        self.notes: List[Note] = _parse_input_notes(notes_input)
        self.instrument: str = instrument
