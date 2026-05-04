# Startup Idea Validator

[English](README.md) | **中文**

> 智能验证创业想法，一键生成可行性报告

自动分析市场规模、竞品格局、技术可行性、商业模式和潜在风险，帮助创业者在投入大量时间前做出明智决策。

## 功能特性

- 📊 **市场规模分析** - TAM/SAM/SOM 三层市场估算
- 👥 **竞品深度扫描** - 识别主要竞品，分析差异化机会
- 💻 **技术可行性评估** - 开发成本、MVP 路径建议
- 💰 **商业模式验证** - Unit Economics、LTV/CAC 分析
- ⚠️ **风险矩阵** - 法律合规、市场、执行风险评估
- 📋 **验证报告** - 生成可执行的验证报告和下一步建议

## 快速开始

### 命令行使用

```bash
# 基本验证
python scripts/startup_validator.py --idea "面向中小企业的 AI 客服系统"

# 深度分析
python scripts/startup_validator.py --idea "你的想法" --deep-analysis

# 指定输出目录
python scripts/startup_validator.py --idea "你的想法" --output ./report
```

### 直接使用

```python
from startup_validator import StartupIdeaValidator

validator = StartupIdeaValidator("你的创业想法")
report = validator.validate(deep_analysis=True)

print(f"评分: {report.validation_score}/100")
print(f"建议: {report.recommendation}")
```

## 示例输出

验证结果包含综合评分（0-100）和详细报告：

```
============================================================
🚀 Startup Idea Validator v1.0.0
============================================================

🔍 Validating idea: 面向中小企业的 AI 客服系统
📊 Identified industry: ai_ml
📈 Market analysis complete
👥 Found 6 competitors
💻 Tech feasibility: high
💰 Recommended model: subscription
⚠️ Identified 5 risks

============================================================
📊 Validation Score: 72/100
💡 Recommendation: 🌟 强烈推荐
============================================================
```

生成的 Markdown 报告包含：

| 章节 | 内容 |
|------|------|
| 综合评分 | 可视化评分条 + 推荐结论 |
| 市场规模 | TAM/SAM/SOM + 增长率 |
| 竞品分析 | 竞品对比表格 |
| 技术评估 | 复杂度、周期、成本 |
| 商业模式 | 盈利模式、Unit Economics |
| 风险矩阵 | 风险等级 + 缓解策略 |
| 下一步 | 5 个可执行的下一步建议 |

## 支持的行业

| 行业 | 关键词示例 |
|------|----------|
| AI/ML | AI、大模型、GPT、LLM、AIGC |
| SaaS | 企业软件、B2B、订阅、CRM |
| 金融科技 | 支付、金融、保险、理财 |
| 电商 | 电商、购物、市场、零售 |
| 教育 | 在线教育、学习、MOOC、培训 |
| 医疗健康 | 医疗、健康、问诊、挂号 |
| 社交 | 社交、社区、IM、通讯 |
| 游戏 | 游戏、手游、电竞 |
| HR科技 | 招聘、HR、人力资源 |
| 物流 | 物流、仓储、配送、供应链 |

## 输出报告示例

```markdown
# 🚀 创业想法验证报告

**想法**: 面向中小企业的 AI 客服系统  
**验证时间**: 2026-05-04  
**行业**: ai_ml  
**版本**: 1.0.0

---

## 📊 综合评分

| 评分 | ██████████░░░░░░░░░░ | 72/100 |
|--------|----------------------|------------------|
| 结论 | 🌟 **强烈推荐** |  |

---

## 🎯 执行摘要

🌟 强烈推荐：这个想法市场潜力大，技术可行，建议立即启动。建议聚焦 MVP 核心功能，快速验证市场反应。

[... 完整报告内容 ...]
```

## 开发

```bash
# 克隆仓库
git clone https://github.com/zhan1206/startup-idea-validator.git
cd startup-idea-validator

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或: venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行验证
python scripts/startup_validator.py --idea "你的创业想法"
```

## 贡献

欢迎贡献代码或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
