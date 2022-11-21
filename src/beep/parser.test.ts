import { parseNotes } from './parser';

describe('parses', () => {
  const testData = [
    {
      input: 'abc',
      expected: [
        { note: ['G3'], duration: 1, silent: false },
        { note: ['G5'], duration: 1, silent: false },
        { note: ['E5'], duration: 1, silent: false },
      ],
    },
    {
      input: 'ABC',
      expected: [
        { note: ['G3'], duration: 1, silent: false },
        { note: ['G5'], duration: 1, silent: false },
        { note: ['E5'], duration: 1, silent: false },
      ],
    },
    { input: 'a__', expected: [{ note: ['G3'], duration: 3, silent: false }] },
    {
      input: 'a---a',
      expected: [
        { note: ['G3'], duration: 1, silent: false },
        { note: [], duration: 1, silent: true },
        { note: [], duration: 1, silent: true },
        { note: [], duration: 1, silent: true },
        { note: ['G3'], duration: 1, silent: false },
      ],
    },
    {
      input: 'a__-__b',
      expected: [
        { note: ['G3'], duration: 3, silent: false },
        { note: [], duration: 3, silent: true },
        { note: ['G5'], duration: 1, silent: false },
      ],
    },
    {
      input: '(abc)',
      expected: [{ note: ['G3', 'G5', 'E5'], duration: 1, silent: false }],
    },
    {
      input: '(abc)__',
      expected: [{ note: ['G3', 'G5', 'E5'], duration: 3, silent: false }],
    },
    {
      input: '[abcd]_',
      expected: [
        { note: ['G3'], duration: 0.5, silent: false },
        { note: ['G5'], duration: 0.5, silent: false },
        { note: ['E5'], duration: 0.5, silent: false },
        { note: ['B4'], duration: 0.5, silent: false },
      ],
    },
    {
      input: 'a[badc]e',
      expected: [
        { note: ['G3'], duration: 1, silent: false },
        { note: ['G5'], duration: 0.25, silent: false },
        { note: ['G3'], duration: 0.25, silent: false },
        { note: ['B4'], duration: 0.25, silent: false },
        { note: ['E5'], duration: 0.25, silent: false },
        { note: ['F2'], duration: 1, silent: false },
      ],
    },
  ];

  testData.forEach(({ input, expected }) => {
    it(`should generate correct notes from '${input}'`, () => {
      // Act
      const result = parseNotes(input);

      // Assert
      expect(result).toEqual(expected);
    });
  });
});
