#!/usr/bin/env python3
"""
Startup Idea Validator
智能验证创业想法的可行性和市场潜力

功能：市场规模分析、竞品扫描、技术评估、商业模式验证
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict

VERSION = "1.0.0"

# 行业分类和关键词
INDUSTRY_PATTERNS = {
    "saas": {
        "keywords": ["saas", "软件即服务", "订阅", "企业软件", "B2B", "B2B软件", "CRM", "ERP", "项目管理", "协作"],
        "market_data": {"global": 200e9, "growth": 15, "description": "全球企业 SaaS 市场"}
    },
    "fintech": {
        "keywords": ["支付", "金融", "银行", "保险", "理财", "贷款", "信用卡", "支付", "fintech", "金融科技"],
        "market_data": {"global": 312e9, "growth": 12, "description": "全球金融科技市场"}
    },
    "ecommerce": {
        "keywords": ["电商", "购物", "零售", "商城", " marketplace", "二手", "跨境电商", "电商平台"],
        "market_data": {"global": 6.5e12, "growth": 10, "description": "全球电商市场"}
    },
    "edtech": {
        "keywords": ["教育", "在线教育", "学习", "培训", "课程", "MOOC", "edtech", "教育科技", "技能培训"],
        "market_data": {"global": 342e9, "growth": 16, "description": "全球教育科技市场"}
    },
    "healthcare": {
        "keywords": ["医疗", "健康", "问诊", "挂号", "医药", "健康管理", "healthcare", "远程医疗"],
        "market_data": {"global": 517e9, "growth": 15, "description": "全球数字医疗市场"}
    },
    "ai_ml": {
        "keywords": ["AI", "人工智能", "机器学习", "ChatGPT", "大模型", "LLM", "GPT", "AIGC", "生成式AI"],
        "market_data": {"global": 150e9, "growth": 37, "description": "全球 AI 市场"}
    },
    "food_delivery": {
        "keywords": ["外卖", "餐饮", "配送", "生鲜", "买菜", "同城配送", "food delivery"],
        "market_data": {"global": 1.2e12, "growth": 11, "description": "全球食品配送市场"}
    },
    "travel": {
        "keywords": ["旅游", "酒店", "机票", "民宿", "旅行", "预订", "travel", "booking"],
        "market_data": {"global": 9e12, "growth": 8, "description": "全球旅游市场"}
    },
    "social": {
        "keywords": ["社交", "社区", "IM", "即时通讯", "陌生人社交", "social", "dating"],
        "market_data": {"global": 50e9, "growth": 12, "description": "全球社交网络市场"}
    },
    "gaming": {
        "keywords": ["游戏", "手游", "电竞", "休闲游戏", "game", "gaming"],
        "market_data": {"global": 250e9, "growth": 9, "description": "全球游戏市场"}
    },
    "hr_tech": {
        "keywords": ["招聘", "HR", "人力资源", "绩效", "薪酬", "招聘平台", "ATS"],
        "market_data": {"global": 22e9, "growth": 8, "description": "全球 HR Tech 市场"}
    },
    "logistics": {
        "keywords": ["物流", "仓储", "配送", "供应链", "货运", "logistics", "supply chain"],
        "market_data": {"global": 9e12, "growth": 7, "description": "全球物流市场"}
    },
    "realestate": {
        "keywords": ["房地产", "房产", "租房", "买房", "中介", "real estate", "proptech"],
        "market_data": {"global": 4e12, "growth": 6, "description": "全球房产市场"}
    },
    "auto": {
        "keywords": ["汽车", "车后", "二手车", "新能源", "充电", "汽车服务", "auto", "automotive"],
        "market_data": {"global": 8e12, "growth": 5, "description": "全球汽车后市场"}
    },
}

# 竞品数据库（常见竞品）
KNOWN_COMPETITORS = {
    # 企业 SaaS
    "salesforce": {"industry": "saas", "type": "incumbent", "description": "CRM 巨头"},
    "hubspot": {"industry": "saas", "type": "incumbent", "description": "营销自动化"},
    "slack": {"industry": "saas", "type": "incumbent", "description": "企业协作"},
    "notion": {"industry": "saas", "type": "challenger", "description": "文档协作"},
    "figma": {"industry": "saas", "type": "challenger", "description": "设计协作"},
    
    # 金融科技
    "stripe": {"industry": "fintech", "type": "incumbent", "description": "支付基础设施"},
    "antgroup": {"industry": "fintech", "type": "incumbent", "description": "蚂蚁集团"},
    "airwallex": {"industry": "fintech", "type": "challenger", "description": "跨境支付"},
    "pdd": {"industry": "fintech", "type": "challenger", "description": "拼多多支付"},
    
    # 电商
    "alibaba": {"industry": "ecommerce", "type": "incumbent", "description": "阿里巴巴"},
    "jd": {"industry": "ecommerce", "type": "incumbent", "description": "京东"},
    "pinduoduo": {"industry": "ecommerce", "type": "challenger", "description": "拼多多"},
    "shopify": {"industry": "ecommerce", "type": "challenger", "description": "独立站建站"},
    
    # AI
    "openai": {"industry": "ai_ml", "type": "incumbent", "description": "OpenAI"},
    "anthropic": {"industry": "ai_ml", "type": "challenger", "description": "Anthropic Claude"},
    "baidu": {"industry": "ai_ml", "type": "incumbent", "description": "百度文心"},
    "zhipu": {"industry": "ai_ml", "type": "challenger", "description": "智谱 AI"},
    
    # 教育
    "tal": {"industry": "edtech", "type": "incumbent", "description": "好未来"},
    "zuoyebang": {"industry": "edtech", "type": "challenger", "description": "作业帮"},
    "coursera": {"industry": "edtech", "type": "challenger", "description": "Coursera"},
    "udemy": {"industry": "edtech", "type": "challenger", "description": "Udemy"},
    
    # 医疗
    "pingan": {"industry": "healthcare", "type": "incumbent", "description": "平安好医生"},
    "weiyi": {"industry": "healthcare", "type": "challenger", "description": "微医"},
    
    # 社交
    "wechat": {"industry": "social", "type": "incumbent", "description": "微信"},
    "momo": {"industry": "social", "type": "challenger", "description": "陌陌"},
    "soul": {"industry": "social", "type": "challenger", "description": "Soul"},
}

# 商业模式类型
BUSINESS_MODELS = {
    "subscription": {
        "name": "订阅制",
        "description": "月/年订阅，按使用量或功能分层定价",
        "typical_ltv": "12-36个月",
        "pros": ["可预测收入", "客户粘性高", "现金流好"],
        "cons": ["获客成本高", "需要持续提供价值"],
        "examples": ["Netflix", "Slack", "Notion"]
    },
    "transaction": {
        "name": "交易抽佣",
        "description": "按交易金额抽取一定比例佣金",
        "typical_ltv": "单次交易 x 复购率",
        "pros": ["规模化后利润高", "轻资产"],
        "cons": ["需要大量流量", "利润薄"],
        "examples": ["美团", "滴滴", "Airbnb"]
    },
    "freemium": {
        "name": "免费增值",
        "description": "基础功能免费，高级功能付费",
        "typical_ltv": "5-10%免费用户转化",
        "pros": ["病毒式增长", "获客成本低"],
        "cons": ["转化率低", "服务器成本高"],
        "examples": ["Dropbox", "Slack", "Spotify"]
    },
    "marketplace": {
        "name": "双边市场",
        "description": "连接供需双方，撮合交易",
        "typical_ltv": "双边网络效应",
        "pros": ["网络效应", "护城河深"],
        "cons": ["冷启动困难", "鸡生蛋问题"],
        "examples": ["淘宝", "Uber", "Airbnb"]
    },
    "saas_api": {
        "name": "API/开发者收费",
        "description": "按 API 调用次数或开发者数量收费",
        "typical_ltv": "API 使用量增长",
        "pros": ["边际成本低", "开发者生态"],
        "cons": ["定价难", "竞争激烈"],
        "examples": ["Stripe", "Twilio", "OpenAI"]
    },
    "hardware": {
        "name": "硬件销售",
        "description": "销售硬件设备",
        "typical_ltv": "一次性 + 耗材/服务",
        "pros": ["客单价高", "现金流好"],
        "cons": ["重资产", "库存风险"],
        "examples": ["Apple", "大疆", "小米"]
    },
    "advertising": {
        "name": "广告变现",
        "description": "免费服务 + 广告收入",
        "typical_ltv": "用户注意力 x 广告 CPM",
        "pros": ["规模化快", "用户门槛低"],
        "cons": ["用户体验差", "广告主依赖"],
        "examples": ["Google", "Facebook", "抖音"]
    },
    "data": {
        "name": "数据服务",
        "description": "聚合数据，提供洞察或数据服务",
        "typical_ltv": "数据价值 x 使用频率",
        "pros": ["毛利率高", "护城河深"],
        "cons": ["合规风险", "数据获取成本高"],
        "examples": ["Bloomberg", "同花顺", "天眼查"]
    },
}

# 风险类型
RISK_TYPES = {
    "market": {
        "name": "市场风险",
        "examples": ["市场太小", "需求不真实", "时机太早/太晚"]
    },
    "competition": {
        "name": "竞争风险",
        "examples": ["巨头入场", "价格战", "差异化不足"]
    },
    "technical": {
        "name": "技术风险",
        "examples": ["技术不可行", "难以规模化", "数据瓶颈"]
    },
    "regulatory": {
        "name": "监管风险",
        "examples": ["合规要求", "牌照门槛", "政策变化"]
    },
    "capital": {
        "name": "资金风险",
        "examples": ["烧钱太快", "融资困难", "单位经济不健康"]
    },
    "team": {
        "name": "团队风险",
        "examples": ["创始人能力", "核心人才流失", "执行力不足"]
    },
    "customer": {
        "name": "客户风险",
        "examples": ["获客成本高", "留存率低", "客户集中度"]
    },
    "legal": {
        "name": "法律风险",
        "examples": ["知识产权", "隐私合规", "合同纠纷"]
    },
}

# 技术复杂度评估
TECH_COMPLEXITY = {
    "low": {
        "name": "低复杂度",
        "dev_time": "1-3个月",
        "team_size": "1-3人",
        "cost_estimate": "$5,000-20,000",
        "examples": ["信息展示型", "简单表单", "内容管理"]
    },
    "medium": {
        "name": "中复杂度",
        "dev_time": "3-6个月",
        "team_size": "3-6人",
        "cost_estimate": "$20,000-100,000",
        "examples": ["社区产品", "电商平台", "SaaS 工具"]
    },
    "high": {
        "name": "高复杂度",
        "dev_time": "6-12个月",
        "team_size": "6-15人",
        "cost_estimate": "$100,000-500,000",
        "examples": ["AI 应用", "实时通讯", "复杂交易系统"]
    },
    "very_high": {
        "name": "极高复杂度",
        "dev_time": "12+个月",
        "team_size": "15+人",
        "cost_estimate": "$500,000+",
        "examples": ["操作系统", "数据库", "底层基础设施"]
    },
}

# 中国关键词
CN_INDICATORS = {
    "market_name": "中国市场",
    "currency": "¥",
    "platforms": ["微信", "抖音", "小红书", "B站", "知乎", "微博"],
    "payment": ["微信支付", "支付宝"],
    "regulatory": ["网信办", "工信部", "银保监会", "证监会"],
}

@dataclass
class Competitor:
    name: str
    industry: str
    comp_type: str  # incumbent, challenger
    description: str
    strengths: str
    weaknesses: str
    url: str = ""

@dataclass
class Risk:
    risk_type: str
    level: str  # high, medium, low
    description: str
    mitigation: str

@dataclass
class ValidationReport:
    idea: str
    timestamp: str
    version: str
    industry: str
    market_analysis: Dict
    competitors: List[Dict]
    tech_feasibility: Dict
    business_model: Dict
    risks: List[Dict]
    validation_score: float
    recommendation: str
    next_steps: List[str]


class StartupIdeaValidator:
    """创业想法验证器"""
    
    def __init__(self, idea: str):
        self.idea = idea
        self.idea_lower = idea.lower()
        self.report: Optional[ValidationReport] = None
    
    def validate(self, deep_analysis: bool = False) -> ValidationReport:
        """执行完整的想法验证"""
        print(f"🔍 Validating idea: {self.idea}")
        
        # 1. 识别行业
        industry = self._identify_industry()
        print(f"📊 Identified industry: {industry}")
        
        # 2. 市场规模分析
        market_analysis = self._analyze_market(industry)
        print(f"📈 Market analysis complete")
        
        # 3. 竞品分析
        competitors = self._analyze_competitors(industry, deep_analysis)
        print(f"👥 Found {len(competitors)} competitors")
        
        # 4. 技术可行性
        tech_feasibility = self._evaluate_tech()
        print(f"💻 Tech feasibility: {tech_feasibility['complexity']}")
        
        # 5. 商业模式评估
        business_model = self._evaluate_business_model()
        print(f"💰 Recommended model: {business_model['type']}")
        
        # 6. 风险评估
        risks = self._assess_risks(industry, competitors, tech_feasibility)
        print(f"⚠️ Identified {len(risks)} risks")
        
        # 7. 计算综合评分
        score = self._calculate_score(market_analysis, competitors, tech_feasibility, risks)
        
        # 8. 生成建议
        recommendation = self._generate_recommendation(score, risks)
        next_steps = self._generate_next_steps(score, industry)
        
        self.report = ValidationReport(
            idea=self.idea,
            timestamp=datetime.now().isoformat(),
            version=VERSION,
            industry=industry,
            market_analysis=market_analysis,
            competitors=[asdict(c) for c in competitors],
            tech_feasibility=tech_feasibility,
            business_model=business_model,
            risks=[asdict(r) for r in risks],
            validation_score=score,
            recommendation=recommendation,
            next_steps=next_steps
        )
        
        return self.report
    
    def _identify_industry(self) -> str:
        """识别想法所属行业"""
        for industry, config in INDUSTRY_PATTERNS.items():
            for keyword in config["keywords"]:
                if keyword.lower() in self.idea_lower:
                    return industry
        return "general"
    
    def _analyze_market(self, industry: str) -> Dict:
        """分析市场规模"""
        if industry == "general":
            return {
                "tam": "未知",
                "sam": "未知",
                "som": "未知",
                "growth_rate": "未知",
                "analysis": "需要更多信息来评估市场规模"
            }
        
        config = INDUSTRY_PATTERNS.get(industry, {})
        market_data = config.get("market_data", {})
        description = market_data.get("description", "")
        
        # 估算 TAM/SAM/SOM（简化模型）
        tam = market_data.get("global", 0)
        sam = tam * 0.1  # 假设可服务市场为总市场的 10%
        som = sam * 0.1  # 假设可获得市场为可服务市场的 10%
        growth = market_data.get("growth", 10)
        
        # 检测是否中国特有
        is_cn_focused = any(cn_word in self.idea_lower for cn_word in 
                           ["中国", "中文", "微信", "抖音", "小红书", "国内"])
        
        if is_cn_focused:
            tam = tam * 0.15  # 中国市场约占全球 15%
            sam = tam * 0.3
            som = sam * 0.1
            market_name = "中国市场规模"
        else:
            market_name = "全球市场规模"
        
        return {
            "industry": config.get("keywords", ["通用"])[0],
            "description": description,
            "market_name": market_name,
            "tam": self._format_money(tam),
            "sam": self._format_money(sam),
            "som": self._format_money(som),
            "growth_rate": f"{growth}%",
            "analysis": self._generate_market_analysis(industry, tam, sam, som)
        }
    
    def _format_money(self, amount: float) -> str:
        """格式化金额显示"""
        if amount >= 1e12:
            return f"${amount/1e12:.1f}万亿"
        elif amount >= 1e9:
            return f"${amount/1e9:.1f}亿"
        elif amount >= 1e6:
            return f"${amount/1e6:.1f}百万"
        else:
            return f"${amount:,.0f}"
    
    def _generate_market_analysis(self, industry: str, tam: float, sam: float, som: float) -> str:
        """生成市场分析文字"""
        analyses = {
            "ai_ml": f"AI市场正在爆发式增长，{self._format_money(tam)}的总市场中，预计{self._format_money(sam)}可在中期服务，初期可触及约{self._format_money(som)}。",
            "saas": f"企业SaaS市场持续增长，{self._format_money(tam)}的总市场中，中小企业细分约{self._format_money(sam)}，可获得市场约{self._format_money(som)}。",
            "ecommerce": f"电商市场体量巨大，{self._format_money(tam)}的盘子中，垂直领域约{self._format_money(sam)}，新进入者初期可分得约{self._format_money(som)}。",
            "fintech": f"金融科技监管趋严但机会仍在，{self._format_money(tam)}市场中，{self._format_money(sam)}为可服务市场，初期目标约{self._format_money(som)}。",
        }
        return analyses.get(industry, f"市场容量{self._format_money(tam)}，可服务市场{self._format_money(sam)}，可获得市场{self._format_money(som)}。")
    
    def _analyze_competitors(self, industry: str, deep: bool) -> List[Competitor]:
        """分析竞品"""
        competitors = []
        
        # 从已知竞品库中匹配
        for name, info in KNOWN_COMPETITORS.items():
            if info["industry"] == industry:
                competitors.append(Competitor(
                    name=name,
                    industry=info["industry"],
                    comp_type=info["type"],
                    description=info["description"],
                    strengths=self._get_competitor_strengths(name),
                    weaknesses=self._get_competitor_weaknesses(name),
                    url=f"https://{name}.com"
                ))
        
        # 根据想法特点添加建议关注的竞品
        idea_competitors = self._find_idea_competitors(industry)
        competitors.extend(idea_competitors)
        
        return competitors[:10]  # 限制返回数量
    
    def _get_competitor_strengths(self, name: str) -> str:
        strengths = {
            "salesforce": "品牌认知度、市场主导地位、生态系统",
            "hubspot": "易用性、入门门槛低、营销自动化",
            "slack": "用户粘性、集成生态",
            "notion": "灵活性、模板丰富、社区驱动",
            "figma": "实时协作、设计师生态",
            "stripe": "开发者体验、全球覆盖",
            "openai": "技术领先、品牌效应、GPT生态",
            "shopify": "独立站生态、应用市场",
        }
        return strengths.get(name, "品牌、用户基础、资金")
    
    def _get_competitor_weaknesses(self, name: str) -> str:
        weaknesses = {
            "salesforce": "复杂、昂贵、用户体验差",
            "hubspot": "定价争议、功能限制",
            "slack": "搜索功能弱、非企业场景",
            "notion": "性能问题、协作功能弱",
            "stripe": "费率、区域限制、合规复杂",
            "openai": "成本高、延迟、幻觉问题",
            "shopify": "对平台依赖、利润率薄",
        }
        return weaknesses.get(name, "大公司病、创新慢、定制化差")
    
    def _find_idea_competitors(self, industry: str) -> List[Competitor]:
        """根据想法特点添加潜在竞品"""
        competitors = []
        
        # 检测目标用户群
        if any(kw in self.idea_lower for kw in ["中小企业", "SMB", "小公司"]):
            competitors.append(Competitor(
                name="feishu/飞书",
                industry=industry,
                comp_type="incumbent",
                description="字节跳动企业协作套件",
                strengths="免费、集成好、年轻用户",
                weaknesses="大企业功能弱"
            ))
        
        if any(kw in self.idea_lower for kw in ["AI", "智能", "大模型"]):
            competitors.append(Competitor(
                name="coze扣子",
                industry=industry,
                comp_type="challenger",
                description="字节跳动 AI 应用开发平台",
                strengths="免费、字节生态",
                weaknesses="生态封闭"
            ))
        
        return competitors
    
    def _evaluate_tech(self) -> Dict:
        """评估技术可行性"""
        tech_score = 0
        complexity = "low"
        factors = []
        
        # AI 相关特性
        if any(kw in self.idea_lower for kw in ["AI", "大模型", "GPT", "LLM", "生成"]):
            tech_score += 20
            complexity = "high"
            factors.append("需要大模型 API 集成或微调")
        
        # 实时功能
        if any(kw in self.idea_lower for kw in ["实时", "聊天", "IM", "直播", "视频"]):
            tech_score += 15
            if complexity == "low":
                complexity = "medium"
            factors.append("需要 WebSocket/实时通信技术支持")
        
        # 支付相关
        if any(kw in self.idea_lower for kw in ["支付", "金融", "交易", "电商"]):
            tech_score += 15
            if complexity != "very_high":
                complexity = "medium" if complexity == "low" else complexity
            factors.append("涉及支付合规和资金安全")
        
        # 移动端
        if any(kw in self.idea_lower for kw in ["APP", "移动", "小程序", "iOS", "Android"]):
            tech_score += 10
            if complexity == "low":
                complexity = "medium"
            factors.append("需要多端开发支持")
        
        # 社交/社区
        if any(kw in self.idea_lower for kw in ["社交", "社区", "UGC", "内容创作"]):
            tech_score += 10
            factors.append("需要内容审核和反垃圾机制")
        
        # 数据分析
        if any(kw in self.idea_lower for kw in ["数据", "分析", "BI", "报表", "洞察"]):
            tech_score += 10
            factors.append("需要数据管道和可视化能力")
        
        # IoT/硬件
        if any(kw in self.idea_lower for kw in ["IoT", "硬件", "设备", "传感器"]):
            tech_score += 25
            complexity = "very_high"
            factors.append("涉及硬件研发和供应链管理")
        
        # 没有特殊技术要求
        if tech_score == 0:
            complexity = "low"
            factors.append("技术栈成熟，可快速开发")
        
        tech_config = TECH_COMPLEXITY.get(complexity, TECH_COMPLEXITY["medium"])
        
        return {
            "complexity": complexity,
            "complexity_name": tech_config["name"],
            "estimated_time": tech_config["dev_time"],
            "team_size": tech_config["team_size"],
            "estimated_cost": tech_config["cost_estimate"],
            "factors": factors,
            "mvp_path": self._suggest_mvp_path(complexity)
        }
    
    def _suggest_mvp_path(self, complexity: str) -> str:
        """建议 MVP 开发路径"""
        paths = {
            "low": "使用 SaaS 服务（如 Supabase/Firebase）+ Next.js/React，1-2个月完成 MVP",
            "medium": "后端 Django/FastAPI + 前端 React/Vue，分阶段交付核心功能",
            "high": "核心功能独立开发，其他功能用第三方服务集成，控制研发成本",
            "very_high": "考虑从细分场景切入，先用人工+工具验证需求，再逐步自动化"
        }
        return paths.get(complexity, paths["medium"])
    
    def _evaluate_business_model(self) -> Dict:
        """评估商业模式"""
        # 根据想法特点推荐商业模式
        model_type = "subscription"
        
        if any(kw in self.idea_lower for kw in ["交易", "电商", "市场", "撮合"]):
            model_type = "marketplace"
        elif any(kw in self.idea_lower for kw in ["免费", "社交", "内容", "工具"]):
            model_type = "freemium"
        elif any(kw in self.idea_lower for kw in ["API", "开发者", "平台"]):
            model_type = "saas_api"
        elif any(kw in self.idea_lower for kw in ["广告", "流量"]):
            model_type = "advertising"
        elif any(kw in self.idea_lower for kw in ["硬件", "设备", "IoT"]):
            model_type = "hardware"
        
        model = BUSINESS_MODELS.get(model_type, BUSINESS_MODELS["subscription"])
        
        return {
            "type": model_type,
            "name": model["name"],
            "description": model["description"],
            "typical_ltv": model["typical_ltv"],
            "pros": model["pros"],
            "cons": model["cons"],
            "examples": model["examples"],
            "unit_economics": self._estimate_unit_economics(model_type)
        }
    
    def _estimate_unit_economics(self, model_type: str) -> Dict:
        """估算单位经济学"""
        estimates = {
            "subscription": {"cac": "$50-200", "ltv": "$200-1000", "ltv_cac": "3-5x", "payback": "3-12月"},
            "marketplace": {"cac": "$20-100", "ltv": "GMV的10-30%", "take_rate": "5-15%", "payback": "3-6月"},
            "freemium": {"cac": "$5-30", "ltv": "$50-500", "ltv_cac": "2-5x", "payback": "1-6月"},
            "saas_api": {"cac": "$100-500", "ltv": "$500-5000", "ltv_cac": "3-10x", "payback": "6-18月"},
            "advertising": {"cac": "$1-10", "ltv": "$5-50", "ltv_cac": "3-10x", "payback": "1-3月"},
        }
        return estimates.get(model_type, {"cac": "未知", "ltv": "未知", "ltv_cac": "未知", "payback": "未知"})
    
    def _assess_risks(self, industry: str, competitors: List[Competitor], 
                     tech: Dict) -> List[Risk]:
        """评估风险"""
        risks = []
        
        # 市场风险
        if industry == "general":
            risks.append(Risk(
                risk_type="market",
                level="high",
                description="市场定位不明确，需要进一步分析",
                mitigation="深入调研目标用户和市场需求"
            ))
        
        # 竞争风险
        incumbents = [c for c in competitors if c.comp_type == "incumbent"]
        if incumbents:
            risks.append(Risk(
                risk_type="competition",
                level="high",
                description=f"面临 {len(incumbents)} 个行业巨头的竞争压力",
                mitigation="寻找差异化切入点，聚焦细分用户群或独特价值主张"
            ))
        
        # 技术风险
        if tech["complexity"] in ["high", "very_high"]:
            risks.append(Risk(
                risk_type="technical",
                level="medium" if tech["complexity"] == "high" else "high",
                description=f"技术复杂度较高（{tech['complexity_name']}），研发周期长",
                mitigation="从 MVP 开始，控制研发成本，考虑技术合作"
            ))
        
        # 监管风险
        if industry in ["fintech", "healthcare"]:
            risks.append(Risk(
                risk_type="regulatory",
                level="high",
                description=f"{industry} 行业面临严格监管，需要相关资质",
                mitigation="提前了解监管要求，准备合规方案，必要时寻求法律顾问"
            ))
        
        # 中国特有监管
        if any(kw in self.idea_lower for kw in ["内容", "社区", "社交", "新闻", "媒体"]):
            risks.append(Risk(
                risk_type="regulatory",
                level="medium",
                description="内容平台需注意网络安全、数据合规、内容审核",
                mitigation="接入内容审核服务，建立举报机制，关注政策变化"
            ))
        
        # 资金风险
        if tech["complexity"] in ["high", "very_high"]:
            risks.append(Risk(
                risk_type="capital",
                level="medium",
                description=f"初期研发成本较高（{tech['estimated_cost']}）",
                mitigation="准备足够的启动资金，考虑政府补贴或早期投资"
            ))
        
        # 差异化风险
        risks.append(Risk(
            risk_type="differentiation",
            level="medium",
            description="需要找到明确的差异化优势，避免陷入同质竞争",
            mitigation="深入分析竞品弱点，找到未满足的需求点"
        ))
        
        return risks
    
    def _calculate_score(self, market: Dict, competitors: List[Competitor],
                        tech: Dict, risks: List[Risk]) -> float:
        """计算综合评分 (0-100)"""
        score = 50  # 基础分
        
        # 市场规模加分
        if "万亿" in market.get("tam", ""):
            score += 20
        elif "亿" in market.get("tam", ""):
            score += 15
        elif market.get("tam") != "未知":
            score += 10
        
        # 增长潜力加分
        growth_str = market.get("growth_rate", "0%").replace("%", "").replace("+", "")
        try:
            growth = int(growth_str)
            if growth >= 20:
                score += 15
            elif growth >= 10:
                score += 10
            else:
                score += 5
        except:
            pass
        
        # 差异化机会加分
        if len(competitors) < 5:
            score += 10  # 竞争不激烈
        elif not any(c.comp_type == "incumbent" for c in competitors):
            score += 15  # 没有巨头
        
        # 技术可行性加分/减分
        if tech["complexity"] == "low":
            score += 10
        elif tech["complexity"] == "medium":
            score += 5
        elif tech["complexity"] in ["high", "very_high"]:
            score -= 10
        
        # 风险调整
        high_risks = len([r for r in risks if r.level == "high"])
        medium_risks = len([r for r in risks if r.level == "medium"])
        score -= high_risks * 8
        score -= medium_risks * 3
        
        return max(0, min(100, score))
    
    def _generate_recommendation(self, score: float, risks: List[Risk]) -> str:
        """生成建议"""
        if score >= 75:
            return "🌟 强烈推荐：这个想法市场潜力大，技术可行，建议立即启动。建议聚焦 MVP 核心功能，快速验证市场反应。"
        elif score >= 60:
            return "✅ 推荐：这个想法有一定潜力，但需要找到明确的差异化切入点。建议做小规模用户测试后再加大投入。"
        elif score >= 45:
            return "⚠️ 谨慎：市场或竞争存在不确定性，建议深入调研后再决定。可以考虑先做 POC 验证核心假设。"
        else:
            high_risks = [r for r in risks if r.level == "high"]
            risk_summary = "、".join([r.risk_type for r in high_risks[:2]])
            return f"❌ 暂不推荐：主要风险在于{risk_summary}。建议重新思考方向或等待更好的时机。"
    
    def _generate_next_steps(self, score: float, industry: str) -> List[str]:
        """生成下一步行动建议"""
        steps = []
        
        if score >= 60:
            steps = [
                "1. 定义 MVP：列出 3 个核心功能，避免功能蔓延",
                "2. 用户访谈：找 10 个潜在用户深度访谈，验证需求真伪",
                "3. 竞品体验：亲自使用竞品 1 周，记录痛点和机会",
                "4. 构建原型：用 Figma/PPT 做原型，收集反馈",
                "5. 快速验证：用人工或简易工具验证核心价值假设"
            ]
        else:
            steps = [
                "1. 重新调研：深入了解市场规模和竞争格局",
                "2. 缩小范围：考虑聚焦更细分的人群或场景",
                "3. 差异化思考：明确为什么是你来做这件事",
                "4. 寻找联合创始人：补充技术和行业经验短板"
            ]
        
        return steps
    
    def export_json(self) -> str:
        """导出为 JSON"""
        if not self.report:
            return "{}"
        return json.dumps(asdict(self.report), ensure_ascii=False, indent=2)


def write_markdown_report(report: ValidationReport, output_path: Path):
    """生成 Markdown 报告"""
    md = f"""# 🚀 创业想法验证报告

