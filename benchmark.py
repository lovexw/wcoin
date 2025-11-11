#!/usr/bin/env python3
"""
WCOIN性能基准测试
测试挖矿速度、交易处理、区块验证等性能指标
"""

import time
import statistics
from blockchain import Blockchain, Wallet, Transaction
from mining import Miner
import config

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_mining_performance():
    """测试挖矿性能"""
    print_header("⛏️  挖矿性能测试")
    
    blockchain = Blockchain()
    blockchain.create_genesis_block()
    wallet = Wallet()
    wallet.generate_keypair()
    
    mining_times = []
    nonces = []
    
    print(f"\n正在挖掘 10 个区块（难度 {config.GENESIS_DIFFICULTY}）...\n")
    
    for i in range(10):
        start_time = time.time()
        block = blockchain.mine_pending_transactions(wallet.address)
        elapsed = time.time() - start_time
        
        mining_times.append(elapsed)
        nonces.append(block.nonce)
        
        print(f"区块 #{block.index:2d}: {elapsed:6.2f}s | Nonce: {block.nonce:8d} | "
              f"速率: {block.nonce/elapsed:,.0f} H/s")
    
    avg_time = statistics.mean(mining_times)
    med_time = statistics.median(mining_times)
    min_time = min(mining_times)
    max_time = max(mining_times)
    avg_nonce = statistics.mean(nonces)
    avg_hashrate = avg_nonce / avg_time
    
    print(f"\n📊 统计结果:")
    print(f"   平均时间: {avg_time:.2f}s")
    print(f"   中位时间: {med_time:.2f}s")
    print(f"   最快时间: {min_time:.2f}s")
    print(f"   最慢时间: {max_time:.2f}s")
    print(f"   平均Nonce: {avg_nonce:,.0f}")
    print(f"   平均算力: {avg_hashrate:,.0f} H/s")
    print(f"   总用时: {sum(mining_times):.2f}s")
    
    return blockchain

def test_transaction_throughput(blockchain):
    """测试交易处理吞吐量"""
    print_header("💸 交易处理性能测试")
    
    wallets = []
    for i in range(100):
        w = Wallet()
        w.generate_keypair()
        wallets.append(w)
    
    print(f"\n创建了 {len(wallets)} 个钱包")
    
    print("\n正在创建 1000 笔交易...")
    start_time = time.time()
    
    tx_count = 0
    for i in range(1000):
        sender = wallets[i % len(wallets)]
        recipient = wallets[(i + 1) % len(wallets)]
        tx = Transaction(sender.address, recipient.address, 1.0)
        blockchain.add_transaction(tx)
        tx_count += 1
    
    elapsed = time.time() - start_time
    tps = tx_count / elapsed
    
    print(f"\n📊 统计结果:")
    print(f"   交易总数: {tx_count}")
    print(f"   用时: {elapsed:.2f}s")
    print(f"   TPS (每秒交易数): {tps:,.0f}")
    print(f"   平均延迟: {(elapsed/tx_count)*1000:.2f}ms")

def test_block_validation():
    """测试区块验证性能"""
    print_header("✅ 区块验证性能测试")
    
    blockchain = Blockchain()
    blockchain.create_genesis_block()
    wallet = Wallet()
    wallet.generate_keypair()
    
    print("\n正在创建 50 个区块...")
    for i in range(50):
        blockchain.mine_pending_transactions(wallet.address)
        if (i + 1) % 10 == 0:
            print(f"   已创建 {i + 1} 个区块...")
    
    print(f"\n正在验证 {len(blockchain.chain)} 个区块...")
    start_time = time.time()
    is_valid = blockchain.is_valid()
    elapsed = time.time() - start_time
    
    blocks_per_sec = len(blockchain.chain) / elapsed
    
    print(f"\n📊 统计结果:")
    print(f"   区块总数: {len(blockchain.chain)}")
    print(f"   验证结果: {'✅ 通过' if is_valid else '❌ 失败'}")
    print(f"   验证用时: {elapsed:.4f}s")
    print(f"   验证速度: {blocks_per_sec:,.0f} 块/秒")
    print(f"   平均延迟: {(elapsed/len(blockchain.chain))*1000:.2f}ms/块")

