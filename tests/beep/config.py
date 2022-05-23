from typing import List

import pytest as pytest

from beep.config import _parse_input_notes, Note


@pytest.mark.parametrize("characters, expected", [
    ('abc', [
        Note(note='D2', start=0, end=1),
        Note(note='D4', start=1, end=2),
        Note(note='B4', start=2, end=3),
    ]),
    ('ABC', [
        Note(note='D2', start=0, end=1),
        Note(note='D4', start=1, end=2),
        Note(note='B4', start=2, end=3),
    ]),
    ('a__', [
        Note(note='D2', start=0, end=3),
    ]),
    ('a---a', [
        Note(note='D2', start=0, end=1),
        Note(note='D2', start=4, end=5),
    ]),
    ('a__-__b', [
        Note(note='D2', start=0, end=3),
        Note(note='D4', start=6, end=7),
    ]),
    ('(abc)', [
        Note(note='D2', start=0, end=1),
        Note(note='D4', start=0, end=1),
        Note(note='B4', start=0, end=1),
    ]),
    ('(abc)__', [
        Note(note='D2', start=0, end=3),
        Note(note='D4', start=0, end=3),
        Note(note='B4', start=0, end=3),
    ]),
    ('[abcd]_', [
        Note(note='D2', start=0, end=0.5),
        Note(note='D4', start=0.5, end=1),
        Note(note='B4', start=1, end=1.5),
        Note(note='F2', start=1.5, end=2),
    ]),
    ('a[badc]e', [
        Note(note='D2', start=0, end=1),
        Note(note='D4', start=1, end=1.25),
        Note(note='D2', start=1.25, end=1.5),
        Note(note='F2', start=1.5, end=1.75),
        Note(note='B4', start=1.75, end=2),
        Note(note='C1', start=2, end=3),
    ])
])
def test__parse_input_notes__returns_expected_output(characters: str, expected: List[Note]) -> None:
    # Act
    result = _parse_input_notes(characters)

    # Assert
    assert len(result) == len(expected)

    for index, ex in enumerate(expected):
        assert result[index].note == ex.note
        assert result[index].start == ex.start
        assert result[index].end == ex.end
