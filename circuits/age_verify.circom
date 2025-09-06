pragma circom 2.0.0;

include "circomlib/circuits/comparators.circom";
include "circomlib/circuits/poseidon.circom";

// Age verification circuit
template AgeVerification() {
    signal input birth_year;
    signal input current_year; 
    signal input min_age;
    signal input nonce; // For privacy
    
    signal output is_valid;
    signal output commitment;
    
    // Check if age >= min_age
    component age_check = GreaterEqThan(8);
    age_check.in[0] <== current_year - birth_year;
    age_check.in[1] <== min_age;
    
    is_valid <== age_check.out;
    
    // Create commitment to hide actual birth year
    component hasher = Poseidon(3);
    hasher.inputs[0] <== birth_year;
    hasher.inputs[1] <== nonce;
    hasher.inputs[2] <== current_year;
    
    commitment <== hasher.out;
}

component main = AgeVerification();