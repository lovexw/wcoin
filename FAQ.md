# ❓ WCOIN 常见问题解答 (FAQ)

## 📋 目录

- [安装问题](#安装问题)
- [运行问题](#运行问题)
- [挖矿问题](#挖矿问题)
- [网络问题](#网络问题)
- [性能问题](#性能问题)
- [其他问题](#其他问题)

---

## 安装问题

### Q: 安装依赖时出现错误？

**A:** 确保你使用的是Python 3.11+版本：

```bash
python --version  # 应该显示 3.11 或更高

# 如果版本不对，使用：
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Q: `pycryptodome` 安装失败？

**A:** 在某些系统上需要先安装构建工具：

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev build-essential

# macOS
xcode-select --install

# 然后重新安装
pip install pycryptodome
```

### Q: Windows上无法运行shell脚本？

**A:** 使用Python直接启动：

```bash
# 单节点
python main.py

# 多节点需要手动启动
python main.py --port 9333 --dashboard-port 5000
python main.py --port 9334 --dashboard-port 5001 --peers localhost:9333
```

---

## 运行问题

### Q: 启动后提示端口被占用？

**A:** 检查并更换端口：

```bash
# 检查端口占用
lsof -i :9333
lsof -i :5000

# 使用其他端口
python main.py --port 9999 --dashboard-port 8888
```

### Q: Dashboard无法访问？

**A:** 检查以下几点：

1. 确认节点正在运行
2. 访问 `http://localhost:5000` 而不是 `http://127.0.0.1:5000`
3. 检查防火墙设置
4. 查看终端输出的实际Dashboard URL

### Q: 如何停止节点？

**A:** 

```bash
# 单节点：按 Ctrl+C

# 多节点网络：
./stop_network.sh

# 或手动停止：
pkill -f "python main.py"
```

---

## 挖矿问题

### Q: 挖矿速度太慢？

**A:** 调整难度设置：

```python
# 编辑 config.py
GENESIS_DIFFICULTY = 2  # 从4降低到2
BLOCK_TIME = 30         # 测试环境可以设置更短
```

### Q: 挖矿没有奖励？

**A:** 检查：

1. 是否超过10年（525,600块后无奖励）
2. 查看区块高度和减半情况
3. 确认钱包地址正确

### Q: 如何查看挖矿收益？

**A:** 访问Dashboard或运行：

```python
python -c "
from blockchain import Blockchain
bc = Blockchain()
bc.load_from_file('data/blockchain.json')
print('总供应量:', bc.get_total_supply(), 'WCN')
"
```

### Q: 能用GPU挖矿吗？

**A:** 当前版本只支持CPU挖矿。GPU挖矿需要：

1. 使用CUDA或OpenCL重写挖矿算法
2. 修改 `blockchain/block.py` 中的 `mine_block()` 方法
3. 这超出了测试版本的范围

---

## 网络问题

### Q: 节点无法互相连接？

**A:** 检查：

```bash
# 1. 确认节点都在运行
curl http://localhost:9333/ping
curl http://localhost:9334/ping

# 2. 手动添加对等节点
python -c "
import requests
requests.post('http://localhost:9334/peers/add', 
              json={'peer': 'localhost:9333'})
"

# 3. 检查防火墙
```

### Q: 区块链无法同步？

**A:** 

1. 确认对等节点已连接
2. 检查区块链文件是否损坏
3. 删除 `data/` 目录重新同步

```bash
rm -rf data/
python main.py --peers localhost:9333
```

### Q: Docker容器间无法通信？

**A:** 使用容器名而不是localhost：

```bash
# 在docker-compose.yml中已配置
command: python main.py --peers node1:9333
```

---

## 性能问题

### Q: 如何提高挖矿速度？

**A:** 优化建议：

1. **降低难度**：`GENESIS_DIFFICULTY = 2`
2. **使用PyPy**：`pypy3 main.py`（可能快5-10倍）
3. **优化代码**：修改 `block.py` 使用更高效的哈希计算
4. **多核挖矿**：修改代码支持多线程（当前单线程）

### Q: 内存占用太高？

**A:** 

```python
# 定期清理交易池
# 在 config.py 中限制：
MAX_PENDING_TRANSACTIONS = 1000

# 或定期重启节点，数据会持久化
```

### Q: 区块链文件太大？

**A:** 

1. 实现区块修剪（Pruning）
2. 使用数据库替代JSON存储
3. 压缩历史数据

当前是测试版，JSON存储便于调试。

---

## 其他问题

### Q: 可以修改总供应量吗？

**A:** 可以，修改 `config.py`：

```python
TOTAL_SUPPLY = 21_000_000  # 改成2100万
INITIAL_REWARD = 50        # 调整初始奖励
HALVING_INTERVAL = 210000  # 调整减半周期
```

### Q: 如何备份钱包？

**A:** 

```bash
# 备份钱包文件
cp data/wallet.json wallet_backup_$(date +%Y%m%d).json

# 或导出私钥（请安全保存）
python -c "
from blockchain import Wallet
w = Wallet()
w.load_from_file('data/wallet.json')
print('私钥:', w.private_key.decode())
"
```

### Q: 支持智能合约吗？

**A:** 当前版本不支持。要添加智能合约需要：

1. 实现虚拟机（类似EVM）
2. 设计合约语言
3. 修改交易和区块结构
4. 这是一个复杂的功能，超出测试版范围

### Q: 可以连接到真实的比特币网络吗？

**A:** 不可以。WCOIN是独立的测试链，不兼容比特币协议。

### Q: 如何贡献代码？

**A:** 查看 [CONTRIBUTING.md](CONTRIBUTING.md)：

1. Fork项目
2. 创建功能分支
3. 提交Pull Request
4. 遵循代码规范

### Q: 项目是否可以商用？

**A:** 可以，MIT许可证允许商业使用。但请注意：

- 这是测试版本
- 未经过安全审计
- 不适合生产环境
- 自行承担风险

---

## 🔧 故障排除命令

### 清理环境

```bash
# 删除所有数据（谨慎！）
rm -rf data/ venv/ __pycache__/ */__pycache__/

# 重新安装
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 检查健康状态

```bash
# 测试所有功能
python test_mining.py

# 性能测试
python benchmark.py

# 功能演示
python demo.py

# API测试
python api_client_example.py
```

### 查看日志

```bash
# 查看节点日志
tail -f logs/node1.log
tail -f logs/node2.log

# 实时监控
watch -n 1 'curl -s http://localhost:9333/stats | python -m json.tool'
```

---

## 📞 获取帮助

如果以上都无法解决你的问题：

1. **查看文档**：
   - [README.md](README.md)
   - [QUICKSTART.md](QUICKSTART.md)
   - [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

2. **提交Issue**：
   - 描述问题和环境
   - 附上错误日志
   - 提供复现步骤

3. **社区讨论**：
   - 在GitHub Discussions提问
   - 查看已有的Issue

---

## 💡 最佳实践

### 测试环境配置

```python
# config.py
BLOCK_TIME = 30              # 快速测试
GENESIS_DIFFICULTY = 2       # 低难度
HALVING_INTERVAL = 10        # 快速验证减半
```

### 生产环境配置

```python
# config.py
BLOCK_TIME = 600             # 10分钟
GENESIS_DIFFICULTY = 5       # 高难度
HALVING_INTERVAL = 52560     # 1年
MAX_PEERS = 100              # 更多节点
```

### 安全建议

1. ✅ 定期备份 `data/wallet.json`
2. ✅ 使用强密码保护服务器
3. ✅ 不要暴露P2P端口到公网
4. ✅ 定期更新依赖包
5. ✅ 监控系统资源使用

---

**最后更新**: 2024-11-11  
**版本**: v1.0.0