**想法**: {report.idea}  
**验证时间**: {report.timestamp}  
**行业**: {report.industry}  
**版本**: {report.version}

---

## 📊 综合评分

"""
    
    # 评分可视化
    score = report.validation_score
    bar_length = int(score / 5)
    bar = "█" * bar_length + "░" * (20 - bar_length)
    
    if score >= 75:
        score_emoji = "🌟"
        score_text = "强烈推荐"
    elif score >= 60:
        score_emoji = "✅"
        score_text = "推荐"
    elif score >= 45:
        score_emoji = "⚠️"
        score_text = "谨慎"
    else:
        score_emoji = "❌"
        score_text = "暂不推荐"
    
    md += f"""| 评分 | {bar} | {score}/100 |
|--------|{'-' * 22}|--------------|
| 结论 | {score_emoji} **{score_text}** |  |

---

## 🎯 执行摘要

{report.recommendation}

"""
    
    md += f"""---

## 📈 市场规模分析

| 指标 | 数值 |
|------|------|
| 市场描述 | {report.market_analysis.get('description', 'N/A')} |
| TAM（总市场） | {report.market_analysis.get('tam', 'N/A')} |
| SAM（可服务市场） | {report.market_analysis.get('sam', 'N/A')} |
| SOM（可获得市场） | {report.market_analysis.get('som', 'N/A')} |
| 增长率 | {report.market_analysis.get('growth_rate', 'N/A')} |

