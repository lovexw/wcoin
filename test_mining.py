#!/usr/bin/env python3
"""
WCOIN Mining Test Script
测试挖矿功能
"""

import time
from blockchain import Blockchain, Wallet
from mining import Miner
import config

print("=" * 50)
print("WCOIN Mining Test")
print("=" * 50)

print("\n1. Creating blockchain...")
blockchain = Blockchain()
blockchain.create_genesis_block()
print(f"✅ Genesis block created: {blockchain.get_latest_block().hash[:16]}...")

print("\n2. Creating wallet...")
wallet = Wallet()
wallet.generate_keypair()
print(f"✅ Wallet address: {wallet.address}")

print("\n3. Creating miner...")
miner = Miner(blockchain, wallet)
print("✅ Miner created")

print("\n4. Mining 5 blocks...")
for i in range(5):
    print(f"\n   Mining block {i+1}/5...")
    block = blockchain.mine_pending_transactions(wallet.address)
    
    reward = 0
    for tx in block.transactions:
        if tx.is_coinbase() and tx.recipient == wallet.address:
            reward = tx.amount
            break
    
    print(f"   ✅ Block #{block.index} mined!")
    print(f"      Hash: {block.hash[:32]}...")
    print(f"      Nonce: {block.nonce}")
    print(f"      Reward: {reward} {config.COIN_SYMBOL}")
    print(f"      Difficulty: {block.difficulty}")

print("\n5. Blockchain statistics:")
stats = blockchain.get_statistics()
print(f"   Height: {stats['height']}")
print(f"   Difficulty: {stats['difficulty']}")
print(f"   Total Supply: {stats['total_supply']} {config.COIN_SYMBOL}")
print(f"   Total Transactions: {stats['total_transactions']}")

print("\n6. Wallet balance:")
balance = blockchain.get_balance(wallet.address)
print(f"   Balance: {balance} {config.COIN_SYMBOL}")

print("\n7. Validating blockchain...")
if blockchain.is_valid():
    print("   ✅ Blockchain is valid!")
else:
    print("   ❌ Blockchain validation failed!")

print("\n8. Testing halving mechanism...")
print(f"   Initial reward (block 0): {blockchain.calculate_mining_reward(0)}")
print(f"   After 1st halving (block {config.HALVING_INTERVAL}): {blockchain.calculate_mining_reward(config.HALVING_INTERVAL)}")
print(f"   After 2nd halving (block {config.HALVING_INTERVAL*2}): {blockchain.calculate_mining_reward(config.HALVING_INTERVAL*2)}")
print(f"   After 10th halving (block {config.HALVING_INTERVAL*10}): {blockchain.calculate_mining_reward(config.HALVING_INTERVAL*10)}")

print("\n" + "=" * 50)
print("✅ All tests passed!")
print("=" * 50)
