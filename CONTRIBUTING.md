# 🤝 贡献指南

感谢你对WCOIN项目的关注！我们欢迎各种形式的贡献。

## 📝 贡献方式

### 1. 报告问题 (Issues)

发现bug或有新想法？请创建Issue：

- 清晰描述问题或建议
- 提供复现步骤（如果是bug）
- 包含环境信息（操作系统、Python版本等）

### 2. 提交代码 (Pull Requests)

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交改动 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### 3. 改进文档

文档同样重要！欢迎：
- 修正错别字
- 补充说明
- 添加使用示例
- 翻译文档

### 4. 分享经验

- 写博客文章
- 制作视频教程
- 在社区分享使用经验

## 🎯 开发指南

### 代码规范

遵循PEP 8 Python代码风格：

```bash
# 安装代码检查工具
pip install flake8 black

# 格式化代码
black .

# 检查代码
flake8 .
```

### 提交信息规范

使用清晰的提交信息：

```
feat: 添加新功能
fix: 修复bug
docs: 更新文档
style: 代码格式调整
refactor: 代码重构
test: 添加测试
chore: 构建/工具变动
```

### 测试

```bash
# 运行测试（如果有）
python -m pytest

# 手动测试
python main.py --no-mining
curl http://localhost:5000/api/stats
```

## 🔍 代码审查要点

Pull Request会被检查：

- [ ] 代码符合PEP 8规范
- [ ] 添加了必要的注释
- [ ] 更新了相关文档
- [ ] 测试通过
- [ ] 没有引入新的依赖（或充分说明）
- [ ] 向后兼容（或充分说明breaking changes）

## 💡 改进建议

### 当前可以改进的地方

1. **性能优化**
   - 区块链数据库存储（使用SQLite/LevelDB）
   - 交易池管理
   - 网络通信优化

2. **功能扩展**
   - 交易验证和UTXO模型
   - SPV轻节点支持
   - 交易费机制
   - 智能合约支持

3. **安全增强**
   - 更强的网络加密
   - DDoS防护
   - 分叉检测和处理

4. **用户体验**
   - CLI命令行工具
   - 移动端钱包
   - 区块浏览器
   - 更美观的Dashboard

5. **测试完善**
   - 单元测试
   - 集成测试
   - 压力测试
   - 安全测试

## 🎓 学习资源

### 区块链基础
- [Bitcoin白皮书](https://bitcoin.org/bitcoin.pdf)
- [精通比特币](https://github.com/bitcoinbook/bitcoinbook)
- [区块链技术指南](https://yeasy.gitbook.io/blockchain_guide/)

### Python相关
- [Python官方文档](https://docs.python.org/3/)
- [Flask文档](https://flask.palletsprojects.com/)
- [PEP 8风格指南](https://pep8.org/)

## 👥 社区

- 通过Issues讨论
- 在Pull Request中交流
- 分享你的使用案例

## 📧 联系方式

有问题或建议？可以：
- 创建Issue
- 提交Pull Request
- 在代码中添加注释

## ⚖️ 行为准则

- 尊重他人
- 保持友善
- 专注于技术讨论
- 欢迎新手

## 🎉 贡献者

感谢所有贡献者！

---

**让我们一起打造更好的WCOIN！💎**