**分析**: {report.market_analysis.get('analysis', 'N/A')}

"""
    
    # 竞品分析
    md += f"""---

## 👥 竞品分析

"""
    
    if report.competitors:
        md += "| 竞品 | 类型 | 描述 | 优势 | 劣势 |\n"
        md += "|------|------|------|------|------|\n"
        for comp in report.competitors[:8]:
            md += f"| {comp['name']} | {comp['comp_type']} | {comp['description']} | {comp['strengths']} | {comp['weaknesses']} |\n"
    else:
        md += "未发现明显竞品，这是一个潜在的机会点。\n"
    
    # 技术可行性
    md += f"""

---

## 💻 技术可行性评估

| 维度 | 评估 |
|------|------|
| 复杂度 | {report.tech_feasibility.get('complexity_name', 'N/A')} |
| 开发周期 | {report.tech_feasibility.get('estimated_time', 'N/A')} |
| 团队规模 | {report.tech_feasibility.get('team_size', 'N/A')} |
| 预估成本 | {report.tech_feasibility.get('estimated_cost', 'N/A')} |

**技术因素**:
"""
    for factor in report.tech_feasibility.get('factors', []):
        md += f"- {factor}\n"
    
    md += f"""
**MVP 开发建议**: {report.tech_feasibility.get('mvp_path', 'N/A')}

