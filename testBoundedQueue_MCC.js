const assert = require("assert");
const { BoundedQueue } = require("./BoundedQueue.js");

function runMCCTests() {
    console.log("\n=== Running BoundedQueue MCC Tests (enqueue) ===\n");

    // Helper: fill queue with n elements
    function makeQueue(capacity, numFilled) {
        const q = new BoundedQueue(capacity);
        for (let i = 0; i < numFilled; i++) q.enqueue(i);
        return q;
    }

    // --- MCC1 ---
    let q1 = makeQueue(3, 0);
    q1.enqueue(5);
    assert.strictEqual(q1.size, 1);
    console.log("MCC1 passed");

    // --- MCC2 ---
    let q2 = makeQueue(3, 1);
    q2.enqueue(6);
    assert.strictEqual(q2.size, 2);
    console.log("MCC2 passed");

    // --- MCC3 ---
    let q3 = makeQueue(3, 3);
    assert.throws(() => q3.enqueue(7), /queue is full/);
    console.log("MCC3 passed");

    // --- MCC4 ---
    let q4 = makeQueue(3, 0);
    assert.throws(() => q4.enqueue("abc"), /element is invalid/);
    console.log("MCC4 passed");

    // --- MCC5 ---
    let q5 = makeQueue(3, 1);
    assert.throws(() => q5.enqueue("abc"), /element is invalid/);
    console.log("MCC5 passed");

    // --- MCC6 ---
    let q6 = makeQueue(3, 3);
    assert.throws(() => q6.enqueue("abc"), /element is invalid/);
    console.log("MCC6 passed");

    // --- MCC7 ---
    let q7 = makeQueue(3, 0);
    assert.throws(() => q7.enqueue(NaN), /element is invalid/);
    console.log("MCC7 passed");

    // --- MCC8 ---
    let q8 = makeQueue(3, 1);
    assert.throws(() => q8.enqueue(NaN), /element is invalid/);
    console.log("MCC8 passed");

    // --- MCC9 ---
    let q9 = makeQueue(3, 3);
    assert.throws(() => q9.enqueue(NaN), /element is invalid/);
    console.log("MCC9 passed");

    console.log("\nAll MCC tests passed successfully!");
}

runMCCTests();
