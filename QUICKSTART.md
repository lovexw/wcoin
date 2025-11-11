# 🚀 WCOIN 快速开始指南

## 1️⃣ 单节点快速体验（5分钟）

### 安装并启动

```bash
# 使用启动脚本（推荐）
./start.sh

# 或手动启动
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### 查看Dashboard

打开浏览器访问：**http://localhost:5000**

你会看到：
- ⛓️ 区块链实时状态
- 💰 挖矿进度和奖励
- 🌐 网络连接信息
- 📦 最新区块列表

### 停止节点

按 `Ctrl+C` 停止节点

---

## 2️⃣ 多节点P2P网络（10分钟）

### 启动3节点网络

```bash
./start_network.sh
```

这会启动：
- **节点1**（种子节点）: 端口9333, Dashboard http://localhost:5000
- **节点2**: 端口9334, Dashboard http://localhost:5001
- **节点3**: 端口9335, Dashboard http://localhost:5002

### 观察区块同步

1. 打开3个浏览器标签，分别访问3个Dashboard
2. 观察节点1挖矿产生新区块
3. 看到其他节点实时同步区块
4. 查看"网络状态"中的"连接节点数"

### 停止网络

```bash
./stop_network.sh
```

---

## 3️⃣ 手动配置多节点

### 终端1 - 种子节点
```bash
python main.py --port 9333 --dashboard-port 5000
```

### 终端2 - 节点2
```bash
python main.py --port 9334 --dashboard-port 5001 --peers localhost:9333
```

### 终端3 - 节点3（不挖矿，仅同步）
```bash
python main.py --port 9335 --dashboard-port 5002 --peers localhost:9333 --no-mining
```

---

## 4️⃣ 命令行参数说明

```bash
python main.py [选项]

--port PORT              # P2P节点端口（默认9333）
--dashboard-port PORT    # Web界面端口（默认5000）
--no-mining              # 不启动挖矿
--peers PEER [PEER ...]  # 连接的种子节点
```

### 示例

```bash
# 端口10000，连接到2个种子节点
python main.py --port 10000 --peers localhost:9333 localhost:9334

# 只同步不挖矿
python main.py --no-mining

# 自定义Dashboard端口
python main.py --dashboard-port 8080
```

---

## 5️⃣ 数据存储位置

所有数据保存在 `data/` 目录：

```
data/
├── blockchain.json  # 区块链数据
├── wallet.json      # 钱包私钥（请妥善保管！）
└── peers.json       # 已知节点列表
```

### 备份钱包

```bash
cp data/wallet.json wallet_backup.json
```

### 重置区块链

```bash
rm -rf data/
```

重启节点会创建新的创世区块。

---

## 6️⃣ 测试场景

### 场景1：观察难度调整

1. 启动单节点持续挖矿
2. 等待2016个区块
3. 观察难度自动调整

### 场景2：测试区块同步

1. 启动节点A，挖10个区块
2. 停止节点A
3. 启动节点B（新节点）
4. 重启节点A，添加B为peer
5. 观察B同步A的区块链

### 场景3：观察减半机制

1. 修改 `config.py` 中的 `HALVING_INTERVAL = 10`（测试用）
2. 启动节点挖矿
3. 每10个区块奖励减半

```python
# config.py
HALVING_INTERVAL = 10  # 改为10方便测试
```

---

## 7️⃣ 常见问题

### Q: 端口被占用怎么办？
```bash
# 使用其他端口
python main.py --port 9999 --dashboard-port 5555
```

### Q: 挖矿太慢？
```bash
# 降低难度（在config.py中）
GENESIS_DIFFICULTY = 2  # 改为2或3
```

### Q: 如何查看日志？
```bash
# 如果使用start_network.sh启动
tail -f logs/node1.log
```

### Q: 忘记钱包地址？
查看Dashboard上的"钱包地址"，或：
```bash
cat data/wallet.json | grep address
```

### Q: 如何在不同电脑间组网？
```bash
# 电脑A（192.168.1.100）
python main.py --port 9333

# 电脑B
python main.py --port 9333 --peers 192.168.1.100:9333
```

---

## 8️⃣ Dashboard功能说明

### 区块链状态
- **区块高度**: 当前区块总数
- **当前难度**: 挖矿难度（前导零个数）
- **总交易数**: 所有区块的交易总和
- **网络算力**: 估算的哈希算力

### 经济模型
- **流通供应量**: 已挖出的WCOIN总数
- **当前区块奖励**: 下一个区块的奖励
- **已减半次数**: 发生过几次减半
- **距离下次减半**: 还需多少区块

### 挖矿状态
- **挖矿状态**: 是否正在挖矿
- **已挖区块**: 本节点挖出的区块数
- **总奖励**: 本节点获得的总奖励
- **钱包余额**: 当前钱包余额

### 网络状态
- **节点端口**: P2P通信端口
- **连接节点数**: 已连接的对等节点
- **运行时间**: 节点运行时长
- **对等节点**: 已连接节点列表

---

## 9️⃣ 性能优化建议

### 加快出块速度（测试用）
```python
# config.py
BLOCK_TIME = 60  # 改为60秒
GENESIS_DIFFICULTY = 3  # 降低难度
```

### 减少内存使用
```python
# blockchain.py - mine_pending_transactions()
transactions = [coinbase_tx] + self.pending_transactions[:5]  # 减少每块交易数
```

### 定期清理日志
```bash
# 限制日志大小
python main.py > >(head -n 10000 > output.log) 2>&1
```

---

## 🎯 下一步

- 📖 阅读完整 [README.md](README.md)
- 🔍 研究源代码了解实现细节
- 🛠️ 修改 `config.py` 调整参数
- 🌐 在多台电脑间搭建真正的P2P网络
- 📊 扩展Dashboard添加更多统计信息

---

**Happy Mining! ⛏️💎**
