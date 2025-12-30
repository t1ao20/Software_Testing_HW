import threading
import time
import logging
import queue
# This program demonstrates a classic multithreaded deadlock scenario.

# Setup basic logging to see thread activity.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(threadName)s | %(message)s'
)

# Define two shared resources, each protected by a lock.
lock_resource_a = threading.Lock()
lock_resource_b = threading.Lock()

# A shared queue to manage tasks.
# Although not directly part of the deadlock, it adds to the program's complexity.
task_queue = queue.Queue()

# This function simulates a complex, multi-stage task.
def complex_task_function(task_id):
    logging.info(f"Starting complex task {task_id}.")
    for i in range(5):
        time.sleep(0.5)
        logging.info(f"Task {task_id} is in progress, step {i+1}...")
    logging.info(f"Task {task_id} completed.")
    return True

# The first faulty thread function.
# It attempts to acquire locks in the order: A then B.
def worker_thread_a(thread_name):
    logging.info(f"{thread_name} is starting.")
    logging.info(f"{thread_name} attempting to acquire lock on Resource A...")
    
    lock_resource_a.acquire()
    logging.info(f"{thread_name} acquired lock on Resource A. Waiting for Resource B...")
    
    time.sleep(1)
    
    lock_resource_b.acquire()
    
    
    logging.info(f"{thread_name} acquired lock on Resource B. Critical section entered.")
    # Perform the critical task.
    complex_task_function(1)
    
    # Release the locks.
    lock_resource_b.release()
    lock_resource_a.release()
    
    logging.info(f"{thread_name} finished and released both locks.")

# The second faulty thread function.
# It attempts to acquire locks in the order: B then A, causing a deadlock.
def worker_thread_b(thread_name):
    logging.info(f"{thread_name} is starting.")
    logging.info(f"{thread_name} attempting to acquire lock on Resource B...")
    
    lock_resource_b.acquire()
    logging.info(f"{thread_name} acquired lock on Resource B. Waiting for Resource A...")
    
    time.sleep(1)
    
    lock_resource_a.acquire()
    
    
    logging.info(f"{thread_name} acquired lock on Resource A. Critical section entered.")
    # Perform the critical task.
    complex_task_function(2)
    
    # Release the locks.
    lock_resource_a.release()
    lock_resource_b.release()
    
    logging.info(f"{thread_name} finished and released both locks.")

def test_deadlock_scenario():
    # Create two threads, each running one of the faulty worker functions
    thread1 = threading.Thread(target=worker_thread_a, args=("Thread-A",), name="Thread-A")
    thread2 = threading.Thread(target=worker_thread_b, args=("Thread-B",), name="Thread-B")

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait a few seconds for the deadlock to occur
    time.sleep(5)

    thread1.join(timeout=1)
    thread2.join(timeout=1)

    # Check if both threads are still alive after the wait → sign of deadlock
    if thread1.is_alive() and thread2.is_alive():
        logging.error("Deadlock detected: Both threads are stuck waiting for each other.")
    else:
        logging.info("No deadlock detected (unexpected).")
        logging.info("All threads completed.")
        
# The main function to set up and run the threads.
if __name__ == "__main__":
    test_deadlock_scenario()
