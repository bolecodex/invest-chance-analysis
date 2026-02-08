"""
商机发掘 — 多智能体最小 Demo
============================
运行方式: python app.py
访问地址: http://localhost:8000
"""
from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()

# ╔══════════════════════════════════════════════════════════════════╗
# ║                        配置 & 全局状态                          ║
# ╚══════════════════════════════════════════════════════════════════╝

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
USE_MOCK = not OPENAI_API_KEY or OPENAI_API_KEY in ("sk-your-key-here", "your-ark-api-key-here")

# 内存数据库
db: dict[str, list] = {
    "articles": [],
    "cleaned": [],
    "opportunities": [],
    "reports": [],
    "pipeline_runs": [],
}


# ╔══════════════════════════════════════════════════════════════════╗
# ║                        样本文章数据                             ║
# ╚══════════════════════════════════════════════════════════════════╝

SAMPLE_ARTICLES = [
    {
        "id": "art-001",
        "title": "月之暗面完成超10亿美元融资，估值约33亿美元",
        "author": "36氪",
        "publish_time": "2026-01-15",
        "url": "https://example.com/article/001",
        "content": """
        据36氪独家获悉，大模型创业公司月之暗面（Moonshot AI）已于近期完成超10亿美元融资，
        投后估值约33亿美元。本轮融资由红杉中国、小红书领投，阿里巴巴、美团、蓝驰创投等跟投。

        月之暗面成立于2023年3月，创始人杨植麟毕业于清华大学计算机系，曾在卡内基梅隆大学
        (CMU) 攻读博士学位，师从苹果AI负责人 Ruslan Salakhutdinov。杨植麟曾在 Google Brain
        实习，发表过多篇 NeurIPS、ICML 顶会论文，其代表作 Transformer-XL 和 XLNet 论文
        引用量合计超过8000次。

        公司核心产品为 Kimi 智能助手，主打超长上下文窗口能力（支持200万字输入），上线以来
        月活用户已突破1200万。团队目前约200人，核心成员来自清华大学、Google Brain、Meta AI
        等顶级机构。

        月之暗面此前已完成天使轮（2023年6月，约2000万美元，红杉中国领投）和A轮（2023年12月，
        约10亿美元，多家机构联合投资）。此轮融资后，月之暗面将成为国内估值最高的大模型创业
        公司之一，资金将主要用于模型训练算力采购和产品研发。
        """,
    },
    {
        "id": "art-002",
        "title": "云原生安全公司探真科技完成A轮数千万元融资",
        "author": "投资界",
        "publish_time": "2026-01-20",
        "url": "https://example.com/article/002",
        "content": """
        投资界1月20日消息，云原生安全公司探真科技近日宣布完成数千万元A轮融资，本轮融资由
        经纬创投领投，老股东红点中国跟投。融资资金将主要用于产品研发和市场拓展。

        探真科技成立于2024年初，专注于云原生环境下的安全检测与防护。公司创始人兼CEO李明辉
        拥有15年网络安全从业经验，曾任阿里云安全产品线负责人，此前在绿盟科技担任高级研究员。
        CTO 王磊为清华大学网络安全方向博士，曾在 IEEE S&P、USENIX Security 等顶级安全
        会议上发表多篇论文。

        公司核心产品"探真云卫"是一款面向 Kubernetes 环境的安全平台，提供容器镜像扫描、
        运行时威胁检测、合规审计等功能。目前已服务超过50家企业客户，包括多家金融机构和
        互联网公司。

        据 IDC 报告，2025年中国云安全市场规模达到187亿元，年增长率超过25%。云原生安全
        作为其中增速最快的子赛道，预计2027年市场规模将超过80亿元。探真科技在容器安全
        这一细分领域已进入前三名。
        """,
    },
    {
        "id": "art-003",
        "title": "AI Agent 自动化平台 FlowAgent 获得500万美元种子轮融资",
        "author": "机器之心",
        "publish_time": "2026-02-01",
        "url": "https://example.com/article/003",
        "content": """
        AI Agent 工作流自动化平台 FlowAgent 近日宣布完成500万美元种子轮融资，由真格基金
        领投，奇绩创坛、硅谷知名天使投资人参投。

        FlowAgent 成立于2025年9月，创始人张涵为北京大学计算机系本科、斯坦福大学 AI Lab
        博士，曾在 OpenAI 担任研究工程师，参与了 GPT-4 的 RLHF 训练工作。联合创始人
        刘思远为前字节跳动飞书团队技术负责人，拥有丰富的企业级SaaS产品经验。

        FlowAgent 的核心产品是一个低代码 AI Agent 编排平台，用户可以通过拖拽方式构建
        复杂的 AI 工作流，支持多模型调度、工具调用和人机协作。目前产品处于内测阶段，
        已有约200家企业申请试用。

        张涵在斯坦福期间发表了关于大模型工具调用（Tool-Use）和多智能体协作的研究论文，
        其中"ReAct: Synergizing Reasoning and Acting"一文在 Google Scholar 上引用量
        超过2000次。公司还开源了核心推理框架 FlowEngine，在 GitHub 上已获得 3.2k Stars。

        AI Agent 赛道在2025年下半年迎来投资热潮，据不完全统计，2025年全球 AI Agent
        相关创业公司共获得超过50亿美元融资。FlowAgent 所在的企业级 Agent 平台赛道
        竞争者包括 LangChain（已融资2500万美元）、CrewAI、AutoGen 等。
        """,
    },
]


