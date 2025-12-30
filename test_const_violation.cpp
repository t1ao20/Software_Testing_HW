#include <iostream>
#include <vector>

// Test case for const correctness violation in MatrixProcessor.cpp
// The fault is using const_cast to modify supposedly const data

void process_matrix_faulty(const int* const* matrix, int rows, int cols) {
    std::cout << "Processing a matrix with const parameters..." << std::endl;
    
    // The function signature indicates that the matrix and its contents are const
    std::cout << "Matrix contents (should be read-only):" << std::endl;
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            int value = matrix[i][j];
            std::cout << "matrix[" << i << "][" << j << "] = " << value << " ";
        }
        std::cout << std::endl;
    }
    
    // FAULT: Using const_cast to remove const protection
    std::cout << "\n*** CONST VIOLATION FAULT ***" << std::endl;
    int** non_const_matrix = const_cast<int**>(matrix);
    
    // FAULT: Attempting to modify supposedly const data
    std::cout << "Attempting to modify matrix[0][0] from " << matrix[0][0] << " to 999..." << std::endl;
    non_const_matrix[0][0] = 999;  // This violates const correctness!
    
    std::cout << "After modification, matrix[0][0] = " << matrix[0][0] << std::endl;
    std::cout << "Const violation completed - undefined behavior may occur!" << std::endl;
}

int main() {
    std::cout << "=== CONST CORRECTNESS VIOLATION TEST ===" << std::endl;
    std::cout << "This test demonstrates const_cast abuse in MatrixProcessor.cpp" << std::endl;
    
    // Test Case 1: Create a matrix and pass it to the faulty function
    const int rows = 3;
    const int cols = 3;
    
    // Create matrix data
    int* matrix_data = new int[rows * cols];
    int** matrix = new int*[rows];
    
    // Initialize matrix
    int value = 10;
    for (int i = 0; i < rows; ++i) {
        matrix[i] = &matrix_data[i * cols];
        for (int j = 0; j < cols; ++j) {
            matrix[i][j] = value++;
        }
    }
    
    std::cout << "\n--- Test Case 1: Normal matrix (modifiable source) ---" << std::endl;
    std::cout << "Original matrix:" << std::endl;
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }
    
    // Cast to const and call faulty function
    const int* const* const_matrix = const_cast<const int* const*>(matrix);
    process_matrix_faulty(const_matrix, rows, cols);
    
    std::cout << "\nMatrix after const violation:" << std::endl;
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }
    
    // Test Case 2: Truly const data (more dangerous)
    std::cout << "\n--- Test Case 2: Truly const data (undefined behavior) ---" << std::endl;
    const int const_array[2][2] = {{100, 200}, {300, 400}};
    const int* const_ptrs[2] = {const_array[0], const_array[1]};
    
    std::cout << "Attempting to modify truly const data..." << std::endl;
    std::cout << "WARNING: This may cause undefined behavior, crash, or corruption!" << std::endl;
    
    try {
        process_matrix_faulty(const_ptrs, 2, 2);
    } catch (...) {
        std::cout << "Exception caught during const violation!" << std::endl;
    }
    
    std::cout << "\n=== CONST VIOLATION ANALYSIS ===" << std::endl;
    std::cout << "The fault occurs because:" << std::endl;
    std::cout << "1. const_cast removes compile-time const protection" << std::endl;
    std::cout << "2. Modifying originally const data leads to undefined behavior" << std::endl;
    std::cout << "3. The compiler assumes const data won't change (optimization issues)" << std::endl;
    std::cout << "4. This breaks the contract established by the function signature" << std::endl;
    
    // Clean up
    delete[] matrix_data;
    delete[] matrix;
    
    return 0;
}