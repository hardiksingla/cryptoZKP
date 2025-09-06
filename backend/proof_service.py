import json
import os
import tempfile
import subprocess
from typing import Dict, List
from models import AgeProof

class ProofService:
    def __init__(self):
        self.current_year = 2024
        
    def generate_age_proof(self, birth_year: int, nonce: int, min_age: int = 18) -> AgeProof:
        """Generate zero-knowledge proof of age (simplified version)"""
        
        # For demo purposes, we'll simulate the ZK proof
        # In a real implementation, this would use actual zkSNARK circuits
        
        age = self.current_year - birth_year
        is_old_enough = age >= min_age
        
        # Simulate proof generation
        proof_data = {
            "pi_a": ["0x1234", "0x5678", "0x1"],
            "pi_b": [["0xabcd", "0xefgh"], ["0x9876", "0x5432"], ["0x1", "0x0"]],
            "pi_c": ["0xdeaf", "0xbeef", "0x1"],
            "protocol": "groth16"
        }
        
        # Public signals: [is_old_enough, commitment]
        from crypto_utils import create_commitment
        commitment = create_commitment(birth_year, nonce, self.current_year)
        
        public_signals = [
            1 if is_old_enough else 0,  # Result of age check
            int(commitment[:16], 16) % (2**32)  # Commitment (truncated for demo)
        ]
        
        return AgeProof(
            proof=proof_data,
            public_signals=public_signals,
            is_valid=True  # In real implementation, this would be verified
        )
    
    def verify_age_proof(self, proof: Dict, public_signals: List) -> bool:
        """Verify a zero-knowledge age proof"""
        # For demo purposes, always return True if proof structure is valid
        required_keys = ["pi_a", "pi_b", "pi_c", "protocol"]
        return all(key in proof for key in required_keys)