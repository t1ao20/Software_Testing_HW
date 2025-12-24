const assert = require('assert');
const { test } = require('node:test');

const Calculator = require('../src/calculator');

/* ---------------------------
 *  Input validation (month)
 * --------------------------- */
test('invalid month1 (<1)', () => {
  assert.throws(
    () => Calculator.main(0, 1, 2, 1, 2024),
    /invalid month1/
  );
});

test('invalid month1 (>12)', () => {
  assert.throws(
    () => Calculator.main(13, 1, 2, 1, 2024),
    /invalid month1/
  );
});

test('invalid month2 (<1)', () => {
  assert.throws(
    () => Calculator.main(1, 1, 0, 1, 2024),
    /invalid month2/
  );
});

test('invalid month2 (>12)', () => {
  assert.throws(
    () => Calculator.main(1, 1, 13, 1, 2024),
    /invalid month2/
  );
});
/* ---------------------------
  *  Input validation - edge (month)
  * --------------------------- */
test('valid month1 (1)', () => {
  assert.doesNotThrow(
    () => Calculator.main(1, 1, 2, 1, 2024)
  );
});
test('valid month1 (12)', () => {
  assert.doesNotThrow(
    () => Calculator.main(12, 1, 12, 31, 2024)
  );
});
test('valid month2 (1)', () => {
  assert.doesNotThrow(
    () => Calculator.main(1, 1, 1, 31, 2024)
  );
});
test('valid month2 (12)', () => {
  assert.doesNotThrow(
    () => Calculator.main(11, 1, 12, 31, 2024)
  );
});
/* ---------------------------
 *  Input validation (day)
 * --------------------------- */
test('invalid day1 (<1)', () => {
  assert.throws(
    () => Calculator.main(1, 0, 2, 1, 2024),
    /invalid day1/
  );
});

test('invalid day1 (>31)', () => {
  assert.throws(
    () => Calculator.main(1, 32, 2, 1, 2024),
    /invalid day1/
  );
});

test('invalid day2 (<1)', () => {
  assert.throws(
    () => Calculator.main(1, 1, 2, 0, 2024),
    /invalid day2/
  );
});

test('invalid day2 (>31)', () => {
  assert.throws(
    () => Calculator.main(1, 1, 2, 32, 2024),
    /invalid day2/
  );
});
/* ---------------------------
 *  Input validation - edge (day)
 * --------------------------- */
test('valid day1 (1)', () => {
  assert.doesNotThrow(
    () => Calculator.main(1, 1, 2, 1, 2024)
  );
});
test('valid day1 (31)', () => {
  assert.doesNotThrow(
    () => Calculator.main(1, 31, 2, 1, 2024)
  );
});
test('valid day2 (1)', () => {
  assert.doesNotThrow(
    () => Calculator.main(1, 1, 2, 1, 2024)
  );
});
test('valid day2 (31)', () => {
  assert.doesNotThrow(
    () => Calculator.main(1, 1, 2, 31, 2024)
  );
}); 
/* ---------------------------
 *  Input validation (year)
 * --------------------------- */
test('invalid year (<1)', () => {
  assert.throws(
    () => Calculator.main(1, 1, 2, 1, 0),
    /invalid year/
  );
});

test('invalid year (>10000)', () => {
  assert.throws(
    () => Calculator.main(1, 1, 2, 1, 10001),
    /invalid year/
  );
});
/* ---------------------------
 *  Input validation - edge (year)
 * --------------------------- */
test('valid year (1)', () => {
  assert.doesNotThrow(
    () => Calculator.main(1, 1, 2, 1, 1)
  );
});
test('valid year (10000)', () => {
  assert.doesNotThrow(
    () => Calculator.main(1, 1, 2, 1, 10000)
  );
});
/* ---------------------------
 *  Logical ordering constraints
 * --------------------------- */
test('same month but day1 > day2 throws', () => {
  assert.throws(
    () => Calculator.main(5, 10, 5, 5, 2024),
    /day1 must be less than day2/
  );
});

test('month1 > month2 throws', () => {
  assert.throws(
    () => Calculator.main(6, 1, 5, 10, 2024),
    /month1 must be less than month2/
  );
});
/* ---------------------------
 *  Logical ordering constraints
 * --------------------------- */
test('month1 == month2 and day1 <= day2 does not throw', () => {
  assert.doesNotThrow(
    () => Calculator.main(3, 5, 3, 5, 2024)
  );
});

test('month1 == month2 and day1 < day2 does not throw', () => {
  assert.doesNotThrow(
    () => Calculator.main(3, 5, 3, 10, 2024)
  );
});

test('month1 < month2 does not throw', () => {
  assert.doesNotThrow(
    () => Calculator.main(4, 10, 5, 5, 2024)
  );
});
/* ---------------------------
 *  Same month calculation
 * --------------------------- */
test('same month simple difference', () => {
  assert.strictEqual(
    Calculator.main(3, 5, 3, 20, 2024),
    15
  );
});

/* ---------------------------
 *  Different months (non-leap year)
 * --------------------------- */
test('cross months (non-leap year)', () => {
  // Jan 10 -> Mar 5 (2023)
  // Jan: 31 - 10 = 21
  // Feb: 28
  // Mar: 5
  assert.strictEqual(
    Calculator.main(1, 10, 3, 5, 2023),
    21 + 28 + 5
  );
});
test('accumulates middle months correctly', () => {
  // Jan 10 → Apr 5
  // Jan: 21
  // Feb: 28
  // Mar: 31
  // Apr: 5
  assert.strictEqual(
    Calculator.main(1, 10, 4, 5, 2023),
    21 + 28 + 31 + 5
  );
});

/* ---------------------------
 *  Different months (leap year)
 * --------------------------- */
test('cross months (leap year)', () => {
  // Feb 10 -> Mar 10 (2024 leap year)
  // Feb: 29 - 10 = 19
  // Mar: 10
  assert.strictEqual(
    Calculator.main(2, 10, 3, 10, 2024),
    19 + 10
  );
});

test('accumulates middle months correctly (leap year)', () => {
  // Jan 10 → Apr 5 (2024 leap year)
  // Jan: 21
  // Feb: 29
  // Mar: 31
  // Apr: 5
  assert.strictEqual(
    Calculator.main(1, 10, 4, 5, 2024),
    21 + 29 + 31 + 5
  );
});

/* ---------------------------
 *  Leap year rules (kill all % mutants)
 * --------------------------- */
test('leap year divisible by 400', () => {
  // 2000 is leap year
  assert.strictEqual(
    Calculator.main(2, 1, 3, 1, 2000),
    29
  );
});

test('not leap year divisible by 100 only', () => {
  // 1900 is NOT leap year
  assert.strictEqual(
    Calculator.main(2, 1, 3, 1, 1900),
    28
  );
});

test('leap year divisible by 4 but not 100', () => {
  // 2024 is leap year
  assert.strictEqual(
    Calculator.main(2, 1, 3, 1, 2024),
    29
  );
});



