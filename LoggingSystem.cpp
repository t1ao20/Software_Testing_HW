#include <iostream>
#include <thread>
#include <vector>
#include <mutex> // Note: The fault is the LACK of mutex use.


// A shared global variable that is a critical resource.
// The fault is that this variable is not protected by a lock.
int total_logs_processed = 0;

// The core function executed by each thread.
void processLogs(int thread_id, int num_logs_to_process) {
    std::cout << "Thread " << thread_id << " starting to process logs..." << std::endl;
    
    for (int i = 0; i < num_logs_to_process; ++i) {
        
        total_logs_processed++;
        
        std::this_thread::sleep_for(std::chrono::nanoseconds(1));
    }
    
    std::cout << "Thread " << thread_id << " finished." << std::endl;
}

// A function to set up and run the threads.
void startProcessing(int num_threads, int logs_per_thread) {
    std::cout << "Expected total logs: " << num_threads * logs_per_thread << std::endl;
    std::cout << "Starting log processing with " << num_threads << " threads." << std::endl;
    
    std::vector<std::thread> threads;
    for (int i = 0; i < num_threads; ++i) {
        threads.push_back(std::thread(processLogs, i, logs_per_thread));
    }
    
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "\nAll threads have finished." << std::endl;
    std::cout << "Final count of logs processed: " << total_logs_processed << std::endl;
}

int main() {
    const int NUM_THREADS = 10;
    const int LOGS_PER_THREAD = 10000;
    
    // Run the program multiple times to observe the race condition.
    std::cout << "Running race condition example..." << std::endl;
    startProcessing(NUM_THREADS, LOGS_PER_THREAD);
    
    return 0;
}
