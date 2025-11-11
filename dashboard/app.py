"""
WCOIN Dashboard
网络状态展示面板
"""

from flask import Flask, render_template, jsonify
import config
import time


class Dashboard:
    """Dashboard类"""
    
    def __init__(self, blockchain, miner, p2p_node):
        self.blockchain = blockchain
        self.miner = miner
        self.p2p_node = p2p_node
        self.app = Flask(__name__, 
                        template_folder='templates',
                        static_folder='static')
        self.start_time = time.time()
        
        self._setup_routes()
        
    def _setup_routes(self):
        """设置路由"""
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
            
        @self.app.route('/api/stats')
        def get_stats():
            blockchain_stats = self.blockchain.get_statistics()
            miner_stats = self.miner.get_statistics()
            
            current_height = blockchain_stats['height']
            current_reward = self.blockchain.calculate_mining_reward(current_height)
            next_halving = config.HALVING_INTERVAL - (current_height % config.HALVING_INTERVAL)
            halving_count = current_height // config.HALVING_INTERVAL
            
            max_supply = config.TOTAL_SUPPLY
            current_supply = blockchain_stats['total_supply']
            supply_percentage = (current_supply / max_supply * 100) if max_supply > 0 else 0
            
            uptime = time.time() - self.start_time
            
            return jsonify({
                'blockchain': {
                    'height': blockchain_stats['height'],
                    'difficulty': blockchain_stats['difficulty'],
                    'total_supply': round(current_supply, 2),
                    'max_supply': max_supply,
                    'supply_percentage': round(supply_percentage, 2),
                    'total_transactions': blockchain_stats['total_transactions'],
                    'latest_block_hash': blockchain_stats.get('latest_block_hash', 'N/A'),
                    'network_hashrate': round(blockchain_stats['network_hashrate'], 2)
                },
                'mining': {
                    'is_mining': miner_stats['is_mining'],
                    'current_reward': round(current_reward, 2),
                    'blocks_mined': miner_stats['blocks_mined'],
                    'total_reward': round(miner_stats['total_reward'], 2),
                    'wallet_balance': round(miner_stats['wallet_balance'], 2),
                    'next_halving': next_halving,
                    'halving_count': halving_count
                },
                'network': {
                    'peers_count': len(self.p2p_node.peers),
                    'peers': list(self.p2p_node.peers),
                    'port': self.p2p_node.port,
                    'uptime': round(uptime)
                }
            })
            
        @self.app.route('/api/blocks')
        def get_recent_blocks():
            recent_blocks = self.blockchain.chain[-10:]
            blocks_data = []
            
            for block in reversed(recent_blocks):
                blocks_data.append({
                    'index': block.index,
                    'hash': block.hash,
                    'timestamp': block.timestamp,
                    'transactions': len(block.transactions),
                    'difficulty': block.difficulty,
                    'nonce': block.nonce
                })
                
            return jsonify(blocks_data)
            
        @self.app.route('/api/wallet')
        def get_wallet_info():
            return jsonify({
                'address': self.miner.wallet.address or 'No wallet',
                'balance': round(self.blockchain.get_balance(self.miner.wallet.address), 2) if self.miner.wallet.address else 0
            })
            
    def run(self, host=None, port=None):
        """运行Dashboard"""
        host = host or config.DASHBOARD_HOST
        port = port or config.DASHBOARD_PORT
        print(f"🖥️  Dashboard running at http://{host}:{port}")
        self.app.run(host=host, port=port, debug=False)
