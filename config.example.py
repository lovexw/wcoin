"""
WCOIN Configuration Example
复制此文件为config.py并根据需要修改参数
"""

# 币种信息
COIN_NAME = "WCOIN"
COIN_SYMBOL = "WCN"

# 经济模型参数
TOTAL_SUPPLY = 15_000_000  # 总量1500万枚
INITIAL_REWARD = 143  # 初始区块奖励
HALVING_INTERVAL = 52560  # 减半间隔（区块数）- 约1年（假设10分钟/块）
MAX_HALVINGS = 10  # 最大减半次数（10年后停止产出）

# 区块链参数
BLOCK_TIME = 600  # 目标出块时间（秒）- 10分钟
DIFFICULTY_ADJUSTMENT_INTERVAL = 2016  # 难度调整间隔（区块数）- 约2周
GENESIS_DIFFICULTY = 4  # 创世区块难度（前导零个数）- 建议3-5
MIN_DIFFICULTY = 1  # 最小难度
MAX_DIFFICULTY = 30  # 最大难度

# P2P网络参数
DEFAULT_PORT = 9333
MAX_PEERS = 50
PEER_DISCOVERY_INTERVAL = 60  # 秒
BLOCK_SYNC_INTERVAL = 10  # 秒

# 钱包参数
ADDRESS_VERSION = b'\x00'  # 地址版本前缀

# Dashboard参数
DASHBOARD_PORT = 5000
DASHBOARD_HOST = '0.0.0.0'

# 数据存储
DATA_DIR = './data'
BLOCKCHAIN_FILE = 'blockchain.json'
WALLET_FILE = 'wallet.json'
PEERS_FILE = 'peers.json'

# ==========================================
# 测试环境建议配置（快速出块）
# ==========================================
# BLOCK_TIME = 30  # 30秒出块
# GENESIS_DIFFICULTY = 2  # 降低难度
# HALVING_INTERVAL = 100  # 100块减半（方便测试）
# DIFFICULTY_ADJUSTMENT_INTERVAL = 50  # 50块调整

# ==========================================
# 生产环境建议配置（安全稳定）
# ==========================================
# BLOCK_TIME = 600  # 10分钟出块
# GENESIS_DIFFICULTY = 5  # 提高难度
# MAX_PEERS = 100  # 增加节点连接数
