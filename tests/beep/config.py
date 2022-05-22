from typing import List

import pytest as pytest

from beep.config import _parse_input_notes, Beep


@pytest.mark.parametrize("characters, expected", [
    ('abc', [
        Beep(note='D2', start=0, end=1),
        Beep(note='D4', start=1, end=2),
        Beep(note='B4', start=2, end=3),
    ]),
    ('ABC', [
        Beep(note='D2', start=0, end=1),
        Beep(note='D4', start=1, end=2),
        Beep(note='B4', start=2, end=3),
    ]),
    ('a__', [
        Beep(note='D2', start=0, end=3),
    ]),
    ('(abc)', [
        Beep(note='D2', start=0, end=1),
        Beep(note='D4', start=0, end=1),
        Beep(note='B4', start=0, end=1),
    ]),
    ('a[badc]e', [
        Beep(note='D2', start=0, end=1),
        Beep(note='D4', start=1, end=1.25),
        Beep(note='D2', start=1.25, end=1.5),
        Beep(note='F2', start=1.5, end=1.75),
        Beep(note='B4', start=1.75, end=2),
        Beep(note='C1', start=2, end=3),
    ])
])
def test__parse_input_notes__returns_expected_output(characters: str, expected: List[Beep]) -> None:
    # Act
    result = _parse_input_notes(characters)

    # Assert
    assert len(result) == len(expected)

    for index, ex in enumerate(expected):
        assert result[index].note == ex.note
        assert result[index].start == ex.start
        assert result[index].end == ex.end