# ╔══════════════════════════════════════════════════════════════════╗
# ║                         LLM 调用工具                            ║
# ╚══════════════════════════════════════════════════════════════════╝

openai_client = None


def get_openai_client():
    global openai_client
    if openai_client is None and not USE_MOCK:
        from openai import OpenAI
        openai_client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
            timeout=120.0,
        )
    return openai_client


async def call_llm(system_prompt: str, user_prompt: str) -> dict:
    """调用 LLM 并返回 JSON 结果"""
    if USE_MOCK:
        return {}  # Mock 模式下由各 Agent 自己提供 fallback

    client = get_openai_client()
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        content = response.choices[0].message.content
        # 从响应中提取 JSON（兼容模型返回 markdown 代码块的情况）
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        # 找到第一个 { 和最后一个 }
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            content = content[start:end]
        return json.loads(content)
    except Exception as e:
        print(f"  [LLM Error] {type(e).__name__}: {e}")
        return {}  # 出错时回退到 Mock


# ╔══════════════════════════════════════════════════════════════════╗
# ║                       Agent 实现                                ║
# ╚══════════════════════════════════════════════════════════════════╝


class BaseAgent:
    name: str = "base"
    emoji: str = "🤖"

    async def run(self, input_data: Any) -> Any:
        raise NotImplementedError


# ─────────────── Agent 1: Crawler (使用样本数据) ───────────────


class CrawlerAgent(BaseAgent):
    name = "Crawler"
    emoji = "🕷️"

    async def run(self, _=None) -> list[dict]:
        """模拟爬取文章 — 直接返回样本数据"""
        await asyncio.sleep(0.5)  # 模拟网络延迟
        return SAMPLE_ARTICLES


# ─────────────── Agent 2: Cleaner (投融资聚焦清洗) ───────────────


