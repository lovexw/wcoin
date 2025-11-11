# 💎 WCOIN - Decentralized Mining System

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Beta-yellow.svg)

WCOIN是一个类似比特币的去中心化挖矿系统，使用Python实现。每个人都可以运行节点，同步区块链，并参与挖矿。

> ⚠️ **这是一个测试版本**，仅用于学习和测试目的，不建议在生产环境中使用。

## ✨ 核心特性

### 📊 经济模型
- **总供应量**: 15,000,000 WCOIN
- **初始区块奖励**: 143 WCOIN
- **减半周期**: 每52,560个区块（约1年）
- **减半次数**: 10次（10年后停止产出）
- **区块时间**: 约10分钟

### ⛓️ 区块链特性
- **工作量证明 (PoW)**: 类似比特币的挖矿机制
- **难度调整**: 每2016个区块自动调整难度
- **P2P网络**: 去中心化节点通信
- **匿名性**: 使用钱包地址，保护隐私

### 🖥️ 功能组件
- **挖矿系统**: 自动挖矿，获取区块奖励
- **P2P网络**: 节点发现和区块同步
- **Web Dashboard**: 实时显示网络状态
- **钱包管理**: RSA加密的密钥对

## 📚 文档导航

- 📖 [完整README](README.md) - 你在这里
- 🚀 [快速开始指南](QUICKSTART.md) - 5分钟上手
- 🐳 [Docker部署](DOCKER.md) - 容器化部署
- 🤝 [贡献指南](CONTRIBUTING.md) - 如何参与
- 📊 [项目总览](PROJECT_OVERVIEW.md) - 技术细节

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行单节点（本地测试）

```bash
python main.py
```

这将启动：
- P2P节点（端口9333）
- 挖矿系统
- Web Dashboard（http://localhost:5000）

### 运行多节点（P2P网络）

**节点1（种子节点）:**
```bash
python main.py --port 9333 --dashboard-port 5000
```

**节点2:**
```bash
python main.py --port 9334 --dashboard-port 5001 --peers localhost:9333
```

**节点3:**
```bash
python main.py --port 9335 --dashboard-port 5002 --peers localhost:9333
```

### 命令行参数

```bash
python main.py [选项]

选项:
  --port PORT              P2P节点端口（默认: 9333）
  --dashboard-port PORT    Dashboard端口（默认: 5000）
  --no-mining              启动但不挖矿
  --peers PEER [PEER ...]  种子节点地址（例如: localhost:9334）
```

## 📱 Dashboard功能

访问 `http://localhost:5000` 查看：

- **区块链状态**: 区块高度、难度、算力
- **经济模型**: 流通量、减半倒计时
- **挖矿状态**: 已挖区块、总奖励、钱包余额
- **网络状态**: 连接节点、运行时间
- **最近区块**: 最新10个区块详情

Dashboard每5秒自动刷新数据。

## 🏗️ 项目结构

```
wcoin/
├── blockchain/          # 区块链核心
│   ├── block.py        # 区块类
│   ├── blockchain.py   # 区块链逻辑
│   ├── transaction.py  # 交易处理
│   └── wallet.py       # 钱包管理
├── mining/             # 挖矿模块
│   └── miner.py        # 挖矿逻辑
├── network/            # P2P网络
│   └── node.py         # 节点通信
├── dashboard/          # Web界面
│   ├── app.py          # Flask后端
│   └── templates/      # HTML模板
├── config.py           # 配置文件
├── main.py             # 主程序
└── data/               # 数据存储
    ├── blockchain.json # 区块链数据
    ├── wallet.json     # 钱包数据
    └── peers.json      # 节点列表
```

## 🔐 安全性与匿名性

- **钱包地址**: 基于RSA公钥生成，类似比特币地址
- **交易签名**: 使用私钥签名，公钥验证
- **匿名性**: 只显示钱包地址，不涉及真实身份
- **去中心化**: 无中心服务器，所有节点平等

## 📈 经济模型详解

### 供应量计算

总供应量通过减半机制控制：

```
第1年（0-52559块）:    143 WCN/块
第2年（52560-105119块）: 71.5 WCN/块
第3年:                  35.75 WCN/块
...
第10年:                 0.14 WCN/块
第11年及以后:           0 WCN/块
```

总量 ≈ 143 × 52560 × (1 + 1/2 + 1/4 + ... + 1/512) ≈ 15,000,000 WCN

### 难度调整

类似比特币，每2016个区块调整一次难度：
- 如果出块时间 < 5分钟 → 增加难度
- 如果出块时间 > 20分钟 → 降低难度
- 目标：保持约10分钟出块时间

## 🌐 P2P网络

### 节点通信

节点间通过HTTP API通信：
- `GET /blockchain`: 获取完整区块链
- `POST /block`: 接收新区块
- `GET /peers`: 获取节点列表
- `POST /peers/add`: 添加新节点

### 区块同步

节点启动时：
1. 连接到种子节点
2. 下载区块链
3. 验证区块有效性
4. 替换本地链（如果远程链更长）

### 区块广播

挖到新区块时：
1. 验证区块有效性
2. 广播到所有已知节点
3. 节点接收并验证
4. 接受有效区块并继续挖矿

## 💻 开发指南

### 添加新功能

1. **修改配置**: 编辑 `config.py`
2. **扩展区块链**: 修改 `blockchain/` 模块
3. **定制挖矿**: 修改 `mining/miner.py`
4. **优化网络**: 修改 `network/node.py`

### 测试

```bash
# 运行单节点测试
python main.py --no-mining

# 运行多节点测试
python main.py --port 9333 &
python main.py --port 9334 --peers localhost:9333 &
python main.py --port 9335 --peers localhost:9333 &
```

## 🎯 使用场景

- **学习区块链**: 理解PoW、P2P、难度调整等机制
- **测试挖矿**: 在本地环境测试挖矿算法
- **私有链**: 搭建企业内部的私有区块链
- **教学演示**: 展示去中心化系统工作原理

## ⚠️ 注意事项

### 这是测试版本

- 仅用于学习和测试
- 不建议用于生产环境
- 没有经过完整的安全审计

### 性能考虑

- 难度过高会导致出块时间过长
- 区块链数据会随时间增长
- P2P网络在大规模部署时需要优化

### 安全建议

- 定期备份 `data/` 目录
- 保护好 `wallet.json` 文件
- 不要共享私钥
- 使用防火墙保护P2P端口

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

## 📄 许可证

MIT License - 自由使用和修改

## 🎉 致谢

灵感来源于比特币白皮书和去中心化理念。

---

**Happy Mining! ⛏️💎**
