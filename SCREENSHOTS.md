# 📸 WCOIN 界面预览

## Dashboard主界面

Dashboard展示了完整的区块链网络状态，包括：

### 区块链状态
- 区块高度
- 当前难度
- 总交易数
- 网络算力
- 最新区块哈希

### 经济模型
- 流通供应量
- 最大供应量
- 当前区块奖励
- 已减半次数
- 距离下次减半
- 进度条显示

### 挖矿状态
- 挖矿状态（活跃/停止）
- 已挖区块数
- 总奖励
- 钱包余额
- 钱包地址

### 网络状态
- 节点端口
- 连接节点数
- 运行时间
- 对等节点列表

### 最近区块
表格显示最新10个区块：
- 区块高度
- 区块哈希
- 时间戳
- 交易数
- 难度
- Nonce值

## 界面特点

✨ **美观的渐变背景**
- 紫色渐变主题
- 现代化卡片设计
- 响应式布局

📊 **实时数据更新**
- 每5秒自动刷新
- 无需手动刷新页面
- 流畅的过渡动画

🎨 **交互效果**
- 卡片悬停效果
- 进度条动画
- 状态徽章
- 颜色编码

## 访问方式

### 单节点
访问: http://localhost:5000

### 多节点网络
- 节点1: http://localhost:5000
- 节点2: http://localhost:5001
- 节点3: http://localhost:5002

## API端点

Dashboard提供RESTful API：

```bash
# 获取统计信息
curl http://localhost:5000/api/stats

# 获取最近区块
curl http://localhost:5000/api/blocks

# 获取钱包信息
curl http://localhost:5000/api/wallet
```

## 终端输出

启动节点时会看到：

```
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

🚀 Initializing WCOIN node...
📦 Creating genesis block...
✅ Genesis block created! Hash: 0000411b9d278c4a...
🔑 Generating new wallet...
✅ Wallet created!
💼 Wallet Address: WxGyw6+Zk5bMAkFuwajpFqdKcay4=
💰 Balance: 0.00 WCN

🌐 Starting P2P node on port 9333...
🌐 P2P Node started on port 9333

⛏️  Mining started! Address: WxGyw6+Zk5bMAkFuwajpFqdKcay4=
⛏️  Mining block #1 with difficulty 4...
✅ Block mined! Hash: 00006ac67d25aae5... (Time: 0.48s)
💰 Block #1 mined! Reward: 143.00 WCN
   Total mined: 1 blocks, 143.00 WCN

🖥️  Dashboard running at http://0.0.0.0:5000
✨ WCOIN node is running! Press Ctrl+C to stop.
```

## 挖矿过程

实时显示挖矿进度：

```
⛏️  Mining block #1 with difficulty 4...
✅ Block mined! Hash: 00006ac67d25aae5... (Time: 0.48s)
💰 Block #1 mined! Reward: 143.00 WCN
   Total mined: 1 blocks, 143.00 WCN

⛏️  Mining block #2 with difficulty 4...
✅ Block mined! Hash: 000001a0a6ebdc98... (Time: 0.03s)
💰 Block #2 mined! Reward: 143.00 WCN
   Total mined: 2 blocks, 286.00 WCN

⛏️  Mining block #3 with difficulty 4...
✅ Block mined! Hash: 000088da357835ee... (Time: 0.33s)
💰 Block #3 mined! Reward: 143.00 WCN
   Total mined: 3 blocks, 429.00 WCN
```

## 网络同步

节点连接时的输出：

```
👥 Added peer: localhost:9334
📥 Received and accepted block #5 from network
🔄 Blockchain synced! New height: 10
```

## 难度调整

每2016个区块自动调整：

```
📈 Difficulty increased to 5
📉 Difficulty decreased to 3
```

---

**提示**: 要获得最佳体验，请在现代浏览器中打开Dashboard（推荐Chrome/Firefox/Edge）。
