import { keyNotes } from '../constants/notes';

export interface Note {
  note: string[];
  duration: number;
  silent: boolean;
}

class BeepParseError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'BeepParseError';
  }
}

abstract class AbstractBeep {
  protected prolongs: number = 0;

  prolong(): void {
    this.prolongs++;
  }

  abstract addNote(note: string): void;

  abstract getNotes(): (Note | null)[];
}

class SilentBeep extends AbstractBeep {
  addNote(): void {}

  getNotes(): (Note | null)[] {
    return [{ note: [], duration: this.prolongs + 1, silent: true }];
  }
}

class SingleBeep extends AbstractBeep {
  private note: string;

  addNote(note: string) {
    this.note = note;
  }

  getNotes(): (Note | null)[] {
    return [{ note: [this.note], duration: this.prolongs + 1, silent: false }];
  }
}

class BeepGroup extends AbstractBeep {
  private notes: string[] = [];

  addNote(note: string) {
    this.notes = this.notes.concat(note);
  }

  getNotes(): (Note | null)[] {
    let result: (Note | null)[] = [];
    const duration = (this.prolongs + 1) / this.notes.length;

    this.notes.forEach((note) => {
      if (note === '-') {
        return;
      }

      result = result.concat({
        note: [keyNotes[note.toLowerCase()]],
        duration,
        silent: false,
      });
    });

    return result;
  }
}

class BeepChord extends AbstractBeep {
  private notes: string[] = [];

  addNote(note: string) {
    this.notes = this.notes.concat(note);
  }

  getNotes(): (Note | null)[] {
    return [
      {
        note: this.notes.map((note) => keyNotes[note.toLowerCase()]),
        duration: this.prolongs + 1,
        silent: false,
      },
    ];
  }
}

export const parseNotes = (characters: string): Note[] => {
  // List of beeps to be played
  let beeps: AbstractBeep[] = [];

  // Current sequence of beeps, between []
  let sequence: BeepGroup | undefined;

  // Current chord of beeps, between ()
  let chord: BeepChord | undefined;

  characters.split('').forEach((character) => {
    if (character == ' ') {
      return;
    }

    if (character == '-') {
      beeps = beeps.concat(new SilentBeep());
      return;
    }

    if (character == '[' && sequence) {
      throw new BeepParseError(
        'Unexpected [ found, you already have another bracket open',
      );
    }

    if (character == ']' && !sequence) {
      throw new BeepParseError('Unexpected ] found, you need to use a [ first');
    }

    if (character == ')' && !chord) {
      throw new BeepParseError('Unexpected ) found, you need to use a ( first');
    }

    if (character == '(' && chord) {
      throw new BeepParseError(
        'Unexpected ( found, you already have another bracket open',
      );
    }

    if (character == '[') {
      sequence = new BeepGroup();
      return;
    }

    if (character == '(') {
      chord = new BeepChord();
      return;
    }

    if (character == ']') {
      beeps = beeps.concat(sequence);
      sequence = undefined;
      return;
    }

    if (character == ')') {
      beeps = beeps.concat(chord);
      chord = null;
      return;
    }

    if (chord && sequence) {
      sequence.addNote(character);
      chord.addNote(character);
      return;
    }

    if (sequence) {
      sequence.addNote(character);
      return;
    }

    if (chord) {
      chord.addNote(character);
      return;
    }

    if (character === '_') {
      beeps[beeps.length - 1].prolong();
      return;
    }

    const singleBeep = new SingleBeep();
    singleBeep.addNote(keyNotes[character.toLowerCase()]);
    beeps = beeps.concat(singleBeep);
  });

  if (sequence) {
    throw new BeepParseError('You forgot to finish a pair of brackets');
  }

  if (chord) {
    throw new BeepParseError('You forgot to finish a pair of parenthesis');
  }

  return beeps.reduce(
    (previous, current) => previous.concat(current.getNotes()),
    [],
  );
};
