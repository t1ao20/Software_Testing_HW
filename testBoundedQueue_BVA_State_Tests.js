const assert = require("assert");
const { BoundedQueue } = require("./BoundedQueue.js");

function runAdvancedTests() {
    console.log("\n=== Running BoundedQueue BVA + State Tests ===\n");

    // --- BVA Tests ---
    assert.throws(() => new BoundedQueue(-1), RangeError, "BVA1 failed");
    console.log("BVA1 passed");

    const bq0 = new BoundedQueue(0);
    assert.throws(() => bq0.enqueue(1), /queue is full/, "BVA2 failed");
    console.log("BVA2 passed");

    const bq1 = new BoundedQueue(1);
    bq1.enqueue(10);
    assert.throws(() => bq1.enqueue(20), /queue is full/, "BVA3 failed");
    console.log("BVA3 passed");

    const bq2 = new BoundedQueue(2);
    bq2.enqueue(1);
    bq2.enqueue(2);
    assert.throws(() => bq2.enqueue(3), /queue is full/, "BVA4 failed");
    console.log("BVA4 passed");

    const bq5 = new BoundedQueue(2);
    bq5.enqueue(1);
    const val5 = bq5.dequeue();
    assert.strictEqual(val5, 1, "BVA5 failed");
    assert.strictEqual(bq5.is_empty(), true, "BVA5 failed is_empty()");
    console.log("BVA5 passed");

    const bq6 = new BoundedQueue(2);
    bq6.enqueue(1);
    bq6.enqueue(2);
    const v1 = bq6.dequeue(); // remove front
    bq6.enqueue(3);            // wraps around
    const v2 = bq6.dequeue();  // should return 2
    const v3 = bq6.dequeue();  // should return 3
    assert.deepStrictEqual([v1, v2, v3], [1, 2, 3], "BVA6 wrap-around failed");
    console.log("BVA6 passed (wrap-around logic OK)");

    // --- Sequence/State Tests ---
    const seq1 = new BoundedQueue(3);
    seq1.enqueue(10);
    seq1.enqueue(20);
    seq1.enqueue(30);
    seq1.dequeue();
    seq1.enqueue(40); // Wrap-around
    assert.deepStrictEqual(seq1.toString().includes("is_full(): true"), true, "SEQ1 failed");
    console.log("SEQ1 passed");

    const seq2 = new BoundedQueue(2);
    seq2.enqueue(1);
    seq2.enqueue(2);
    seq2.dequeue();
    seq2.dequeue();
    seq2.enqueue(99);
    assert.strictEqual(seq2.dequeue(), 99, "SEQ2 failed");
    console.log("SEQ2 passed");

    const seq3 = new BoundedQueue(2);
    seq3.enqueue(5);
    seq3.enqueue(10);
    assert.strictEqual(seq3.is_full(), true, "SEQ3 failed");
    console.log("SEQ3 passed");

    const seq4 = new BoundedQueue(2);
    seq4.enqueue(1);
    seq4.dequeue();
    assert.strictEqual(seq4.is_empty(), true, "SEQ4 failed");
    console.log("SEQ4 passed");

    console.log("\nAll advanced BVA + state-based tests passed successfully!");
}

runAdvancedTests();
