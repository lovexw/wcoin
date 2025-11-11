# 🐳 WCOIN Docker 部署指南

使用Docker快速部署WCOIN网络，无需手动配置Python环境。

## 📋 前置要求

- Docker
- Docker Compose

### 安装Docker

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
```bash
brew install docker docker-compose
```

或下载 [Docker Desktop](https://www.docker.com/products/docker-desktop)

---

## 🚀 快速启动

### 单容器启动

```bash
# 构建镜像
docker build -t wcoin .

# 运行容器
docker run -d \
  --name wcoin-node \
  -p 9333:9333 \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  wcoin
```

访问: http://localhost:5000

### 停止容器

```bash
docker stop wcoin-node
docker rm wcoin-node
```

---

## 🌐 多节点网络（推荐）

### 启动3节点网络

```bash
# 启动所有节点
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看特定节点日志
docker-compose logs -f node1
```

### 访问Dashboard

- **节点1**: http://localhost:5000
- **节点2**: http://localhost:5001
- **节点3**: http://localhost:5002

### 管理命令

```bash
# 查看运行状态
docker-compose ps

# 停止所有节点
docker-compose down

# 重启节点
docker-compose restart

# 停止并删除数据
docker-compose down -v
```

---

## 🔧 自定义配置

### 修改节点数量

编辑 `docker-compose.yml`，添加更多节点：

```yaml
  node4:
    build: .
    container_name: wcoin-node4
    ports:
      - "9336:9333"
      - "5003:5000"
    volumes:
      - ./data/node4:/app/data
    networks:
      - wcoin-network
    depends_on:
      - node1
    command: python main.py --port 9333 --dashboard-port 5000 --peers node1:9333
```

### 自定义启动参数

```yaml
command: python main.py --port 9333 --dashboard-port 5000 --no-mining --peers node1:9333
```

### 使用环境变量

创建 `.env` 文件：

```env
WCOIN_PORT=9333
DASHBOARD_PORT=5000
GENESIS_DIFFICULTY=4
```

---

## 📊 监控和维护

### 查看容器资源使用

```bash
docker stats
```

### 进入容器Shell

```bash
docker exec -it wcoin-node1 /bin/bash
```

### 备份区块链数据

```bash
# 数据在宿主机的data目录
tar -czf wcoin-backup.tar.gz data/
```

### 恢复数据

```bash
tar -xzf wcoin-backup.tar.gz
docker-compose up -d
```

---

## 🌍 跨主机部署

### 主机A（种子节点）

```bash
docker run -d \
  --name wcoin-seed \
  -p 9333:9333 \
  -p 5000:5000 \
  wcoin
```

### 主机B（连接到A）

```bash
docker run -d \
  --name wcoin-node \
  -p 9333:9333 \
  -p 5000:5000 \
  wcoin \
  python main.py --peers <主机A的IP>:9333
```

---

## 🐛 故障排查

### 端口冲突

```bash
# 使用其他端口
docker run -p 9999:9333 -p 8888:5000 wcoin
```

### 容器无法启动

```bash
# 查看详细日志
docker logs wcoin-node

# 检查配置
docker-compose config
```

### 网络问题

```bash
# 检查网络
docker network ls
docker network inspect wcoin_wcoin-network

# 重建网络
docker-compose down
docker network prune
docker-compose up -d
```

### 清理所有数据

```bash
# 停止并删除所有容器和数据
docker-compose down -v
rm -rf data/

# 重新开始
docker-compose up -d
```

---

## 📈 生产环境建议

### 使用持久化存储

```yaml
volumes:
  - wcoin-data:/app/data

volumes:
  wcoin-data:
    driver: local
```

### 限制资源使用

```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### 添加健康检查

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/api/stats"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 自动重启

```yaml
restart: unless-stopped
```

---

## 🔐 安全建议

1. **不要暴露P2P端口到公网**（除非必要）
2. **使用防火墙限制访问**
3. **定期备份钱包文件**
4. **使用Docker secrets管理敏感数据**

```yaml
secrets:
  wallet_key:
    file: ./secrets/wallet.json
    
services:
  node1:
    secrets:
      - wallet_key
```

---

## 📚 相关资源

- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose文档](https://docs.docker.com/compose/)
- [WCOIN主文档](README.md)

---

**Happy Containerized Mining! 🐳⛏️**
