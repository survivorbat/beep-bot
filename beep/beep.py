import pretty_midi
import tempfile

from midi2audio import FluidSynth
from beep.config import CreateConfig

note_length = 1


class BeepInstance:
    def __init__(self, guild_id: int) -> None:
        self._guild_id = guild_id

    def create(self, config: CreateConfig, result_path: str) -> None:
        ensemble = pretty_midi.PrettyMIDI()
        program = pretty_midi.instrument_name_to_program(config.instrument)
        instrument = pretty_midi.Instrument(program=program)

        ensemble.instruments.append(instrument)

        for index, note in enumerate(config.notes):
            note_number = pretty_midi.note_name_to_number(note)
            note = pretty_midi.Note(velocity=100, pitch=note_number, start=note_length*index, end=note_length*(index+1))

            instrument.notes.append(note)

        with tempfile.NamedTemporaryFile(suffix='.mid') as temp_mid:
            ensemble.write(temp_mid.name)

            FluidSynth().midi_to_audio(temp_mid.name, result_path)
