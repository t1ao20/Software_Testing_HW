/*
 * A BoundedQueue is a mutable, bounded FIFO data structure
 * of fixed size, with size being set in the constructor
 * A typical Queue is [], [o1], or [o1, o2], where neither o1 nor o2
 * are ever null. Older elements are listed before newer ones.
 */
class BoundedQueue {
    constructor(capacity) {
        if (typeof capacity !== "number" || isNaN(capacity) || !Number.isInteger(capacity)) {
            throw new TypeError("capacity is not an integer");
        }
        if (capacity < 0) {
            throw new RangeError("capacity is less than 0");
        }
        this.capacity = capacity;
        this.elements = [];
        this.size = 0;
        this.front = 0;
        this.back = 0;
    }

    enqueue(element) {
        if (typeof element !== "number" || isNaN(element)) {
            throw new RangeError("element is invalid");
        }
        else if (this.is_full()) {
            throw new Error("queue is full");
        }
        this.size++;
        this.elements[this.back] = element;
        this.back = (this.back + 1) % this.capacity;
    }

    dequeue() {
        if (this.is_empty()) {
            throw new Error("queue is empty");
        }
        this.size--;
        let o = this.elements[this.front];
        this.elements[this.front] = null;
        this.front = (this.front + 1) % this.capacity;
        return o;
    }

    is_empty() {
        return this.size === 0;
    }

    is_full() {
        return this.size === this.capacity;
    }

    toString() {
        let result = "[";
        for (let i = 0; i < this.size; i++) {
            result += this.elements[(this.front + i) % this.capacity];
            if (i < this.size - 1) {
                result += ", ";
            }
        }
        result += "] ";
        result += "is_empty(): " + this.is_empty() + ", is_full(): " + this.is_full();
        return result;
    }
}

// bq = new BoundedQueue(10);

// console.log(bq.toString());

// for (let i = 0; i < 10; i++) {
//     bq.enqueue(i);
// }

// console.log(bq.toString());

// for (let i = 0; i < 3; i++) {
//     bq.dequeue();
// }

// console.log(bq.toString());

// for (let i = 1; i < 3; i++) {
//     bq.enqueue(i);
// }

// console.log(bq.toString());
module.exports = { BoundedQueue };
