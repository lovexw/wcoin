"""
WCOIN Transaction
交易模块
"""

import hashlib
import json
import time


class Transaction:
    """交易类"""
    
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.signature = signature
        self.txid = self._calculate_hash()
        
    def _calculate_hash(self):
        """计算交易哈希"""
        tx_data = {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
        tx_string = json.dumps(tx_data, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()
        
    def to_dict(self):
        """转换为字典"""
        return {
            'txid': self.txid,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'signature': self.signature
        }
        
    @classmethod
    def from_dict(cls, data):
        """从字典创建交易"""
        tx = cls(
            data['sender'],
            data['recipient'],
            data['amount'],
            data.get('signature')
        )
        tx.timestamp = data['timestamp']
        tx.txid = data['txid']
        return tx
        
    def is_coinbase(self):
        """判断是否为Coinbase交易（挖矿奖励）"""
        return self.sender == "COINBASE"
