"""
WCOIN Block
区块模块
"""

import hashlib
import json
import time
from .transaction import Transaction


class Block:
    """区块类"""
    
    def __init__(self, index, transactions, previous_hash, difficulty):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = ""
        
    def calculate_hash(self):
        """计算区块哈希"""
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'difficulty': self.difficulty,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
        
    def mine_block(self):
        """挖矿 - 寻找满足难度要求的nonce"""
        target = '0' * self.difficulty
        
        while True:
            self.hash = self.calculate_hash()
            if self.hash[:self.difficulty] == target:
                return self.hash
            self.nonce += 1
            
    def is_valid(self):
        """验证区块有效性"""
        if self.hash != self.calculate_hash():
            return False
            
        target = '0' * self.difficulty
        if self.hash[:self.difficulty] != target:
            return False
            
        return True
        
    def to_dict(self):
        """转换为字典"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'difficulty': self.difficulty,
            'nonce': self.nonce,
            'hash': self.hash
        }
        
    @classmethod
    def from_dict(cls, data):
        """从字典创建区块"""
        transactions = [Transaction.from_dict(tx) for tx in data['transactions']]
        block = cls(
            data['index'],
            transactions,
            data['previous_hash'],
            data['difficulty']
        )
        block.timestamp = data['timestamp']
        block.nonce = data['nonce']
        block.hash = data['hash']
        return block