class CleanerAgent(BaseAgent):
    name = "Cleaner"
    emoji = "🧹"

    async def run(self, articles: list[dict]) -> list[dict]:
        # 并发处理所有文章，大幅提速
        tasks = [self._clean_one(article) for article in articles]
        results = await asyncio.gather(*tasks)
        return list(results)

    async def _clean_one(self, article: dict) -> dict:
        system_prompt = """你是投融资信息提取专家。请只返回一个JSON对象，不要任何解释文字。格式：
{"title":"标题","summary":"50字摘要","primary_category":"cloud|ai|cloud+ai","signal_type":"融资事件|并购合作|产品发布|技术突破","funding_company":"公司名","funding_round":"轮次","funding_amount":"金额","investors":["投资方"],"lead_investor":"领投方","valuation":"估值","founder_name":"创始人","founder_clues":["背景线索"],"company_desc":"业务描述100字内","team_clues":["团队线索"],"tech_clues":["技术/论文线索"],"completeness_score":0.0}
completeness_score(0~1): 公司+描述0.1,融资0.1,投资方0.08,创始人0.08,团队0.07,技术0.07,产品0.08,市场0.07,竞品0.08,时间0.1,分类0.1,客户0.07"""

        # 压缩文章内容，减少 token
        content = " ".join(article["content"].split())
        user_prompt = f"标题: {article['title']}\n正文: {content}"

        result = await call_llm(system_prompt, user_prompt)

        if not result:  # Mock fallback
            result = self._mock_clean(article)

        result["article_id"] = article["id"]
        result["source_url"] = article.get("url", "")
        result["publish_time"] = article.get("publish_time", "")
        return result

    def _mock_clean(self, article: dict) -> dict:
        """Mock 模式的清洗结果"""
        mocks = {
            "art-001": {
                "title": article["title"],
                "summary": "月之暗面完成超10亿美元融资，估值约33亿美元，红杉中国、小红书领投",
                "primary_category": "ai",
                "signal_type": "融资事件",
                "funding_company": "月之暗面 (Moonshot AI)",
                "funding_round": "B轮",
                "funding_amount": "超10亿美元",
                "investors": ["红杉中国", "小红书", "阿里巴巴", "美团", "蓝驰创投"],
                "lead_investor": "红杉中国、小红书",
                "valuation": "约33亿美元",
                "founder_name": "杨植麟",
                "founder_clues": [
                    "清华大学计算机系毕业",
                    "CMU博士（导师: Ruslan Salakhutdinov）",
                    "Google Brain 实习经历",
                    "NeurIPS/ICML 顶会论文作者",
                ],
                "company_desc": "大模型创业公司，核心产品Kimi智能助手，主打超长上下文窗口（200万字），月活突破1200万",
                "team_clues": ["团队约200人", "核心成员来自清华、Google Brain、Meta AI"],
                "tech_clues": [
                    "Transformer-XL 论文作者（引用超8000次）",
                    "XLNet 论文作者",
                    "多篇NeurIPS/ICML顶会论文",
                ],
                "completeness_score": 0.92,
            },
            "art-002": {
                "title": article["title"],
                "summary": "云原生安全公司探真科技完成A轮数千万元融资，经纬创投领投",
                "primary_category": "cloud",
                "signal_type": "融资事件",
                "funding_company": "探真科技",
                "funding_round": "A轮",
                "funding_amount": "数千万元人民币",
                "investors": ["经纬创投", "红点中国"],
                "lead_investor": "经纬创投",
                "valuation": "未披露",
                "founder_name": "李明辉",
                "founder_clues": [
                    "15年网络安全从业经验",
                    "前阿里云安全产品线负责人",
                    "前绿盟科技高级研究员",
                ],
                "company_desc": "云原生安全公司，核心产品'探真云卫'面向K8s环境提供容器安全检测与防护，已服务50+企业客户",
                "team_clues": [
                    "CTO王磊为清华网络安全博士",
                    "IEEE S&P/USENIX Security顶会论文作者",
                ],
                "tech_clues": [
                    "CTO发表IEEE S&P/USENIX Security论文",
                    "容器安全细分领域前三",
                ],
                "completeness_score": 0.78,
            },
            "art-003": {
                "title": article["title"],
                "summary": "AI Agent平台FlowAgent获500万美元种子轮，真格基金领投",
                "primary_category": "ai",
                "signal_type": "融资事件",
                "funding_company": "FlowAgent",
                "funding_round": "种子轮",
                "funding_amount": "500万美元",
                "investors": ["真格基金", "奇绩创坛"],
                "lead_investor": "真格基金",
                "valuation": "未披露",
                "founder_name": "张涵",
                "founder_clues": [
                    "北京大学计算机系本科",
                    "斯坦福大学AI Lab博士",
                    "前OpenAI研究工程师",
                    "参与GPT-4 RLHF训练",
                ],
                "company_desc": "低代码AI Agent编排平台，支持拖拽构建AI工作流，支持多模型调度和工具调用，约200家企业申请试用",
                "team_clues": [
                    "联合创始人刘思远为前字节跳动飞书技术负责人",
                    "企业级SaaS经验丰富",
                ],
                "tech_clues": [
                    "ReAct论文引用超2000次",
                    "开源FlowEngine获GitHub 3.2k Stars",
                    "大模型工具调用和多智能体协作研究",
                ],
                "completeness_score": 0.85,
            },
        }
        return mocks.get(article["id"], {"completeness_score": 0.5})


# ─────────────── Agent 3: Integrator (信息整合补充) ──────────────


class IntegratorAgent(BaseAgent):
    name = "Integrator"
    emoji = "🧩"

    async def run(self, cleaned_articles: list[dict]) -> list[dict]:
        results = []
        for item in cleaned_articles:
            score = item.get("completeness_score", 0)
            if score < 0.7:
                item = await self._supplement(item)
            item["integration_status"] = "supplemented" if score < 0.7 else "passed"
            results.append(item)
        return results

    async def _supplement(self, item: dict) -> dict:
        """模拟通过 MCP 工具补充信息"""
        await asyncio.sleep(0.3)
        # 在真实场景中，这里会调用投融资数据MCP、学术搜索MCP等
        item["completeness_score"] = min(item.get("completeness_score", 0) + 0.15, 1.0)
        item.setdefault("integration_notes", []).append(
            "通过投融资数据MCP补充了缺失字段"
        )
        return item


# ─────────────── Agent 4: Analyst (七维商机分析) ───────────────


