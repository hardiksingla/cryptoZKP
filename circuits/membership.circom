pragma circom 2.0.0;

include "circomlib/circuits/poseidon.circom";
include "circomlib/circuits/merkletree.circom";

// Merkle tree membership proof
template MembershipProof(levels) {
    signal input leaf;
    signal input pathElements[levels];
    signal input pathIndices[levels];
    signal input root;
    
    signal output valid;
    
    component merkletree = MerkleTreeChecker(levels);
    merkletree.leaf <== leaf;
    merkletree.root <== root;
    
    for (var i = 0; i < levels; i++) {
        merkletree.pathElements[i] <== pathElements[i];
        merkletree.pathIndices[i] <== pathIndices[i];
    }
    
    valid <== merkletree.out;
}

component main = MembershipProof(10);