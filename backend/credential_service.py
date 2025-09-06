from typing import Dict, Optional
from models import MockPassport, Credential
from merkle_tree import SimpleMerkleTree
from crypto_utils import create_commitment, generate_nonce

class CredentialService:
    def __init__(self):
        self.merkle_tree = SimpleMerkleTree()
        self.credentials = {}  # commitment -> credential mapping
        
    def issue_credential(self, passport: MockPassport) -> Credential:
        """Issue anonymous credential based on passport data"""
        
        # Generate random nonce for privacy
        nonce = generate_nonce()
        
        # Create commitment
        commitment = create_commitment(passport.birth_year, nonce)
        
        # Add to merkle tree
        leaf_index = self.merkle_tree.add_leaf(commitment)
        
        # Get merkle path
        path_elements, path_indices = self.merkle_tree.get_proof(leaf_index)
        
        # Create credential
        credential = Credential(
            commitment=commitment,
            birth_year=passport.birth_year,
            nonce=nonce,
            merkle_path=path_elements,
            merkle_index=leaf_index
        )
        
        # Store credential
        self.credentials[commitment] = credential
        
        return credential
    
    def get_credential(self, commitment: str) -> Optional[Credential]:
        return self.credentials.get(commitment)
    
    def get_merkle_root(self) -> str:
        return self.merkle_tree.get_root()
    
    def verify_credential_membership(self, commitment: str) -> bool:
        """Verify that a credential is in the merkle tree"""
        credential = self.get_credential(commitment)
        if not credential:
            return False
        
        return self.merkle_tree.verify_proof(
            commitment,
            credential.merkle_path,
            [0] * len(credential.merkle_path),  # Simplified for demo
            self.get_merkle_root()
        )