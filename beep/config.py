from typing import List


class CreateConfig:
    def __init__(self, notes: List[str], instrument: str, note_length: int) -> None:
        self.notes = notes
        self.instrument = instrument
        self.note_length = note_length
