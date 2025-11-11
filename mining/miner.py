"""
WCOIN Miner
挖矿器模块
"""

import time
import threading
import config


class Miner:
    """挖矿器类"""
    
    def __init__(self, blockchain, wallet, p2p_node=None):
        self.blockchain = blockchain
        self.wallet = wallet
        self.p2p_node = p2p_node
        self.is_mining = False
        self.mining_thread = None
        self.blocks_mined = 0
        self.total_reward = 0
        
    def start_mining(self):
        """开始挖矿"""
        if self.is_mining:
            print("⚠️  Already mining...")
            return
            
        if not self.wallet.address:
            print("❌ No wallet address available")
            return
            
        self.is_mining = True
        self.mining_thread = threading.Thread(target=self._mining_loop, daemon=True)
        self.mining_thread.start()
        print(f"⛏️  Mining started! Address: {self.wallet.address}")
        
    def stop_mining(self):
        """停止挖矿"""
        self.is_mining = False
        if self.mining_thread:
            self.mining_thread.join(timeout=5)
        print("🛑 Mining stopped")
        
    def _mining_loop(self):
        """挖矿循环"""
        while self.is_mining:
            try:
                block = self.blockchain.mine_pending_transactions(self.wallet.address)
                
                reward = 0
                for tx in block.transactions:
                    if tx.is_coinbase() and tx.recipient == self.wallet.address:
                        reward = tx.amount
                        break
                
                self.blocks_mined += 1
                self.total_reward += reward
                
                print(f"💰 Block #{block.index} mined! Reward: {reward:.2f} {config.COIN_SYMBOL}")
                print(f"   Total mined: {self.blocks_mined} blocks, {self.total_reward:.2f} {config.COIN_SYMBOL}")
                
                if self.p2p_node:
                    self.p2p_node.broadcast_block(block)
                    
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Mining error: {e}")
                time.sleep(5)
                
    def get_statistics(self):
        """获取挖矿统计"""
        return {
            'is_mining': self.is_mining,
            'blocks_mined': self.blocks_mined,
            'total_reward': self.total_reward,
            'wallet_balance': self.blockchain.get_balance(self.wallet.address) if self.wallet.address else 0
        }
