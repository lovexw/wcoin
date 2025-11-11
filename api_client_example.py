#!/usr/bin/env python3
"""
WCOIN API客户端示例
展示如何通过HTTP API与WCOIN节点交互
"""

import requests
import json
from typing import Optional, Dict, List

class WCoinClient:
    """WCOIN节点API客户端"""
    
    def __init__(self, node_url: str = "http://localhost:9333"):
        """
        初始化客户端
        
        Args:
            node_url: WCOIN节点的URL地址
        """
        self.node_url = node_url.rstrip('/')
        
    def ping(self) -> bool:
        """
        检查节点是否在线
        
        Returns:
            bool: 节点是否响应
        """
        try:
            response = requests.get(f"{self.node_url}/ping", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def get_blockchain(self) -> Optional[Dict]:
        """
        获取完整区块链
        
        Returns:
            dict: 包含区块链数据的字典
        """
        try:
            response = requests.get(f"{self.node_url}/blockchain", timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"获取区块链失败: {e}")
        return None
    
    def get_stats(self) -> Optional[Dict]:
        """
        获取节点统计信息
        
        Returns:
            dict: 统计信息
        """
        try:
            response = requests.get(f"{self.node_url}/stats", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"获取统计信息失败: {e}")
        return None
    
    def get_peers(self) -> List[str]:
        """
        获取对等节点列表
        
        Returns:
            list: 对等节点地址列表
        """
        try:
            response = requests.get(f"{self.node_url}/peers", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('peers', [])
        except Exception as e:
            print(f"获取节点列表失败: {e}")
        return []
    
    def add_peer(self, peer_address: str) -> bool:
        """
        添加对等节点
        
        Args:
            peer_address: 节点地址，如 "localhost:9334"
            
        Returns:
            bool: 是否成功
        """
        try:
            response = requests.post(
                f"{self.node_url}/peers/add",
                json={'peer': peer_address},
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"添加节点失败: {e}")
        return False
    
    def broadcast_block(self, block_data: Dict) -> bool:
        """
        广播新区块
        
        Args:
            block_data: 区块数据字典
            
        Returns:
            bool: 是否成功
        """
        try:
            response = requests.post(
                f"{self.node_url}/block",
                json=block_data,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"广播区块失败: {e}")
        return False


def demo_basic_queries():
    """演示基本查询操作"""
    print("=" * 70)
    print("  示例1: 基本查询操作")
    print("=" * 70)
    
    client = WCoinClient("http://localhost:9333")
    
    print("\n1️⃣  检查节点状态...")
    if client.ping():
        print("   ✅ 节点在线")
    else:
        print("   ❌ 节点离线或无法访问")
        print("   💡 请先运行: python main.py")
        return
    
    print("\n2️⃣  获取节点统计信息...")
    stats = client.get_stats()
    if stats:
        print(f"   区块高度: {stats['height']}")
        print(f"   当前难度: {stats['difficulty']}")
        print(f"   总供应量: {stats['total_supply']} WCN")
        print(f"   网络算力: {stats['network_hashrate']:.2f} H/s")
    
    print("\n3️⃣  获取对等节点...")
    peers = client.get_peers()
    if peers:
        print(f"   连接的节点: {len(peers)}")
        for peer in peers:
            print(f"      - {peer}")
    else:
        print("   当前没有连接的节点")


def demo_blockchain_analysis():
    """演示区块链分析"""
    print("\n" + "=" * 70)
    print("  示例2: 区块链数据分析")
    print("=" * 70)
    
    client = WCoinClient("http://localhost:9333")
    
    print("\n正在获取区块链数据...")
    blockchain_data = client.get_blockchain()
    
    if not blockchain_data:
        print("❌ 无法获取区块链数据")
        return
    
    chain = blockchain_data['chain']
    length = blockchain_data['length']
    
    print(f"\n✅ 成功获取 {length} 个区块\n")
    
    print("📊 区块链分析:")
    print(f"   总区块数: {length}")
    
    total_txs = sum(len(block['transactions']) for block in chain)
    print(f"   总交易数: {total_txs}")
    
    if length > 0:
        latest_block = chain[-1]
        print(f"\n📦 最新区块:")
        print(f"   高度: {latest_block['index']}")
        print(f"   哈希: {latest_block['hash'][:40]}...")
        print(f"   难度: {latest_block['difficulty']}")
        print(f"   交易: {len(latest_block['transactions'])} 笔")
        print(f"   Nonce: {latest_block['nonce']}")
    
    if length > 1:
        print(f"\n📈 区块统计:")
        difficulties = [block['difficulty'] for block in chain]
        print(f"   最低难度: {min(difficulties)}")
        print(f"   最高难度: {max(difficulties)}")
        print(f"   当前难度: {difficulties[-1]}")


def demo_multi_node():
    """演示多节点连接"""
    print("\n" + "=" * 70)
    print("  示例3: 多节点网络操作")
    print("=" * 70)
    
    nodes = [
        ("节点1", "http://localhost:9333"),
        ("节点2", "http://localhost:9334"),
        ("节点3", "http://localhost:9335"),
    ]
    
    print("\n正在检查网络中的节点...\n")
    
    online_nodes = []
    for name, url in nodes:
        client = WCoinClient(url)
        if client.ping():
            print(f"✅ {name} ({url}) - 在线")
            online_nodes.append((name, url, client))
        else:
            print(f"❌ {name} ({url}) - 离线")
    
    if len(online_nodes) == 0:
        print("\n⚠️  没有在线的节点")
        print("💡 运行 './start_network.sh' 启动多节点网络")
        return
    
    print(f"\n📊 网络状态: {len(online_nodes)}/{len(nodes)} 节点在线\n")
    
    for name, url, client in online_nodes:
        stats = client.get_stats()
        if stats:
            print(f"{name}:")
            print(f"   区块高度: {stats['height']}")
            print(f"   节点数: {len(client.get_peers())}")


def demo_custom_requests():
    """演示自定义API请求"""
    print("\n" + "=" * 70)
    print("  示例4: 自定义API请求")
    print("=" * 70)
    
    node_url = "http://localhost:9333"
    
    print(f"\n发送自定义请求到 {node_url}")
    
    try:
        print("\n1. GET /ping")
        response = requests.get(f"{node_url}/ping", timeout=3)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.json()}")
        
        print("\n2. GET /stats")
        response = requests.get(f"{node_url}/stats", timeout=3)
        print(f"   状态码: {response.status_code}")
        data = response.json()
        print(f"   响应字段: {list(data.keys())}")
        
        print("\n3. GET /peers")
        response = requests.get(f"{node_url}/peers", timeout=3)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.json()}")
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")


def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║            💎 WCOIN API 客户端示例 💎                    ║
    ║                                                          ║
    ║         展示如何通过HTTP API与节点交互                   ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print("\n📝 注意:")
    print("   1. 请确保至少有一个WCOIN节点正在运行")
    print("   2. 默认节点地址: http://localhost:9333")
    print("   3. 可以运行 'python main.py' 启动节点\n")
    
    input("按Enter键继续...")
    
    demo_basic_queries()
    
    demo_blockchain_analysis()
    
    demo_multi_node()
    
    demo_custom_requests()
    
    print("\n" + "=" * 70)
    print("  ✅ 示例演示完成")
    print("=" * 70)
    print("""
    💡 API端点总结:
    
    节点状态:
      GET  /ping              - 检查节点状态
      GET  /stats             - 获取统计信息
    
    区块链:
      GET  /blockchain        - 获取完整区块链
      POST /block             - 接收新区块
    
    网络:
      GET  /peers             - 获取对等节点
      POST /peers/add         - 添加对等节点
    
    Dashboard API (端口5000):
      GET  /api/stats         - Dashboard统计
      GET  /api/blocks        - 最近区块
      GET  /api/wallet        - 钱包信息
    """)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 示例已退出")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
