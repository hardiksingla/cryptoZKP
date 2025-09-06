from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import hashlib

@dataclass
class MockPassport:
    name: str
    birth_year: int
    country: str
    passport_number: str
    expiry_year: int

@dataclass
class Credential:
    commitment: str
    birth_year: int
    nonce: int
    merkle_path: Optional[List[str]] = None
    merkle_index: Optional[int] = None

@dataclass 
class AgeProof:
    proof: Dict
    public_signals: List[int]
    is_valid: bool