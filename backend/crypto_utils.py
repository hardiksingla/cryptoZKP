import hashlib
import secrets
from typing import List

def poseidon_hash_simple(*inputs) -> str:
    """Simple hash function as placeholder for Poseidon hash"""
    # In a real implementation, this would be the Poseidon hash function
    # For demo purposes, we'll use SHA256
    combined = ":".join(str(x) for x in inputs)
    return hashlib.sha256(combined.encode()).hexdigest()

def create_commitment(birth_year: int, nonce: int, current_year: int = 2024) -> str:
    """Create a commitment hash"""
    return poseidon_hash_simple(birth_year, nonce, current_year)

def generate_nonce() -> int:
    """Generate a random nonce"""
    return secrets.randbelow(2**32)