class AnalystAgent(BaseAgent):
    name = "Analyst"
    emoji = "🔬"

    async def run(self, integrated_data: list[dict]) -> list[dict]:
        # 并发分析所有条目
        tasks = [self._analyze(item) for item in integrated_data]
        results = await asyncio.gather(*tasks)
        return [opp for opp in results if opp]

    async def _analyze(self, item: dict) -> Optional[dict]:
        system_prompt = """你是云计算和AI商机分析专家。请只返回一个JSON对象，不要任何解释文字。按七大维度分析：
{
  "id": "opp-xxx",
  "title": "商机标题（简洁有力）",
  "summary": "一句话概述",
  "domain": "cloud | ai | cloud+ai",
  "signal_type": "融资事件 | 并购合作 | 产品发布 | 技术突破",
  "company_profile": {
    "name": "公司名",
    "what_they_do": "用通俗语言描述公司做什么（2-3句话）",
    "products": ["产品列表"],
    "business_model": "商业模式",
    "stage": "seed | early | growth | mature"
  },
  "potential": {
    "market_size": "目标市场规模描述",
    "competitive_advantage": "核心竞争优势",
    "moat_type": "技术壁垒 | 数据壁垒 | 网络效应 | 先发优势 | 品牌 | 无明显护城河",
    "potential_rating": "high | medium | low",
    "reasoning": "潜力判断依据"
  },
  "industry_impact": {
    "scope": "颠覆性 | 重大 | 中等 | 局部",
    "how_it_changes": "具体会怎样改变行业",
    "timeline": "影响显现时间"
  },
  "funding_logic": {
    "round": "融资轮次",
    "amount": "金额",
    "investors": ["投资方"],
    "why_fundable": "为什么资本愿意投（2-3句话分析融资逻辑）",
    "investor_signal": "投资方阵容传递的信号"
  },
  "founder_profile": {
    "name": "创始人姓名",
    "background_summary": "创始人背景一句话总结",
    "highlights": ["关键亮点"],
    "rating": "strong | average | unknown"
  },
  "core_tech": {
    "has_papers": true,
    "key_papers": ["论文简述"],
    "open_source": ["开源项目"],
    "originality": "原创突破 | 工程创新 | 应用集成 | 跟随复制",
    "rating": "cutting_edge | solid | average | weak"
  },
  "star_team": {
    "is_star_team": true,
    "signals": ["明星信号"],
    "rating": "all_star | strong | average | unknown"
  },
  "time_sensitivity": "urgent | short_term | medium_term | long_term",
  "confidence": 0.85
}"""

        user_prompt = f"清洗后的文章数据:\n{json.dumps(item, ensure_ascii=False, indent=2)}"
        result = await call_llm(system_prompt, user_prompt)

        if not result:
            result = self._mock_analyze(item)

        result["id"] = f"opp-{uuid.uuid4().hex[:8]}"
        result["source_article_id"] = item.get("article_id", "")
        result["created_at"] = datetime.now().isoformat()
        return result

    def _mock_analyze(self, item: dict) -> dict:
        company = item.get("funding_company", "未知公司")
        mocks = {
            "月之暗面 (Moonshot AI)": {
                "title": f"月之暗面超10亿美元融资 — 国产大模型头部玩家加速商业化",
                "summary": "月之暗面以Kimi产品切入长文本赛道，凭借顶级团队和明星资本持续融资，估值跻身国内大模型第一梯队",
                "domain": "ai",
                "signal_type": "融资事件",
                "company_profile": {
                    "name": "月之暗面 (Moonshot AI)",
                    "what_they_do": "开发大语言模型，核心产品Kimi智能助手以超长上下文窗口（200万字）为差异化卖点，面向C端用户提供AI对话和内容理解服务",
                    "products": ["Kimi智能助手", "Moonshot API"],
                    "business_model": "C端免费+增值订阅 / B端API按量计费",
                    "stage": "growth",
                },
                "potential": {
                    "market_size": "中国大模型市场2025年规模约200亿元，预计2027年突破600亿元",
                    "competitive_advantage": "超长上下文技术领先；Kimi月活1200万，C端用户基础扎实",
                    "moat_type": "技术壁垒",
                    "potential_rating": "high",
                    "reasoning": "大模型赛道天花板极高，月之暗面在长文本方向建立了技术先发优势和用户心智，且有持续融资能力支撑烧钱期",
                },
                "industry_impact": {
                    "scope": "重大",
                    "how_it_changes": "推动大模型从通用对话向长文档理解、知识管理等专业场景渗透，加速AI替代传统内容处理工具",
                    "timeline": "12-18个月内竞争格局将进一步清晰",
                },
                "funding_logic": {
                    "round": "B轮",
                    "amount": "超10亿美元",
                    "investors": ["红杉中国", "小红书", "阿里巴巴", "美团", "蓝驰创投"],
                    "why_fundable": "创始人杨植麟是Transformer-XL/XLNet作者，论文引用8000+次，学术影响力顶级；Kimi产品月活破千万验证了市场需求；大模型赛道是当前一级市场最热赛道，顶级VC争相布局",
                    "investor_signal": "红杉中国连续加注+互联网巨头(阿里/美团)战略投资，说明产业界看好其商业化潜力",
                },
                "founder_profile": {
                    "name": "杨植麟",
                    "background_summary": "清华CS本科→CMU博士→Google Brain，Transformer-XL/XLNet论文一作，引用超8000次",
                    "highlights": [
                        "清华大学计算机系",
                        "CMU博士（导师为苹果AI负责人）",
                        "Google Brain 研究经历",
                        "Transformer-XL/XLNet 一作（引用8000+）",
                    ],
                    "rating": "strong",
                },
                "core_tech": {
                    "has_papers": True,
                    "key_papers": [
                        "Transformer-XL (NeurIPS, 引用~5000)",
                        "XLNet (NeurIPS, 引用~3000)",
                    ],
                    "open_source": [],
                    "originality": "原创突破",
                    "rating": "cutting_edge",
                },
                "star_team": {
                    "is_star_team": True,
                    "signals": [
                        "创始人为Transformer-XL/XLNet论文一作",
                        "CMU博士+Google Brain背景",
                        "核心团队来自清华/Google Brain/Meta AI",
                        "团队200人规模",
                    ],
                    "rating": "all_star",
                },
                "time_sensitivity": "urgent",
                "confidence": 0.92,
            },
            "探真科技": {
                "title": "探真科技A轮融资 — 云原生安全赛道卡位战",
                "summary": "探真科技切入K8s容器安全细分赛道，创始人有阿里云安全背景，经纬领投看好云安全增长",
                "domain": "cloud",
                "signal_type": "融资事件",
                "company_profile": {
                    "name": "探真科技",
                    "what_they_do": "提供云原生环境下的安全检测与防护，核心产品面向Kubernetes环境，覆盖容器镜像扫描、运行时威胁检测和合规审计",
                    "products": ["探真云卫"],
                    "business_model": "SaaS订阅 + 私有化部署",
                    "stage": "early",
                },
                "potential": {
                    "market_size": "中国云安全市场2025年187亿元，云原生安全子赛道预计2027年达80亿元",
                    "competitive_advantage": "创始人深耕云安全15年，阿里云背景带来的行业认知和客户资源",
                    "moat_type": "先发优势",
                    "potential_rating": "medium",
                    "reasoning": "云原生安全是高增长赛道（25%+），但竞争激烈，公司需要在产品深度上持续投入以建立技术壁垒",
                },
                "industry_impact": {
                    "scope": "局部",
                    "how_it_changes": "推动云原生安全从合规驱动向主动防御演进，提升K8s环境安全基线",
                    "timeline": "6-12个月",
                },
                "funding_logic": {
                    "round": "A轮",
                    "amount": "数千万元人民币",
                    "investors": ["经纬创投", "红点中国"],
                    "why_fundable": "云安全赛道增长确定性高（25%+），创始人有阿里云安全一线实战经验，50+付费客户验证了产品价值",
                    "investor_signal": "经纬创投在安全赛道有多个成功案例，领投说明对云安全方向持续看好",
                },
                "founder_profile": {
                    "name": "李明辉",
                    "background_summary": "15年安全老兵，前阿里云安全产品线负责人，前绿盟科技高级研究员",
                    "highlights": [
                        "15年网络安全经验",
                        "前阿里云安全产品线负责人",
                        "前绿盟科技高级研究员",
                    ],
                    "rating": "strong",
                },
                "core_tech": {
                    "has_papers": True,
                    "key_papers": ["CTO在IEEE S&P/USENIX Security发表论文"],
                    "open_source": [],
                    "originality": "工程创新",
                    "rating": "solid",
                },
                "star_team": {
                    "is_star_team": False,
                    "signals": [
                        "创始人阿里云安全背景",
                        "CTO清华安全博士+顶会论文",
                    ],
                    "rating": "strong",
                },
                "time_sensitivity": "short_term",
                "confidence": 0.78,
            },
            "FlowAgent": {
                "title": "FlowAgent种子轮 — AI Agent工作流编排的早期入场者",
                "summary": "前OpenAI工程师创业做Agent编排平台，ReAct论文加持，赛道正热但竞争激烈",
                "domain": "ai",
                "signal_type": "融资事件",
                "company_profile": {
                    "name": "FlowAgent",
                    "what_they_do": "低代码AI Agent编排平台，让企业用户通过拖拽方式构建复杂AI工作流，支持多模型调度、工具调用和人机协作",
                    "products": ["FlowAgent Platform", "FlowEngine (开源)"],
                    "business_model": "SaaS订阅（按工作流调用量计费）",
                    "stage": "seed",
                },
                "potential": {
                    "market_size": "全球AI Agent市场2025年融资超50亿美元，企业级Agent平台赛道处于早期爆发阶段",
                    "competitive_advantage": "创始人OpenAI背景+ReAct论文引用2000+，对Agent技术有深刻理解；开源策略积累开发者生态",
                    "moat_type": "技术壁垒",
                    "potential_rating": "high",
                    "reasoning": "AI Agent被视为大模型最重要的应用范式，赛道天花板极高；但当前处于极早期，产品能否跑出来取决于执行力",
                },
                "industry_impact": {
                    "scope": "重大",
                    "how_it_changes": "降低企业构建AI自动化工作流的门槛，加速AI从'对话助手'向'自主执行任务'的范式转移",
                    "timeline": "18-24个月",
                },
                "funding_logic": {
                    "round": "种子轮",
                    "amount": "500万美元",
                    "investors": ["真格基金", "奇绩创坛"],
                    "why_fundable": "创始人有OpenAI+斯坦福背景，ReAct论文是Agent领域奠基性工作；AI Agent赛道正热，投资人抢跑布局早期项目",
                    "investor_signal": "真格+奇绩是典型天使/种子轮强势投资方，说明对创始人个人能力高度认可",
                },
                "founder_profile": {
                    "name": "张涵",
                    "background_summary": "北大本科→斯坦福AI Lab博士→OpenAI研究工程师，参与GPT-4训练，ReAct论文引用2000+",
                    "highlights": [
                        "北京大学计算机系本科",
                        "斯坦福大学AI Lab博士",
                        "前OpenAI研究工程师（参与GPT-4）",
                        "ReAct论文引用超2000次",
                    ],
                    "rating": "strong",
                },
                "core_tech": {
                    "has_papers": True,
                    "key_papers": [
                        "ReAct: Synergizing Reasoning and Acting (引用2000+)"
                    ],
                    "open_source": ["FlowEngine (GitHub 3.2k Stars)"],
                    "originality": "原创突破",
                    "rating": "cutting_edge",
                },
                "star_team": {
                    "is_star_team": True,
                    "signals": [
                        "创始人前OpenAI研究工程师",
                        "斯坦福AI Lab博士",
                        "ReAct论文引用2000+",
                        "联合创始人前字节飞书技术负责人",
                    ],
                    "rating": "all_star",
                },
                "time_sensitivity": "urgent",
                "confidence": 0.82,
            },
        }
        return mocks.get(company, self._generic_mock(item))

    def _generic_mock(self, item: dict) -> dict:
        return {
            "title": f"{item.get('funding_company', '未知')} — 商机分析",
            "summary": item.get("summary", "待分析"),
            "domain": item.get("primary_category", "ai"),
            "signal_type": item.get("signal_type", "其他"),
            "company_profile": {"name": item.get("funding_company", ""), "what_they_do": item.get("company_desc", ""), "products": [], "business_model": "未知", "stage": "early"},
            "potential": {"market_size": "待调研", "competitive_advantage": "待分析", "moat_type": "无明显护城河", "potential_rating": "medium", "reasoning": "信息不足"},
            "industry_impact": {"scope": "中等", "how_it_changes": "待分析", "timeline": "待评估"},
            "funding_logic": {"round": item.get("funding_round", ""), "amount": item.get("funding_amount", ""), "investors": item.get("investors", []), "why_fundable": "待分析", "investor_signal": "待分析"},
            "founder_profile": {"name": item.get("founder_name", ""), "background_summary": "待调研", "highlights": item.get("founder_clues", []), "rating": "unknown"},
            "core_tech": {"has_papers": False, "key_papers": [], "open_source": [], "originality": "待评估", "rating": "average"},
            "star_team": {"is_star_team": False, "signals": [], "rating": "unknown"},
            "time_sensitivity": "medium_term",
            "confidence": 0.5,
        }


