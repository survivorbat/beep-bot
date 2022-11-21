import { generate } from './generator';
import path from 'path';
import tmp from 'tmp';
import * as fs from 'fs';

describe('generate', () => {
  const testData = [
    {
      filePath: 'test.mid',
      notes: [],
    },
    {
      filePath: 'test.mid',
      notes: [{ note: ['G5'], duration: 1, silent: false }],
    },
  ];

  testData.forEach(({ filePath, notes }) => {
    const fullPath = path.join(tmp.dirSync().name, filePath);

    it(`should generate a midi file at ${fullPath} from ${notes.length} notes`, async () => {
      // Act
      await generate(fullPath, notes);

      // Assert
      const fileExists = await fs.promises.stat(fullPath);
      expect(fileExists.isFile()).toBeTruthy();
    });
  });
});
