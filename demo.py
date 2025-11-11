#!/usr/bin/env python3
"""
WCOIN完整功能演示
展示区块链、挖矿、交易、P2P等所有功能
"""

import time
import sys
from blockchain import Blockchain, Wallet, Transaction
from mining import Miner
import config

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_subsection(title):
    print(f"\n--- {title} ---")

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║            💎 WCOIN功能演示 💎                       ║
    ║                                                      ║
    ║        完整展示区块链和加密货币的核心功能              ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    print_section("1️⃣  初始化区块链")
    blockchain = Blockchain()
    blockchain.create_genesis_block()
    genesis = blockchain.get_latest_block()
    print(f"✅ 创世区块已创建")
    print(f"   区块高度: {genesis.index}")
    print(f"   区块哈希: {genesis.hash[:40]}...")
    print(f"   难度等级: {genesis.difficulty}")
    print(f"   时间戳: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(genesis.timestamp))}")
    
    print_section("2️⃣  创建钱包和地址")
    print_subsection("创建矿工钱包")
    miner_wallet = Wallet()
    miner_address = miner_wallet.generate_keypair()
    print(f"✅ 矿工钱包已创建")
    print(f"   地址: {miner_address}")
    print(f"   余额: {blockchain.get_balance(miner_address)} {config.COIN_SYMBOL}")
    
    print_subsection("创建用户钱包")
    user1_wallet = Wallet()
    user1_address = user1_wallet.generate_keypair()
    print(f"✅ 用户1钱包已创建")
    print(f"   地址: {user1_address}")
    
    user2_wallet = Wallet()
    user2_address = user2_wallet.generate_keypair()
    print(f"✅ 用户2钱包已创建")
    print(f"   地址: {user2_address}")
    
    print_section("3️⃣  挖矿获取WCOIN")
    miner = Miner(blockchain, miner_wallet)
    
    print("\n正在挖掘前3个区块...")
    for i in range(3):
        print(f"\n🔨 挖掘第 {i+1} 个区块...")
        start_time = time.time()
        block = blockchain.mine_pending_transactions(miner_address)
        elapsed = time.time() - start_time
        
        reward = 0
        for tx in block.transactions:
            if tx.is_coinbase():
                reward = tx.amount
                break
        
        print(f"   ✅ 区块 #{block.index} 已挖出")
        print(f"   ⏱️  用时: {elapsed:.2f}秒")
        print(f"   🎁 奖励: {reward} {config.COIN_SYMBOL}")
        print(f"   🔢 Nonce: {block.nonce}")
        print(f"   📦 哈希: {block.hash[:40]}...")
    
    current_balance = blockchain.get_balance(miner_address)
    print(f"\n💰 矿工当前余额: {current_balance} {config.COIN_SYMBOL}")
    
    print_section("4️⃣  创建和验证交易")
    print_subsection("矿工向用户1转账")
    tx1 = Transaction(miner_address, user1_address, 50)
    blockchain.add_transaction(tx1)
    print(f"✅ 交易创建成功")
    print(f"   从: {miner_address}")
    print(f"   到: {user1_address}")
    print(f"   金额: 50 {config.COIN_SYMBOL}")
    print(f"   交易ID: {tx1.txid[:40]}...")
    
    print_subsection("矿工向用户2转账")
    tx2 = Transaction(miner_address, user2_address, 30)
    blockchain.add_transaction(tx2)
    print(f"✅ 交易创建成功")
    print(f"   从: {miner_address}")
    print(f"   到: {user2_address}")
    print(f"   金额: 30 {config.COIN_SYMBOL}")
    
    print_subsection("打包交易到区块")
    block = blockchain.mine_pending_transactions(miner_address)
    print(f"✅ 区块 #{block.index} 已挖出，包含 {len(block.transactions)} 笔交易")
    
    print_section("5️⃣  查询余额")
    balances = {
        "矿工": blockchain.get_balance(miner_address),
        "用户1": blockchain.get_balance(user1_address),
        "用户2": blockchain.get_balance(user2_address)
    }
    
    for name, balance in balances.items():
        print(f"   {name}: {balance} {config.COIN_SYMBOL}")
    
    total_supply = blockchain.get_total_supply()
    print(f"\n📊 当前总供应量: {total_supply} {config.COIN_SYMBOL}")
    print(f"   最大供应量: {config.TOTAL_SUPPLY:,} {config.COIN_SYMBOL}")
    print(f"   供应进度: {(total_supply / config.TOTAL_SUPPLY * 100):.2f}%")
    
    print_section("6️⃣  区块链验证")
    is_valid = blockchain.is_valid()
    if is_valid:
        print("✅ 区块链验证通过！")
        print("   所有区块哈希正确")
        print("   所有区块链接有效")
        print("   工作量证明验证成功")
    else:
        print("❌ 区块链验证失败！")
    
    print_section("7️⃣  区块链统计")
    stats = blockchain.get_statistics()
    print(f"   区块高度: {stats['height']}")
    print(f"   当前难度: {stats['difficulty']}")
    print(f"   总交易数: {stats['total_transactions']}")
    print(f"   总供应量: {stats['total_supply']} {config.COIN_SYMBOL}")
    print(f"   网络算力: {stats['network_hashrate']:.2f} H/s")
    
    print_section("8️⃣  减半机制演示")
    print("\n未来10年的区块奖励变化：")
    print(f"{'年份':<8} {'区块高度':<12} {'区块奖励':<15} {'年产量':<20}")
    print("-" * 60)
    
    for year in range(11):
        block_height = year * config.HALVING_INTERVAL
        reward = blockchain.calculate_mining_reward(block_height)
        yearly_output = reward * config.HALVING_INTERVAL
        print(f"{year+1:<8} {block_height:<12} {reward:<15.2f} {yearly_output:<20,.2f}")
    
    print_section("9️⃣  区块详情")
    print("\n最近的区块：")
    for block in blockchain.chain[-5:]:
        print(f"\n   区块 #{block.index}")
        print(f"   哈希: {block.hash[:40]}...")
        print(f"   前块: {block.previous_hash[:40]}...")
        print(f"   交易: {len(block.transactions)} 笔")
        print(f"   难度: {block.difficulty}")
        print(f"   Nonce: {block.nonce}")
        print(f"   时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
    
    print_section("🔟  经济模型总结")
    print(f"""
    币种名称: {config.COIN_NAME} ({config.COIN_SYMBOL})
    总供应量: {config.TOTAL_SUPPLY:,} {config.COIN_SYMBOL}
    初始奖励: {config.INITIAL_REWARD} {config.COIN_SYMBOL}/块
    减半周期: {config.HALVING_INTERVAL:,} 块 (~1年)
    最大减半: {config.MAX_HALVINGS} 次 (10年)
    区块时间: {config.BLOCK_TIME} 秒 (~10分钟)
    难度调整: 每 {config.DIFFICULTY_ADJUSTMENT_INTERVAL} 块
    
    当前状态:
    - 已产出: {total_supply:.2f} {config.COIN_SYMBOL}
    - 剩余: {config.TOTAL_SUPPLY - total_supply:.2f} {config.COIN_SYMBOL}
    - 进度: {(total_supply / config.TOTAL_SUPPLY * 100):.4f}%
    """)
    
    print("\n" + "=" * 60)
    print("  ✅ WCOIN演示完成！")
    print("=" * 60)
    print("""
    下一步：
    1. 运行 'python main.py' 启动完整节点
    2. 访问 http://localhost:5000 查看Dashboard
    3. 运行 './start_network.sh' 启动多节点网络
    4. 阅读 README.md 了解更多功能
    """)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 演示已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
