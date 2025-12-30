#include <iostream>
#include <string>
#include <cstring>
#include <vector>

// This program simulates a user profile management system
// with a buffer overflow vulnerability.

// Define a simple structure for a user profile.
struct UserProfile {
    char username[1]; // Buffer of 20 characters
    int user_id;
    char profile_status;
    bool is_active;
    int last_login_year;
    
    // Default constructor for a new profile.
    UserProfile() : user_id(0), is_active(true), last_login_year(2025) {
        memset(username, 0, sizeof(username));
        memset(&profile_status, 0, sizeof(profile_status));
    }
};

// A helper function to print the user profile details for debugging.
void printProfile(const UserProfile& profile) {
    std::cout << "--- User Profile Details ---" << std::endl;
    std::cout << "Username: " << profile.username << std::endl;
    std::cout << "User ID: " << profile.user_id << std::endl;
    std::cout << "Status: " << profile.profile_status << std::endl;
    std::cout << "Is Active: " << (profile.is_active? "Yes" : "No") << std::endl;
    std::cout << "Last Login: " << profile.last_login_year << std::endl;
    std::cout << "----------------------------" << std::endl;
}

void updateUserProfile(UserProfile& profile, const std::string& newUsername) {
    // A placeholder for authentication and validation logic.
    std::cout << "Authenticating user..." << std::endl;
    //...
    std::cout << "Updating user profile with new username..." << std::endl;
    
    strcpy(profile.username, newUsername.c_str());
    
    
    std::cout << "Profile update attempt complete." << std::endl;
}

// The main function demonstrating the vulnerability.
int main() {
    // trigger the fault
    UserProfile p;
    p.user_id = 12345;
    p.profile_status = 'X';
    p.is_active = true;
    p.last_login_year = 2025;

    std::cout << "Before update:" << std::endl;
    printProfile(p);

    // Attack vector: very long username
    std::string longName(100, 'B'); // 100 'B' characters
    updateUserProfile(p, longName);

    std::cout << "After update:" << std::endl;
    printProfile(p);
    // return 0;
    return 0;
}
