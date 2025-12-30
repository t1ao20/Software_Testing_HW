#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <chrono>

// Race condition test based on LoggingSystem.cpp
// The fault is that total_logs_processed is not protected by a mutex

int total_logs_processed = 0;

// Faulty version - no synchronization
void processLogs_faulty(int thread_id, int num_logs_to_process) {
    std::cout << "Thread " << thread_id << " starting to process logs..." << std::endl;
    
    for (int i = 0; i < num_logs_to_process; ++i) {
        // FAULT: Race condition - multiple threads modifying shared variable
        total_logs_processed++;  // This is not atomic and not synchronized!
        
        std::this_thread::sleep_for(std::chrono::nanoseconds(1));
    }
    
    std::cout << "Thread " << thread_id << " finished." << std::endl;
}

// Test function to demonstrate race condition
void testRaceCondition(int num_threads, int logs_per_thread) {
    total_logs_processed = 0;  // Reset counter
    
    int expected_total = num_threads * logs_per_thread;
    std::cout << "\n=== RACE CONDITION TEST ===" << std::endl;
    std::cout << "Expected total logs: " << expected_total << std::endl;
    std::cout << "Starting log processing with " << num_threads << " threads." << std::endl;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    std::vector<std::thread> threads;
    for (int i = 0; i < num_threads; ++i) {
        threads.push_back(std::thread(processLogs_faulty, i, logs_per_thread));
    }
    
    for (auto& t : threads) {
        t.join();
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "\nAll threads have finished." << std::endl;
    std::cout << "Expected count: " << expected_total << std::endl;
    std::cout << "Actual count: " << total_logs_processed << std::endl;
    std::cout << "Difference: " << (expected_total - total_logs_processed) << std::endl;
    std::cout << "Processing time: " << duration.count() << " ms" << std::endl;
    
    if (total_logs_processed != expected_total) {
        std::cout << "*** RACE CONDITION DETECTED! ***" << std::endl;
        std::cout << "The actual count differs from expected due to lost updates." << std::endl;
    } else {
        std::cout << "No race condition detected in this run (may occur randomly)." << std::endl;
    }
}

int main() {
    std::cout << "=== RACE CONDITION TEST SUITE ===" << std::endl;
    std::cout << "This test demonstrates the race condition in LoggingSystem.cpp" << std::endl;
    std::cout << "Multiple threads increment a shared counter without synchronization." << std::endl;
    
    // Test Case 1: Low contention
    std::cout << "\n--- Test Case 1: Low contention (2 threads, 1000 ops each) ---" << std::endl;
    testRaceCondition(2, 1000);
    
    // Test Case 2: Medium contention  
    std::cout << "\n--- Test Case 2: Medium contention (5 threads, 5000 ops each) ---" << std::endl;
    testRaceCondition(5, 5000);
    
    // Test Case 3: High contention - more likely to show race condition
    std::cout << "\n--- Test Case 3: High contention (10 threads, 10000 ops each) ---" << std::endl;
    testRaceCondition(10, 10000);
    
    // Test Case 4: Very high contention
    std::cout << "\n--- Test Case 4: Very high contention (20 threads, 50000 ops each) ---" << std::endl;
    testRaceCondition(20, 50000);
    
    std::cout << "\n=== RACE CONDITION ANALYSIS ===" << std::endl;
    std::cout << "The fault occurs because:" << std::endl;
    std::cout << "1. Multiple threads access 'total_logs_processed' simultaneously" << std::endl;
    std::cout << "2. The increment operation (++) is not atomic" << std::endl;
    std::cout << "3. No mutex protection causes lost updates" << std::endl;
    std::cout << "4. The read-modify-write sequence can be interleaved between threads" << std::endl;
    
    std::cout << "\nRun this test multiple times to see different results!" << std::endl;
    std::cout << "The race condition may not always manifest, making it hard to debug." << std::endl;
    
    return 0;
}