"""
    
    # 商业模式
    bm = report.business_model
    md += f"""---

## 💰 商业模式评估

| 维度 | 内容 |
|------|------|
| 模式类型 | {bm.get('name', 'N/A')} |
| 模式描述 | {bm.get('description', 'N/A')} |
| 典型 LTV | {bm.get('typical_ltv', 'N/A')} |

**优点**: {', '.join(bm.get('pros', []))}

**缺点**: {', '.join(bm.get('cons', []))}

**代表案例**: {', '.join(bm.get('examples', []))}

**单位经济学**:
- CAC: {bm.get('unit_economics', {}).get('cac', 'N/A')}
- LTV: {bm.get('unit_economics', {}).get('ltv', 'N/A')}
- LTV/CAC: {bm.get('unit_economics', {}).get('ltv_cac', 'N/A')}
- 回本周期: {bm.get('unit_economics', {}).get('payback', 'N/A')}

"""
    
    # 风险评估
    md += """---

## ⚠️ 风险矩阵

"""
    
    if report.risks:
        md += "| 风险类型 | 等级 | 描述 | 缓解策略 |\n"
        md += "|----------|------|------|----------|\n"
        for risk in report.risks:
            level_emoji = "🔴" if risk['level'] == 'high' else ("🟡" if risk['level'] == 'medium' else "🟢")
            md += f"| {RISK_TYPES.get(risk['risk_type'], {}).get('name', risk['risk_type'])} | {level_emoji} {risk['level']} | {risk['description']} | {risk['mitigation']} |\n"
    
    # 下一步
    md += """

