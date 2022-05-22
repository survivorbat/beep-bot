import pretty_midi
import tempfile

from midi2audio import FluidSynth

from beep.config import BeepConfig


def create_beeps(config: BeepConfig, result_path: str) -> None:
    ensemble = pretty_midi.PrettyMIDI()
    program = pretty_midi.instrument_name_to_program(config.instrument)
    instrument = pretty_midi.Instrument(program=program)

    for index, note in enumerate(config.notes):
        note_number = pretty_midi.note_name_to_number(note.note)
        entry = pretty_midi.Note(velocity=100, pitch=note_number, start=note.start, end=note.end)

        instrument.notes.append(entry)

    ensemble.instruments.append(instrument)

    with tempfile.NamedTemporaryFile(suffix='.mid') as temp_mid:
        ensemble.write(temp_mid.name)

        FluidSynth().midi_to_audio(temp_mid.name, result_path)
