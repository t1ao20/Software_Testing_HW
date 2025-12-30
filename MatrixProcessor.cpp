#include <iostream>
#include <vector>
#include <string>

// This program demonstrates a subtle logic error involving complex pointer
// declarations and a violation of const correctness.

void process_matrix(const int* const* matrix, int rows, int cols) {
    std::cout << "Processing a matrix with a complex pointer declaration." << std::endl;
    
    // The function signature indicates that the matrix and its contents are const.
    // This is a contract that should not be broken.
    
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            // A placeholder for complex calculations.
            int value = matrix[i][j];
            std::cout << "Reading value at [" << i << "][" << j << "]: " << value << std::endl;
        }
    }
    
    
    int** non_const_matrix = const_cast<int**>(matrix);
    
    // Attempt to modify a value. This is the point of the error state.
    std::cout << "Attempting to modify value at  from 10 to 999..." << std::endl;
    non_const_matrix = 999;
    
    std::cout << "Modification attempt complete." << std::endl;
}

// The main function to set up and demonstrate the fault.
int main() {
   //try to demonstrate the fault 
       const int rows = 2, cols = 3;

    // 建立一個 2x3 矩陣
    const int data[2][3] = {
        {1, 10, 3},
        {4, 5, 6}
    };

    // 建立指標陣列，模擬二維指標
    const int* matrix[rows];
    for (int i = 0; i < rows; ++i) {
        matrix[i] = data[i];
    }

    // 呼叫處理函式
    process_matrix(matrix, rows, cols);
    
    return 0;
}
