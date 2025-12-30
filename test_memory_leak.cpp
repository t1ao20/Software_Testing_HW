#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <chrono>
#include <thread>

// Copy the faulty code structure to test
struct DataRecord {
    int id;
    char* data_buffer;
};

void processLargeFile_faulty(const std::string& filename) {
    std::cout << "Starting file processing for: " << filename << std::endl;
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << filename << std::endl;
        return;
    }

    std::string line;
    int recordCount = 0;
    const int bufferSize = 1024; // This variable is never used
    
    while (std::getline(file, line)) {
        // FAULT 1: Memory leak - DataRecord objects are never freed
        DataRecord* newRecord = new DataRecord();
        newRecord->id = recordCount;
        
        // FAULT 2: Only allocating 1 byte instead of bufferSize, and never freeing
        newRecord->data_buffer = new char; 
        recordCount++;
        
        // FAULT 3: The allocated objects are never deleted anywhere!
    }
    
    file.close();
    std::cout << "Finished processing " << recordCount << " records." << std::endl;
    // At this point, we have leaked recordCount * (sizeof(DataRecord) + 1 byte) memory
}

void createTestFile(const std::string& filename, int numRecords) {
    std::cout << "Creating test file with " << numRecords << " records..." << std::endl;
    std::ofstream file(filename);
    for (int i = 0; i < numRecords; ++i) {
        file << "Test record " << i << " with some data content" << std::endl;
    }
    file.close();
}

int main() {
    std::cout << "=== MEMORY LEAK TEST CASE ===" << std::endl;
    std::cout << "This test demonstrates the memory leak in DataProcessor.cpp" << std::endl;
    
    // Test Case 1: Small file to verify basic functionality
    std::cout << "\n--- Test Case 1: Small file (100 records) ---" << std::endl;
    createTestFile("small_test.txt", 100);
    processLargeFile_faulty("small_test.txt");
    
    // Test Case 2: Larger file to make memory leak more apparent
    std::cout << "\n--- Test Case 2: Large file (50000 records) ---" << std::endl;
    createTestFile("large_test.txt", 50000);
    
    std::cout << "Processing large file - monitor memory usage!" << std::endl;
    std::cout << "Expected memory leak: ~50000 DataRecord objects + 50000 char allocations" << std::endl;
    
    auto start = std::chrono::high_resolution_clock::now();
    processLargeFile_faulty("large_test.txt");
    auto end = std::chrono::high_resolution_clock::now();
    
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "Processing took: " << duration.count() << " milliseconds" << std::endl;
    
    std::cout << "\n--- Memory Leak Analysis ---" << std::endl;
    std::cout << "Memory leaked per record: sizeof(DataRecord) + 1 byte" << std::endl;
    std::cout << "Total records processed: 50100" << std::endl;
    std::cout << "Approximate memory leaked: " << (50100 * (sizeof(DataRecord) + 1)) << " bytes" << std::endl;
    
    std::cout << "\nProgram ending - leaked memory will remain until process terminates!" << std::endl;
    std::cout << "Use a memory profiler (like Valgrind, Dr. Memory, or Visual Studio Diagnostic Tools)" << std::endl;
    std::cout << "to observe the memory leak in real-time." << std::endl;
    
    // Keep program alive to observe memory usage
    std::cout << "\nPress Enter to exit and free all memory..." << std::endl;
    std::cin.get();
    
    return 0;
}