---

## 📋 下一步行动

"""
    for step in report.next_steps:
        md += f"{step}\n"
    
    md += f"""

---

## 📚 参考资源

- [如何做竞品分析](https://www.google.com/search?q=competitive+analysis+methodology)
- [创业想法验证清单](https://www.google.com/search?q=startup+idea+validation+checklist)
- [商业模式画布](https://www.google.com/search?q=business+model+canvas)

---

*报告由 Startup Idea Validator v{VERSION} 生成*
"""
    
    (output_path / 'startup-validation-report.md').write_text(md, encoding='utf-8')
    print(f"✅ Markdown report: {output_path / 'startup-validation-report.md'}")


def main():
    parser = argparse.ArgumentParser(
        description='Startup Idea Validator - 智能验证创业想法的可行性和市场潜力',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 基本验证
  python startup_validator.py --idea "面向中小企业的 AI 客服系统"
  
  # 深度分析
  python startup_validator.py --idea "你的想法" --deep-analysis
  
  # 输出到指定目录
  python startup_validator.py --idea "你的想法" --output ./report
        """
    )
    parser.add_argument('--idea', required=True, help='要验证的创业想法')
    parser.add_argument('--deep-analysis', action='store_true', help='深度分析竞品')
    parser.add_argument('--output', default='./startup-validation', help='输出目录')
    
    args = parser.parse_args()
    
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"🚀 Startup Idea Validator v{VERSION}")
    print(f"{'='*60}\n")
    
    validator = StartupIdeaValidator(args.idea)
    report = validator.validate(deep_analysis=args.deep_analysis)
    
    # 输出 Markdown 报告
    write_markdown_report(report, output_path)
    
    # 保存 JSON
    json_path = output_path / 'validation-report.json'
    json_path.write_text(validator.export_json(), encoding='utf-8')
    print(f"✅ JSON report: {json_path}")
    
    print(f"\n{'='*60}")
    print(f"📊 Validation Score: {report.validation_score}/100")
    print(f"💡 Recommendation: {report.recommendation}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