# ─────────────── Agent 5: Evaluator (七维评分排名) ──────────────


class EvaluatorAgent(BaseAgent):
    name = "Evaluator"
    emoji = "⚖️"

    # 权重配置
    WEIGHTS = {
        "company": 0.10,
        "potential": 0.20,
        "impact": 0.15,
        "funding": 0.20,
        "founder": 0.15,
        "tech": 0.10,
        "team": 0.10,
    }

    async def run(self, opportunities: list[dict]) -> list[dict]:
        # 并发评分
        tasks = [self._score(opp) for opp in opportunities]
        scored = list(await asyncio.gather(*tasks))
        # 排序
        scored.sort(key=lambda x: x.get("scores", {}).get("total", 0), reverse=True)
        for i, opp in enumerate(scored):
            opp["rank"] = i + 1
        return scored

    async def _score(self, opp: dict) -> dict:
        system_prompt = """你是商机评分专家。请只返回一个JSON对象，不要任何解释文字。格式:
{"scores":{"company":8,"potential":9,"impact":7,"funding":9,"founder":9,"tech":10,"team":9,"total":8.8},"importance_level":"S","special_tag":"all_rounder|tech_dark_horse|capital_darling|none","one_line_verdict":"一句话评语"}
每维度1-10分。total=company*0.1+potential*0.2+impact*0.15+funding*0.2+founder*0.15+tech*0.1+team*0.1
S级(>=8.0) A级(6.5-7.9) B级(5.0-6.4) C级(<5.0)"""

        # 精简输入，只传关键信息
        summary = {
            "title": opp.get("title", ""),
            "company": opp.get("company_profile", {}).get("name", ""),
            "what": opp.get("company_profile", {}).get("what_they_do", "")[:100],
            "funding": f"{opp.get('funding_logic', {}).get('round', '')} {opp.get('funding_logic', {}).get('amount', '')}",
            "investors": opp.get("funding_logic", {}).get("investors", []),
            "founder": opp.get("founder_profile", {}).get("background_summary", ""),
            "tech": opp.get("core_tech", {}).get("rating", ""),
            "papers": opp.get("core_tech", {}).get("has_papers", False),
            "star_team": opp.get("star_team", {}).get("is_star_team", False),
            "potential": opp.get("potential", {}).get("potential_rating", ""),
            "impact": opp.get("industry_impact", {}).get("scope", ""),
        }
        user_prompt = json.dumps(summary, ensure_ascii=False)
        result = await call_llm(system_prompt, user_prompt)

        if not result:
            result = self._mock_score(opp)

        opp["scores"] = result.get("scores", {})
        opp["importance_level"] = result.get("importance_level", "B")
        opp["special_tag"] = result.get("special_tag", "none")
        opp["one_line_verdict"] = result.get("one_line_verdict", "")
        return opp

    def _mock_score(self, opp: dict) -> dict:
        company = opp.get("company_profile", {}).get("name", "")
        mocks = {
            "月之暗面 (Moonshot AI)": {
                "scores": {"company": 9, "potential": 9, "impact": 8, "funding": 10, "founder": 10, "tech": 10, "team": 9, "total": 9.25},
                "importance_level": "S",
                "special_tag": "all_rounder",
                "one_line_verdict": "全明星团队+巨额融资+顶级技术，国产大模型赛道头部标的",
            },
            "探真科技": {
                "scores": {"company": 7, "potential": 7, "impact": 5, "funding": 6, "founder": 7, "tech": 6, "team": 6, "total": 6.40},
                "importance_level": "B",
                "special_tag": "none",
                "one_line_verdict": "云安全增长赛道的务实选手，创始人行业经验丰富但差异化有待加强",
            },
            "FlowAgent": {
                "scores": {"company": 7, "potential": 9, "impact": 8, "funding": 7, "founder": 9, "tech": 9, "team": 8, "total": 8.15},
                "importance_level": "S",
                "special_tag": "tech_dark_horse",
                "one_line_verdict": "OpenAI+ReAct论文背景的Agent创业者，技术底蕴深厚，赛道正处爆发前夜",
            },
        }
        return mocks.get(company, {
            "scores": {"company": 5, "potential": 5, "impact": 5, "funding": 5, "founder": 5, "tech": 5, "team": 5, "total": 5.0},
            "importance_level": "B",
            "special_tag": "none",
            "one_line_verdict": "待进一步分析",
        })


