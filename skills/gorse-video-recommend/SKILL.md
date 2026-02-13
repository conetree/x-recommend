---
name: gorse-video-recommend
description: Design and refine lightweight TV/long-video recommendation solution plans using gorse + Flink + Faiss, including architecture, capacity sizing, phased rollout checklist, and risk/tradeoff analysis. Use when users ask for cost-effective recommendation system方案, MVP快速上线, 小团队交付, 方案选型对比, 或“方案三/轻量开源栈”落地路径。
---

# Gorse Video Recommend

Generate a practical, implementation-oriented solution for TV/long-video personalization with **gorse + Flink + Faiss**, optimized for small teams, short timelines, and budget control.

## Execution Workflow

1. **Collect minimum inputs**
   - Ask only for missing core constraints: DAU, catalog size, peak QPS, daily events, timeline, budget, and main scenarios.
2. **Apply baseline assumptions when inputs are missing**
   - Read `references/lightweight-solution.md` and use its defaults explicitly.
3. **Produce two outputs in fixed order**
   - `技术方案文档`
   - `落地清单`
4. **Calibrate by scale tier**
   - If user scale is far above baseline, keep current stack as MVP and clearly state upgrade path + trigger conditions.
5. **Keep language decision-ready**
   - Prefer concrete numbers, service boundaries, SLAs, and tradeoffs over generic statements.

## Output 1: 技术方案文档

Use the following sections in order:

1. 目标与约束（规模、预算、时限、端侧形态）
2. 场景与推荐策略（以片推片、按人推片、Feed、专区/专题）
3. 数据与特征（埋点、清洗、实时/离线特征、画像更新）
4. 召回/排序/重排设计（多路召回、轻量排序、业务规则）
5. 系统架构与组件职责（gorse/Flink/Faiss/Redis/PostgreSQL/Kafka）
6. 在线服务与SLA（延迟、QPS、可用性、降级与容灾）
7. 监控评估与AB（CTR、完播率、留存、冷启动覆盖）
8. 风险与权衡（效果上限、扩展性、语义能力、运维复杂度）
9. 演进路线（从轻量MVP到增强架构的阶段升级）
10. 技术蓝图（分层架构、关键数据流、依赖关系）

### Required quality bar

- Provide explicit assumptions when user data is missing.
- Include at least one latency target and one capacity target.
- Include at least three operational safeguards (e.g.,缓存、熔断、降级、回滚).
- Distinguish **must-have for MVP** vs **phase-2 enhancements**.

## Output 2: 落地清单

Provide a phased checklist with owner role, deliverable, and acceptance signal.

Use these workstreams:

1. 数据接入与埋点（事件规范、质量校验、Kafka/Flink）
2. 特征与画像（标签体系、特征仓、向量生成与更新）
3. 召回与排序（gorse配置、Item2Vec/SVD++、候选融合）
4. 服务化与发布（在线API、缓存、灰度、回滚）
5. 评估与实验（指标口径、AB实验、监控看板）
6. 运维与成本（容量规划、告警、备份、成本跟踪）
7. 里程碑计划（按周拆分、关键风险、触发条件）

### Checklist format

For each item, include:

- **负责人角色**（如：算法/后端/数据/运维/产品）
- **输入依赖**
- **输出交付物**
- **验收标准**
- **风险与回退方案**

## References

- Read `references/lightweight-solution.md` for baseline sizing, component choices, and default tradeoffs.
- Read `references/technical-blueprint.md` for layered blueprint, data flow, dependencies, and 12-week rollout template.

When user asks for code skeleton/API layout, derive endpoint and service boundaries from `references/technical-blueprint.md` first.