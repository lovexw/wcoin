"""
WCOIN Blockchain
区块链主类
"""

import json
import os
import time
from .block import Block
from .transaction import Transaction
import config


class Blockchain:
    """区块链类"""
    
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = config.GENESIS_DIFFICULTY
        
    def create_genesis_block(self):
        """创建创世区块"""
        genesis_tx = Transaction("GENESIS", "GENESIS", 0)
        genesis_block = Block(0, [genesis_tx], "0", self.difficulty)
        genesis_block.mine_block()
        self.chain.append(genesis_block)
        return genesis_block
        
    def get_latest_block(self):
        """获取最新区块"""
        return self.chain[-1] if self.chain else None
        
    def add_transaction(self, transaction):
        """添加待处理交易"""
        self.pending_transactions.append(transaction)
        
    def mine_pending_transactions(self, miner_address):
        """挖矿 - 打包待处理交易"""
        if not self.chain:
            self.create_genesis_block()
            
        latest_block = self.get_latest_block()
        new_index = latest_block.index + 1
        
        reward = self.calculate_mining_reward(new_index)
        if reward > 0:
            coinbase_tx = Transaction("COINBASE", miner_address, reward)
            transactions = [coinbase_tx] + self.pending_transactions[:10]
        else:
            transactions = self.pending_transactions[:10]
            
        self.adjust_difficulty()
        
        new_block = Block(
            new_index,
            transactions,
            latest_block.hash,
            self.difficulty
        )
        
        print(f"⛏️  Mining block #{new_index} with difficulty {self.difficulty}...")
        start_time = time.time()
        new_block.mine_block()
        elapsed = time.time() - start_time
        
        print(f"✅ Block mined! Hash: {new_block.hash[:16]}... (Time: {elapsed:.2f}s)")
        
        self.chain.append(new_block)
        self.pending_transactions = self.pending_transactions[10:]
        
        return new_block
        
    def calculate_mining_reward(self, block_height):
        """计算挖矿奖励（带减半机制）"""
        halvings = block_height // config.HALVING_INTERVAL
        
        if halvings >= config.MAX_HALVINGS:
            return 0
            
        reward = config.INITIAL_REWARD / (2 ** halvings)
        return reward
        
    def adjust_difficulty(self):
        """调整挖矿难度"""
        if len(self.chain) < config.DIFFICULTY_ADJUSTMENT_INTERVAL:
            return
            
        if len(self.chain) % config.DIFFICULTY_ADJUSTMENT_INTERVAL != 0:
            return
            
        last_adjustment_block = self.chain[-config.DIFFICULTY_ADJUSTMENT_INTERVAL]
        latest_block = self.get_latest_block()
        
        time_taken = latest_block.timestamp - last_adjustment_block.timestamp
        expected_time = config.DIFFICULTY_ADJUSTMENT_INTERVAL * config.BLOCK_TIME
        
        if time_taken < expected_time / 2:
            self.difficulty = min(self.difficulty + 1, config.MAX_DIFFICULTY)
            print(f"📈 Difficulty increased to {self.difficulty}")
        elif time_taken > expected_time * 2:
            self.difficulty = max(self.difficulty - 1, config.MIN_DIFFICULTY)
            print(f"📉 Difficulty decreased to {self.difficulty}")
            
    def is_valid(self):
        """验证区块链有效性"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if not current_block.is_valid():
                return False
                
            if current_block.previous_hash != previous_block.hash:
                return False
                
        return True
        
    def get_balance(self, address):
        """获取地址余额"""
        balance = 0
        
        for block in self.chain:
            for tx in block.transactions:
                if tx.recipient == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= tx.amount
                    
        return balance
        
    def get_total_supply(self):
        """获取当前总供应量"""
        total = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.is_coinbase():
                    total += tx.amount
        return total
        
    def save_to_file(self, filepath):
        """保存区块链到文件"""
        data = {
            'chain': [block.to_dict() for block in self.chain],
            'pending_transactions': [tx.to_dict() for tx in self.pending_transactions],
            'difficulty': self.difficulty
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load_from_file(self, filepath):
        """从文件加载区块链"""
        if not os.path.exists(filepath):
            return False
            
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        self.chain = [Block.from_dict(block_data) for block_data in data['chain']]
        self.pending_transactions = [Transaction.from_dict(tx_data) for tx_data in data['pending_transactions']]
        self.difficulty = data['difficulty']
        
        return True
        
    def get_statistics(self):
        """获取区块链统计信息"""
        if not self.chain:
            return {
                'height': 0,
                'difficulty': self.difficulty,
                'total_supply': 0,
                'total_transactions': 0,
                'latest_block_time': None,
                'network_hashrate': 0
            }
            
        latest_block = self.get_latest_block()
        total_txs = sum(len(block.transactions) for block in self.chain)
        
        if len(self.chain) >= 2:
            recent_blocks = self.chain[-10:]
            time_diff = recent_blocks[-1].timestamp - recent_blocks[0].timestamp
            avg_block_time = time_diff / (len(recent_blocks) - 1) if len(recent_blocks) > 1 else config.BLOCK_TIME
            network_hashrate = (2 ** self.difficulty) / avg_block_time if avg_block_time > 0 else 0
        else:
            network_hashrate = 0
            
        return {
            'height': len(self.chain),
            'difficulty': self.difficulty,
            'total_supply': self.get_total_supply(),
            'total_transactions': total_txs,
            'latest_block_time': latest_block.timestamp,
            'latest_block_hash': latest_block.hash,
            'network_hashrate': network_hashrate
        }