# ─────────────── Agent 6: Reporter (图文报告生成) ──────────────


class ReporterAgent(BaseAgent):
    name = "Reporter"
    emoji = "📊"

    async def run(self, opportunities: list[dict]) -> list[dict]:
        reports = []
        for opp in opportunities:
            report = self._generate_report(opp)
            reports.append(report)
        return reports

    def _generate_report(self, opp: dict) -> dict:
        scores = opp.get("scores", {})
        cp = opp.get("company_profile", {})
        pot = opp.get("potential", {})
        imp = opp.get("industry_impact", {})
        fl = opp.get("funding_logic", {})
        fp = opp.get("founder_profile", {})
        ct = opp.get("core_tech", {})
        st = opp.get("star_team", {})

        level = opp.get("importance_level", "B")
        level_colors = {"S": "#dc2626", "A": "#ea580c", "B": "#ca8a04", "C": "#6b7280"}
        level_labels = {"S": "S级 · 重大机会", "A": "A级 · 高价值", "B": "B级 · 有潜力", "C": "C级 · 低优先"}

        tag_map = {
            "tech_dark_horse": "🏴 技术黑马",
            "capital_darling": "💰 资本宠儿",
            "all_rounder": "⭐ 全能选手",
            "none": "",
        }
        special = tag_map.get(opp.get("special_tag", "none"), "")

        # 生成 Mermaid 流程图代码
        mermaid_code = f"""graph LR
    A["{cp.get('name', '公司')}"] --> B["核心产品"]
    B --> C["{', '.join(cp.get('products', ['产品'])[:2])}"]
    A --> D["融资"]
    D --> E["{fl.get('round', '?')} {fl.get('amount', '?')}"]
    A --> F["技术"]
    F --> G["{ct.get('originality', '?')}"]"""

        # 构建雷达图数据
        radar_data = {
            "labels": ["公司业务", "市场潜力", "行业影响", "融资逻辑", "创始人", "核心技术", "团队"],
            "values": [
                scores.get("company", 5),
                scores.get("potential", 5),
                scores.get("impact", 5),
                scores.get("funding", 5),
                scores.get("founder", 5),
                scores.get("tech", 5),
                scores.get("team", 5),
            ],
        }

        return {
            "opportunity_id": opp.get("id", ""),
            "title": opp.get("title", ""),
            "level": level,
            "level_color": level_colors.get(level, "#6b7280"),
            "level_label": level_labels.get(level, ""),
            "special_tag": special,
            "total_score": scores.get("total", 0),
            "one_line_verdict": opp.get("one_line_verdict", ""),
            "company_profile": cp,
            "potential": pot,
            "industry_impact": imp,
            "funding_logic": fl,
            "founder_profile": fp,
            "core_tech": ct,
            "star_team": st,
            "scores": scores,
            "radar_data": radar_data,
            "mermaid_code": mermaid_code,
            "source_article_id": opp.get("source_article_id", ""),
            "created_at": opp.get("created_at", ""),
        }


