#!/usr/bin/env python3
"""
WCOIN - Decentralized Mining System
主程序入口
"""

import os
import sys
import time
import threading
import argparse
from pathlib import Path

from blockchain import Blockchain, Wallet
from mining import Miner
from network import P2PNode
from dashboard.app import Dashboard
import config


def print_banner():
    """打印启动横幅"""
    banner = """
    ╔══════════════════════════════════════════╗
    ║                                          ║
    ║        💎 WCOIN Mining System 💎         ║
    ║                                          ║
    ║     Decentralized | Secure | Fair       ║
    ║                                          ║
    ╚══════════════════════════════════════════╝
    
    Total Supply: 15,000,000 WCN
    Halving: Every year (52,560 blocks)
    Block Time: ~10 minutes
    Initial Reward: 143 WCN
    
    """
    print(banner)


def setup_data_dir():
    """设置数据目录"""
    Path(config.DATA_DIR).mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description='WCOIN Mining System')
    parser.add_argument('--port', type=int, default=config.DEFAULT_PORT, help='P2P node port')
    parser.add_argument('--dashboard-port', type=int, default=config.DASHBOARD_PORT, help='Dashboard port')
    parser.add_argument('--no-mining', action='store_true', help='Start without mining')
    parser.add_argument('--peers', nargs='+', help='Seed peer addresses (e.g., localhost:9334)')
    args = parser.parse_args()
    
    print_banner()
    setup_data_dir()
    
    print("🚀 Initializing WCOIN node...")
    
    blockchain = Blockchain()
    blockchain_file = os.path.join(config.DATA_DIR, config.BLOCKCHAIN_FILE)
    
    if blockchain.load_from_file(blockchain_file):
        print(f"✅ Loaded blockchain from disk (Height: {len(blockchain.chain)})")
    else:
        print("📦 Creating genesis block...")
        blockchain.create_genesis_block()
        blockchain.save_to_file(blockchain_file)
        print(f"✅ Genesis block created! Hash: {blockchain.get_latest_block().hash[:16]}...")
    
    wallet = Wallet()
    wallet_file = os.path.join(config.DATA_DIR, config.WALLET_FILE)
    
    if wallet.load_from_file(wallet_file):
        print(f"✅ Loaded wallet from disk")
    else:
        print("🔑 Generating new wallet...")
        address = wallet.generate_keypair()
        wallet.save_to_file(wallet_file)
        print(f"✅ Wallet created!")
    
    print(f"💼 Wallet Address: {wallet.address}")
    print(f"💰 Balance: {blockchain.get_balance(wallet.address):.2f} {config.COIN_SYMBOL}")
    
    print(f"\n🌐 Starting P2P node on port {args.port}...")
    p2p_node = P2PNode(blockchain, port=args.port)
    p2p_node.start()
    
    if args.peers:
        print(f"👥 Connecting to seed peers...")
        for peer in args.peers:
            p2p_node.add_peer(peer)
        
        print("🔄 Syncing blockchain...")
        if p2p_node.sync_blockchain():
            blockchain.save_to_file(blockchain_file)
    
    miner = Miner(blockchain, wallet, p2p_node)
    
    if not args.no_mining:
        print("\n⛏️  Starting miner...")
        miner.start_mining()
    else:
        print("\n⏸️  Mining disabled (use --no-mining to start without mining)")
    
    def save_periodically():
        """定期保存区块链数据"""
        while True:
            time.sleep(60)
            try:
                blockchain.save_to_file(blockchain_file)
                wallet.save_to_file(wallet_file)
            except Exception as e:
                print(f"⚠️  Error saving data: {e}")
    
    save_thread = threading.Thread(target=save_periodically, daemon=True)
    save_thread.start()
    
    print(f"\n🖥️  Starting dashboard on port {args.dashboard_port}...")
    print(f"📊 Dashboard URL: http://localhost:{args.dashboard_port}")
    print("\n✨ WCOIN node is running! Press Ctrl+C to stop.\n")
    
    try:
        dashboard = Dashboard(blockchain, miner, p2p_node)
        dashboard.run(host=config.DASHBOARD_HOST, port=args.dashboard_port)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down WCOIN node...")
        miner.stop_mining()
        p2p_node.stop()
        blockchain.save_to_file(blockchain_file)
        wallet.save_to_file(wallet_file)
        print("✅ Goodbye!")
        sys.exit(0)


if __name__ == '__main__':
    main()
