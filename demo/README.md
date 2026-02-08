# 什么值得投 — 多智能体商机发掘 Demo

## 快速开始

```bash
# 1. 安装依赖
cd demo
pip install -r requirements.txt

# 2. (可选) 配置 API Key，不配置则使用 Mock 模式
cp .env.example .env
# 编辑 .env 填入你的火山方舟 API Key

# 3. 启动
python app.py
```

打开浏览器访问 **http://localhost:8000**，点击「运行分析」即可。

## 两种运行模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **Mock 模式** | 无需 API Key，使用预置分析结果 | 快速体验完整 UI 和流水线 |
| **LLM 模式** | 需要 OpenAI API Key，调用真实大模型 | 真实体验 AI 分析能力 |

## 系统架构

```
样本文章 → [Crawler] → [Cleaner] → [Integrator] → [Analyst] → [Evaluator] → [Reporter]
             爬虫        清洗         信息整合        七维分析      评分排名       报告生成
```

6 个 Agent 串行协作，每个 Agent 专注一个职责：

1. **Crawler** — 采集文章（Demo 使用内置样本数据）
2. **Cleaner** — 投融资信息专项提取 + 云/AI 分类
3. **Integrator** — 补充不完整信息（模拟 MCP 调用）
4. **Analyst** — 七维商机分析（公司/潜力/影响/融资/创始人/技术/团队）
5. **Evaluator** — 七维评分 + S/A/B/C 分级 + 特殊标记
6. **Reporter** — 生成可视化报告（雷达图 + 评分条）

## 技术栈

- **后端**: Python + FastAPI + 火山方舟 API（OpenAI 兼容）
- **前端**: Tailwind CSS + Chart.js（雷达图）
- **通信**: SSE（Server-Sent Events）实时推送流水线进度