# ╔══════════════════════════════════════════════════════════════════╗
# ║                       Pipeline 编排                             ║
# ╚══════════════════════════════════════════════════════════════════╝


class Pipeline:
    def __init__(self):
        self.crawler = CrawlerAgent()
        self.cleaner = CleanerAgent()
        self.integrator = IntegratorAgent()
        self.analyst = AnalystAgent()
        self.evaluator = EvaluatorAgent()
        self.reporter = ReporterAgent()

    async def run(self):
        """执行完整流水线，yield SSE 事件（带心跳保活）"""
        agents = [
            ("crawler", self.crawler),
            ("cleaner", self.cleaner),
            ("integrator", self.integrator),
            ("analyst", self.analyst),
            ("evaluator", self.evaluator),
            ("reporter", self.reporter),
        ]

        data = None
        for i, (name, agent) in enumerate(agents):
            yield self._event("agent_start", {"agent": name, "emoji": agent.emoji, "step": i + 1, "total": len(agents)})
            try:
                start = time.time()
                # 用心跳包裹长时间运行的 agent
                task = asyncio.create_task(agent.run(data))
                while not task.done():
                    await asyncio.sleep(3)
                    if not task.done():
                        elapsed_so_far = round(time.time() - start, 1)
                        yield self._event("heartbeat", {"agent": name, "elapsed": elapsed_so_far})
                data = task.result()
                elapsed = round(time.time() - start, 2)
                count = len(data) if isinstance(data, list) else 1
                yield self._event("agent_done", {"agent": name, "emoji": agent.emoji, "elapsed": elapsed, "output_count": count})
            except Exception as e:
                yield self._event("agent_error", {"agent": name, "error": str(e)})
                return

        # 存储结果
        db["articles"] = SAMPLE_ARTICLES
        db["cleaned"] = data  # reporter output is the final data
        db["opportunities"] = data
        db["reports"] = data

        yield self._event("pipeline_done", {
            "total_opportunities": len(data),
            "s_count": sum(1 for r in data if r.get("level") == "S"),
            "a_count": sum(1 for r in data if r.get("level") == "A"),
        })

    def _event(self, event_type: str, data: dict) -> str:
        return f"event: {event_type}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


