import hashlib
from typing import List, Tuple, Optional

class SimpleMerkleTree:
    def __init__(self):
        self.leaves = []
        self.tree = []
    
    def _hash(self, data: str) -> str:
        """Hash function for merkle tree"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _build_tree(self):
        """Build the merkle tree"""
        if not self.leaves:
            return
        
        # Start with leaves (already hashed)
        current_level = [self._hash(leaf) for leaf in self.leaves]
        self.tree = [current_level[:]]
        
        # Build tree bottom up
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                parent = self._hash(left + right)
                next_level.append(parent)
            
            current_level = next_level
            self.tree.append(current_level[:])
    
    def add_leaf(self, data: str) -> int:
        """Add leaf and return its index"""
        self.leaves.append(data)
        self._build_tree()
        return len(self.leaves) - 1
    
    def get_proof(self, index: int) -> Tuple[List[str], List[int]]:
        """Get merkle proof for leaf at index"""
        if index >= len(self.leaves):
            return [], []
        
        path_elements = []
        path_indices = []
        current_index = index
        
        # Traverse from leaf to root
        for level in range(len(self.tree) - 1):
            level_nodes = self.tree[level]
            
            if current_index % 2 == 0:  # Left child
                if current_index + 1 < len(level_nodes):
                    sibling = level_nodes[current_index + 1]
                    path_indices.append(1)  # Sibling is on the right
                else:
                    sibling = level_nodes[current_index]  # Self if odd number
                    path_indices.append(0)
            else:  # Right child
                sibling = level_nodes[current_index - 1]
                path_indices.append(0)  # Sibling is on the left
            
            path_elements.append(sibling)
            current_index = current_index // 2
        
        return path_elements, path_indices
    
    def get_root(self) -> str:
        """Get merkle tree root"""
        if not self.tree:
            return "0"
        return self.tree[-1][0] if self.tree[-1] else "0"
    
    def verify_proof(self, leaf: str, proof_elements: List[str], 
                     proof_indices: List[int], root: str) -> bool:
        """Verify a merkle proof"""
        current_hash = self._hash(leaf)
        
        for i, (sibling, is_right) in enumerate(zip(proof_elements, proof_indices)):
            if is_right:
                current_hash = self._hash(current_hash + sibling)
            else:
                current_hash = self._hash(sibling + current_hash)
        
        return current_hash == root