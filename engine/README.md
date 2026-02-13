# Gorse + Flink + Faiss 推荐引擎（基础骨架）

这是一个可快速启动的个性化影视 Feed 推荐系统基础工程，包含：
- **Gorse**：协同过滤/热门/基础推荐服务
- **Flink + Kafka**：行为流处理（模板）
- **Faiss**：向量召回服务（独立微服务）
- **FastAPI**：统一 Feed API（召回融合 + 简单重排）

## 目录

```text
engine/
  docker-compose.yml
  .env.example
  infra/gorse/config.toml
  services/
    api/
    faiss-recall/
  jobs/flink/sql/
```

## 快速启动

```bash
cd engine
cp .env.example .env
docker compose up -d --build
```

服务端口：
- API: `http://localhost:8000`
- Flink UI: `http://localhost:8081`
- Gorse Dashboard: `http://localhost:8088` (admin/admin)
- Gorse Server: `http://localhost:8087`
- Faiss Recall: `http://localhost:8091`

## 核心接口

### 1) 获取个性化 Feed

```bash
curl 'http://localhost:8000/feed/u_1001?scene=feed&size=20'
```

### 2) 上报行为事件

```bash
curl -X POST http://localhost:8000/events \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"u_1001","item_id":"v_2033","event_type":"click","ts":1739261000}'
```

## 下一步建议

1. 接入真实埋点（曝光/点击/播放/完播）
2. Flink作业从 Kafka 消费并写回特征存储（Redis/Postgres）
3. 替换 Faiss demo embedding 为真实文本/多模态向量
4. 增加 AB 实验、监控与降级策略
