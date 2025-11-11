"""
WCOIN P2P Node
P2P网络节点
"""

import socket
import threading
import json
import time
import requests
from flask import Flask, request, jsonify
import config


class P2PNode:
    """P2P网络节点"""
    
    def __init__(self, blockchain, port=None):
        self.blockchain = blockchain
        self.port = port or config.DEFAULT_PORT
        self.peers = set()
        self.app = Flask(__name__)
        self.server_thread = None
        self.is_running = False
        
        self._setup_routes()
        
    def _setup_routes(self):
        """设置API路由"""
        
        @self.app.route('/ping', methods=['GET'])
        def ping():
            return jsonify({'status': 'ok', 'node': f'localhost:{self.port}'})
            
        @self.app.route('/blockchain', methods=['GET'])
        def get_blockchain():
            return jsonify({
                'chain': [block.to_dict() for block in self.blockchain.chain],
                'length': len(self.blockchain.chain)
            })
            
        @self.app.route('/block', methods=['POST'])
        def receive_block():
            block_data = request.json
            if self._validate_and_add_block(block_data):
                return jsonify({'status': 'accepted'})
            return jsonify({'status': 'rejected'}), 400
            
        @self.app.route('/peers', methods=['GET'])
        def get_peers():
            return jsonify({'peers': list(self.peers)})
            
        @self.app.route('/peers/add', methods=['POST'])
        def add_peer():
            peer = request.json.get('peer')
            if peer and peer not in self.peers:
                self.peers.add(peer)
                return jsonify({'status': 'added'})
            return jsonify({'status': 'already_exists'})
            
        @self.app.route('/stats', methods=['GET'])
        def get_stats():
            return jsonify(self.blockchain.get_statistics())
            
    def _validate_and_add_block(self, block_data):
        """验证并添加接收到的区块"""
        try:
            from blockchain.block import Block
            block = Block.from_dict(block_data)
            
            if not block.is_valid():
                return False
                
            latest_block = self.blockchain.get_latest_block()
            if block.index != latest_block.index + 1:
                return False
                
            if block.previous_hash != latest_block.hash:
                return False
                
            self.blockchain.chain.append(block)
            print(f"📥 Received and accepted block #{block.index} from network")
            return True
            
        except Exception as e:
            print(f"❌ Error validating block: {e}")
            return False
            
    def start(self):
        """启动P2P节点"""
        if self.is_running:
            return
            
        self.is_running = True
        self.server_thread = threading.Thread(
            target=lambda: self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False),
            daemon=True
        )
        self.server_thread.start()
        print(f"🌐 P2P Node started on port {self.port}")
        
        time.sleep(1)
        
    def stop(self):
        """停止P2P节点"""
        self.is_running = False
        print("🛑 P2P Node stopped")
        
    def add_peer(self, peer_address):
        """添加对等节点"""
        if peer_address not in self.peers and peer_address != f"localhost:{self.port}":
            self.peers.add(peer_address)
            print(f"👥 Added peer: {peer_address}")
            
            try:
                response = requests.post(
                    f"http://{peer_address}/peers/add",
                    json={'peer': f"localhost:{self.port}"},
                    timeout=3
                )
            except:
                pass
                
    def broadcast_block(self, block):
        """广播新区块到所有对等节点"""
        block_data = block.to_dict()
        
        for peer in list(self.peers):
            try:
                response = requests.post(
                    f"http://{peer}/block",
                    json=block_data,
                    timeout=5
                )
                if response.status_code == 200:
                    print(f"📤 Broadcasted block #{block.index} to {peer}")
            except Exception as e:
                print(f"⚠️  Failed to broadcast to {peer}: {e}")
                
    def sync_blockchain(self):
        """从对等节点同步区块链"""
        longest_chain = None
        max_length = len(self.blockchain.chain)
        
        for peer in list(self.peers):
            try:
                response = requests.get(f"http://{peer}/blockchain", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    length = data['length']
                    
                    if length > max_length:
                        from blockchain.block import Block
                        chain = [Block.from_dict(block_data) for block_data in data['chain']]
                        
                        temp_blockchain = self.blockchain.__class__()
                        temp_blockchain.chain = chain
                        temp_blockchain.difficulty = chain[-1].difficulty if chain else config.GENESIS_DIFFICULTY
                        
                        if temp_blockchain.is_valid():
                            longest_chain = chain
                            max_length = length
                            
            except Exception as e:
                print(f"⚠️  Sync error with {peer}: {e}")
                
        if longest_chain:
            self.blockchain.chain = longest_chain
            print(f"🔄 Blockchain synced! New height: {len(self.blockchain.chain)}")
            return True
            
        return False
        
    def discover_peers(self, seed_nodes):
        """发现对等节点"""
        for seed in seed_nodes:
            try:
                response = requests.get(f"http://{seed}/peers", timeout=3)
                if response.status_code == 200:
                    peers = response.json().get('peers', [])
                    for peer in peers:
                        self.add_peer(peer)
            except:
                pass
