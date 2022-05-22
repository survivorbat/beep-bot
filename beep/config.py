from typing import List

from beep.notes import key_notes


class BeepParseError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class Beep:
    def __init__(self, note: str, start: float, end: float) -> None:
        self.note = note
        self.start = start
        self.end = end


def _ensure_not_first(notes: List[Beep]) -> None:
    if len(notes) == 0:
        raise BeepParseError('misplaced _, no notes came before it')


# TODO: Refactor this if possible

def _parse_input_notes(characters: str) -> List[Beep]:
    note_index = 0

    result = []

    sequence = []
    in_sequence = False

    chord = []
    in_chord = False

    for character in characters:
        if character == '-':
            note_index += 1
            continue

        if character == '[' and in_sequence:
            raise BeepParseError('Unexpected [ found, you already have another bracket open')

        if character == ']' and not in_sequence:
            raise BeepParseError('Unexpected ] found, you need to use a [ first')

        if character == ')' and not in_chord:
            raise BeepParseError('Unexpected ) found, you need to use a ( first')

        if character == '(' and in_chord:
            raise BeepParseError('Unexpected ( found, you already have another bracket open')

        if character == '[':
            in_sequence = True
            continue

        if character == '(':
            in_chord = True
            continue

        if character == ']':
            if len(sequence) > 5:
                raise BeepParseError('Brackets should not have more than 5 characters')

            increment = 1 / len(sequence)

            for i, entry in enumerate(sequence):
                if entry == '_':
                    _ensure_not_first(result)
                    result[-1].end += increment
                    continue

                if entry == '-':
                    continue

                note = Beep(
                    note=key_notes[entry.lower()],
                    start=note_index+i*increment,
                    end=note_index+i*increment+increment
                )
                result.append(note)

            sequence = []
            in_sequence = False
            note_index += 1
            continue

        if character == ')':
            for i, entry in enumerate(chord):
                note = Beep(
                    note=key_notes[entry.lower()],
                    start=note_index,
                    end=note_index+1,
                )
                result.append(note)

            chord = []
            in_chord = False
            note_index += 1
            continue

        if in_sequence and in_chord:
            sequence.append(character)
            chord.append(character)
            continue

        if in_sequence:
            sequence.append(character)
            continue

        if in_chord:
            chord.append(character)
            continue

        if character == '_':
            _ensure_not_first(result)
            result[-1].end += 1
            continue

        note = Beep(note=key_notes[character.lower()], start=note_index, end=note_index + 1)
        result.append(note)
        note_index += 1

    return result


class BeepConfig:
    def __init__(self, notes_input: str, instrument: str) -> None:
        self.notes = _parse_input_notes(notes_input)
        self.instrument = instrument
