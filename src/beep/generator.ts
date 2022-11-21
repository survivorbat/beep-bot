import { Note } from './parser';
import { Track, NoteEvent, Writer, Options } from 'midi-writer-js';
import * as fs from 'fs';
import * as synth from 'synth-js';

export const generate = async (
  filePath: string,
  notes: Note[],
): Promise<void> => {
  const track = new Track();

  notes.forEach((note) => {
    track.addEvent(
      new NoteEvent(<Options>{
        pitch: note.note,
        duration: `${note.duration}`,
        wait: note.silent ? `${note.duration}` : '0',
      }),
    );
  });

  const write = new Writer(track);
  const buffer = write.buildFile();

  synth.midiToWav(Buffer.from(buffer)).toBuffer()

  await fs.promises.writeFile(filePath, buffer);
};
