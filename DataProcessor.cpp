#include <iostream>
#include <vector>
#include <string>
#include <fstream>

// This file contains a class and a function for processing data records from a large file.
// The program is designed to demonstrate a memory leak.

// A simple structure to hold a data record.
struct DataRecord {
    int id;
    char* data_buffer; // This buffer is dynamically allocated
};

// A utility function to generate a dummy data record.
void generateDummyData(DataRecord* record, int size) {
    record->id = rand() % 1000;
    record->data_buffer = new char[size]; // Dynamic allocation
    for (int i = 0; i < size; ++i) {
        record->data_buffer[i] = 'A' + (i % 26);
    }
}

void processLargeFile(const std::string& filename) {
    std::cout << "Starting file processing for: " << filename << std::endl;
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << filename << std::endl;
        return;
    }

    std::string line;
    int recordCount = 0;
    const int bufferSize = 1024; // 1 KB buffer for each record
    
    while (std::getline(file, line)) {
        // --- FAULTY LOGIC STARTS HERE ---
        // A new DataRecord is created on the heap for each line.
        DataRecord* newRecord = new DataRecord();
        newRecord->id = recordCount;
        newRecord->data_buffer = new char; 
        recordCount++;
    }
    
    file.close();
    std::cout << "Finished processing " << recordCount << " records." << std::endl;
}

void startDataIngestion() {
    std::cout << "Running data ingestion process...\n" << std::endl;
    // Create a dummy file for demonstration.
    std::ofstream dummyFile("data.txt");
    for (int i = 0; i < 10000; ++i) {
        dummyFile << "Record " << i << std::endl;
    }
    dummyFile.close();
    
    // Call the faulty function.
    processLargeFile("data.txt");
    
}

int main() {
    startDataIngestion();
    return 0;
}