# ╔══════════════════════════════════════════════════════════════════╗
# ║                        FastAPI 应用                             ║
# ╚══════════════════════════════════════════════════════════════════╝

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"\n{'='*60}")
    print(f"  💰 什么值得投 — 多智能体商机发掘 Demo")
    print(f"  🌐 访问地址: http://localhost:8000")
    print(f"  🤖 LLM 模式: {'Mock（无需API Key）' if USE_MOCK else f'火山方舟 ({OPENAI_MODEL})'}")
    print(f"{'='*60}\n")
    yield

app = FastAPI(title="什么值得投", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
pipeline = Pipeline()


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/api/status")
async def status():
    return {
        "mode": "mock" if USE_MOCK else "llm",
        "model": OPENAI_MODEL if not USE_MOCK else "mock",
        "articles_count": len(db["articles"]),
        "opportunities_count": len(db["opportunities"]),
    }


@app.get("/api/articles")
async def get_articles():
    return SAMPLE_ARTICLES


@app.get("/api/opportunities")
async def get_opportunities():
    return db.get("reports", [])


@app.get("/api/run")
async def run_pipeline():
    """SSE 端点: 运行完整流水线"""
    async def event_stream():
        async for event in pipeline.run():
            yield event
    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ╔══════════════════════════════════════════════════════════════════╗
# ║                          启动入口                               ║
# ╚══════════════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
