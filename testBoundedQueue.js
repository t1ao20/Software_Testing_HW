const assert = require("assert");
const { BoundedQueue } = require("./BoundedQueue.js"); // modify export if needed

function runTests() {
    console.log("Running BoundedQueue ISP + BCC tests...\n");

    // === Constructor Tests ===
    assert.throws(() => new BoundedQueue(-1), RangeError, "C-B1 failed");
    console.log("C-B1 passed");

    const bq0 = new BoundedQueue(0);
    assert.strictEqual(bq0.capacity, 0, "C-B2 failed");
    console.log("C-B2 passed");

    const bq3 = new BoundedQueue(3);
    assert.strictEqual(bq3.is_empty(), true, "C-B3 failed");
    assert.strictEqual(bq3.capacity, 3, "C-B3 failed");
    console.log("C-B3 passed");

    // === C-B4 ===
    assert.throws(() => new BoundedQueue("Miku"), TypeError, "C-B4 failed");
    console.log("C-B4 passed");

    // === Enqueue Tests ===
    const bq = new BoundedQueue(3);
    // base setup: one element in queue
    bq.enqueue(1);
    assert.strictEqual(bq.size, 1, "E-B1 failed");  
    console.log("E-B1 passed");

    assert.throws(() => bq.enqueue("Miku"), RangeError, "E-B2 failed");
    console.log("E-B2 passed");

    assert.throws(() => bq.enqueue(NaN), RangeError, "E-B3 failed");
    console.log("E-B3 passed");

    // Fill queue to full
    bq.enqueue(2);
    bq.enqueue(3);
    assert.throws(() => bq.enqueue(4), Error, "Q-B1 failed");
    console.log("Q-B1 passed");

    // Enqueue on empty queue
    const bqEmpty = new BoundedQueue(3);
    bqEmpty.enqueue(5);
    assert.strictEqual(bqEmpty.size, 1, "Q-B2 failed");
    assert.strictEqual(bqEmpty.back, 1, "Q-B2 failed");  
    assert.deepStrictEqual(bqEmpty.elements[0], 5, "Q-B2 failed");
    console.log("Q-B2 passed");

    bqEmpty.enqueue(5);
    assert.strictEqual(bqEmpty.size, 2, "Q-B3 failed");
    assert.strictEqual(bqEmpty.back, 2, "Q-B3 failed");  
    assert.deepStrictEqual(bqEmpty.elements[1], 5, "Q-B3 failed");
    console.log("Q-B3 passed");

    // === Dequeue Tests ===
    const bqDeq = new BoundedQueue(2);
    assert.throws(() => bqDeq.dequeue(), Error, "D-B1 failed");
    console.log("D-B1 passed");

    bqDeq.enqueue(1);
    bqDeq.enqueue(2);
    const val = bqDeq.dequeue();
    assert.strictEqual(val, 1, "D-B2 failed");
    console.log("D-B2 passed");

    console.log("\nAll tests passed successfully!");
}

runTests();