def test_wallet_generation():
    """测试钱包生成性能"""
    print_header("🔑 钱包生成性能测试")
    
    print("\n正在生成 100 个钱包...")
    start_time = time.time()
    
    wallets = []
    for i in range(100):
        w = Wallet()
        w.generate_keypair()
        wallets.append(w)
        if (i + 1) % 20 == 0:
            print(f"   已生成 {i + 1} 个钱包...")
    
    elapsed = time.time() - start_time
    wallets_per_sec = len(wallets) / elapsed
    
    print(f"\n📊 统计结果:")
    print(f"   钱包总数: {len(wallets)}")
    print(f"   生成用时: {elapsed:.2f}s")
    print(f"   生成速度: {wallets_per_sec:.2f} 个/秒")
    print(f"   平均延迟: {(elapsed/len(wallets))*1000:.0f}ms/个")

def test_balance_queries(blockchain):
    """测试余额查询性能"""
    print_header("💰 余额查询性能测试")
    
    wallets = []
    for i in range(50):
        w = Wallet()
        w.generate_keypair()
        wallets.append(w)
    
    print("\n正在查询 1000 次余额...")
    start_time = time.time()
    
    for i in range(1000):
        wallet = wallets[i % len(wallets)]
        balance = blockchain.get_balance(wallet.address)
    
    elapsed = time.time() - start_time
    queries_per_sec = 1000 / elapsed
    
    print(f"\n📊 统计结果:")
    print(f"   查询总数: 1000")
    print(f"   用时: {elapsed:.2f}s")
    print(f"   QPS (每秒查询数): {queries_per_sec:,.0f}")
    print(f"   平均延迟: {(elapsed/1000)*1000:.2f}ms")

def test_difficulty_levels():
    """测试不同难度级别"""
    print_header("📊 难度级别对比测试")
    
    difficulties = [2, 3, 4, 5]
    
    print("\n测试不同难度级别的挖矿时间：\n")
    print(f"{'难度':<6} {'平均时间':<12} {'平均Nonce':<15} {'算力估算':<15}")
    print("-" * 60)
    
    for difficulty in difficulties:
        blockchain = Blockchain()
        blockchain.difficulty = difficulty
        blockchain.create_genesis_block()
        
        wallet = Wallet()
        wallet.generate_keypair()
        
        times = []
        nonces = []
        
        for i in range(5):
            original_difficulty = config.GENESIS_DIFFICULTY
            config.GENESIS_DIFFICULTY = difficulty
            blockchain.difficulty = difficulty
            
            start_time = time.time()
            block = blockchain.mine_pending_transactions(wallet.address)
            elapsed = time.time() - start_time
            
            config.GENESIS_DIFFICULTY = original_difficulty
            
            times.append(elapsed)
            nonces.append(block.nonce)
        
        avg_time = statistics.mean(times)
        avg_nonce = statistics.mean(nonces)
        hashrate = avg_nonce / avg_time
        
        print(f"{difficulty:<6} {avg_time:<12.2f}s {avg_nonce:<15.0f} {hashrate:<15,.0f} H/s")

def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║            💎 WCOIN 性能基准测试 💎                      ║
    ║                                                          ║
    ║         评估区块链系统的各项性能指标                      ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print(f"\n系统信息:")
    print(f"   Python版本: {__import__('sys').version.split()[0]}")
    print(f"   配置难度: {config.GENESIS_DIFFICULTY}")
    print(f"   区块时间: {config.BLOCK_TIME}秒")
    
    overall_start = time.time()
    
    blockchain = test_mining_performance()
    
    test_transaction_throughput(blockchain)
    
    test_block_validation()
    
    test_wallet_generation()
    
    test_balance_queries(blockchain)
    
    test_difficulty_levels()
    
    overall_elapsed = time.time() - overall_start
    
    print_header("🏁 测试完成")
    print(f"\n   总用时: {overall_elapsed:.2f}秒")
    print(f"   测试项: 6项")
    print(f"   状态: ✅ 全部完成")
    
    print("\n" + "=" * 70)
    print("  性能测试建议:")
    print("=" * 70)
    print("""
    💡 如果挖矿速度太慢：
       - 降低 GENESIS_DIFFICULTY (建议 2-3)
       - 减少测试区块数量
    
    💡 如果需要更高安全性：
       - 提高 GENESIS_DIFFICULTY (建议 5-6)
       - 增加 DIFFICULTY_ADJUSTMENT_INTERVAL
    
    💡 测试环境建议：
       - BLOCK_TIME = 30 (快速测试)
       - GENESIS_DIFFICULTY = 2 (降低难度)
       - HALVING_INTERVAL = 10 (快速验证减半)
    """)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  测试已中断")
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()
