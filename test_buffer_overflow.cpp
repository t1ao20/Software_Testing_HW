#include <iostream>
#include <string>
#include <cstring>
#include <vector>

// Test case for buffer overflow in ProfileUpdater.cpp
// The fault is using strcpy with a 1-byte buffer

struct UserProfile {
    char username[1]; // FAULT: Buffer of only 1 byte (should be much larger)
    int user_id;
    char profile_status;
    bool is_active;
    int last_login_year;
    
    UserProfile() : user_id(0), is_active(true), last_login_year(2025) {
        memset(username, 0, sizeof(username));
        profile_status = 'A'; // Fixed: memset on char instead of array
    }
};

void printProfile(const UserProfile& profile) {
    std::cout << "--- User Profile Details ---" << std::endl;
    std::cout << "Username: " << profile.username << std::endl; // May print garbage
    std::cout << "User ID: " << profile.user_id << std::endl;
    std::cout << "Status: " << profile.profile_status << std::endl;
    std::cout << "Is Active: " << (profile.is_active ? "Yes" : "No") << std::endl;
    std::cout << "Last Login: " << profile.last_login_year << std::endl;
    std::cout << "----------------------------" << std::endl;
}

void updateUserProfile_faulty(UserProfile& profile, const std::string& newUsername) {
    std::cout << "Authenticating user..." << std::endl;
    std::cout << "Updating user profile with new username: '" << newUsername << "'" << std::endl;
    std::cout << "Username length: " << newUsername.length() << " bytes" << std::endl;
    std::cout << "Buffer size: " << sizeof(profile.username) << " byte(s)" << std::endl;
    
    if (newUsername.length() >= sizeof(profile.username)) {
        std::cout << "WARNING: Username too long for buffer! Buffer overflow will occur!" << std::endl;
    }
    
    // FAULT: strcpy doesn't check bounds - will overflow the 1-byte buffer
    strcpy(profile.username, newUsername.c_str());
    
    std::cout << "Profile update attempt complete." << std::endl;
}

void demonstrateCorruption(UserProfile& profile) {
    std::cout << "\n=== MEMORY CORRUPTION ANALYSIS ===" << std::endl;
    
    // Show memory layout around the profile
    unsigned char* profileBytes = reinterpret_cast<unsigned char*>(&profile);
    std::cout << "Profile memory layout (first 16 bytes):" << std::endl;
    for (int i = 0; i < 16; ++i) {
        std::cout << "Byte " << i << ": 0x" << std::hex << (int)profileBytes[i] 
                  << " ('" << (char)(profileBytes[i] >= 32 && profileBytes[i] < 127 ? profileBytes[i] : '.') << "')" << std::endl;
    }
    std::cout << std::dec; // Reset to decimal
}

int main() {
    std::cout << "=== BUFFER OVERFLOW VULNERABILITY TEST ===" << std::endl;
    std::cout << "This test demonstrates the buffer overflow in ProfileUpdater.cpp" << std::endl;
    std::cout << "The username buffer is only 1 byte but strcpy is used without bounds checking." << std::endl;
    
    // Test Case 1: Safe username (fits in 1 byte)
    std::cout << "\n--- Test Case 1: Safe username (empty string) ---" << std::endl;
    UserProfile profile1;
    profile1.user_id = 12345;
    profile1.profile_status = 'A';
    
    std::cout << "Before update:" << std::endl;
    printProfile(profile1);
    demonstrateCorruption(profile1);
    
    updateUserProfile_faulty(profile1, ""); // Empty string fits
    
    std::cout << "After safe update:" << std::endl;
    printProfile(profile1);
    
    // Test Case 2: Small overflow (2-3 characters)
    std::cout << "\n--- Test Case 2: Small buffer overflow (2-3 chars) ---" << std::endl;
    UserProfile profile2;
    profile2.user_id = 67890;
    profile2.profile_status = 'B';
    
    std::cout << "Before update:" << std::endl;
    printProfile(profile2);
    demonstrateCorruption(profile2);
    
    updateUserProfile_faulty(profile2, "AB"); // 2 chars + null = 3 bytes, overflows 1-byte buffer
    
    std::cout << "After small overflow:" << std::endl;
    printProfile(profile2);
    demonstrateCorruption(profile2);
    
    // Test Case 3: Large overflow (normal username)
    std::cout << "\n--- Test Case 3: Large buffer overflow (normal username) ---" << std::endl;
    UserProfile profile3;
    profile3.user_id = 99999;
    profile3.profile_status = 'C';
    
    std::cout << "Before update:" << std::endl;
    printProfile(profile3);
    demonstrateCorruption(profile3);
    
    updateUserProfile_faulty(profile3, "john_doe_123"); // 12 chars, massive overflow
    
    std::cout << "After large overflow:" << std::endl;
    printProfile(profile3);
    demonstrateCorruption(profile3);
    
    // Test Case 4: Very large overflow (potential crash)
    std::cout << "\n--- Test Case 4: Very large buffer overflow (may crash) ---" << std::endl;
    UserProfile profile4;
    profile4.user_id = 11111;
    profile4.profile_status = 'D';
    
    std::cout << "Before update:" << std::endl;
    printProfile(profile4);
    
    std::string longUsername = "this_is_a_very_long_username_that_will_definitely_cause_buffer_overflow_and_memory_corruption";
    std::cout << "Attempting to write " << longUsername.length() << " characters to 1-byte buffer..." << std::endl;
    std::cout << "WARNING: This may crash the program!" << std::endl;
    
    try {
        updateUserProfile_faulty(profile4, longUsername);
        
        std::cout << "After very large overflow (if program didn't crash):" << std::endl;
        printProfile(profile4);
        demonstrateCorruption(profile4);
    } catch (...) {
        std::cout << "Program crashed due to buffer overflow!" << std::endl;
    }
    
    std::cout << "\n=== BUFFER OVERFLOW ANALYSIS ===" << std::endl;
    std::cout << "The fault occurs because:" << std::endl;
    std::cout << "1. Username buffer is only 1 byte (should be at least 20-50 bytes)" << std::endl;
    std::cout << "2. strcpy() doesn't check destination buffer size" << std::endl;
    std::cout << "3. Writing beyond buffer corrupts adjacent memory (user_id, status, etc.)" << std::endl;
    std::cout << "4. Large overflows can corrupt stack/heap and cause crashes" << std::endl;
    std::cout << "5. This could lead to security vulnerabilities (code injection)" << std::endl;
    
    return 0;
}