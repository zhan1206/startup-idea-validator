# Startup Idea Validator

[中文](README_zh.md) | **English**

> Intelligently validate startup ideas, generate feasibility reports in one click

Automatically analyze market size, competitive landscape, technical feasibility, business models, and potential risks to help entrepreneurs make informed decisions before investing significant time.

## Features

- 📊 **Market Size Analysis** - TAM/SAM/SOM three-tier market estimation
- 👥 **Competitor Deep Scan** - Identify major competitors, analyze differentiation opportunities
- 💻 **Technical Feasibility** - Development cost, MVP path recommendations
- 💰 **Business Model Validation** - Unit Economics, LTV/CAC analysis
- ⚠️ **Risk Matrix** - Legal compliance, market, execution risk assessment
- 📋 **Validation Report** - Generate actionable validation report and next-step recommendations

## Quick Start

### Command Line Usage

```bash
# Basic validation
python scripts/startup_validator.py --idea "AI-powered customer service system for SMEs"

# Deep analysis
python scripts/startup_validator.py --idea "your idea" --deep-analysis

# Specify output directory
python scripts/startup_validator.py --idea "your idea" --output ./report
```

### Direct Usage

```python
from startup_validator import StartupIdeaValidator

validator = StartupIdeaValidator("your startup idea")
report = validator.validate(deep_analysis=True)

print(f"Score: {report.validation_score}/100")
print(f"Recommendation: {report.recommendation}")
```

## Example Output

Validation results include a comprehensive score (0-100) and detailed report:

```
============================================================
🚀 Startup Idea Validator v1.0.0
============================================================

🔍 Validating idea: AI-powered customer service system for SMEs
📊 Identified industry: ai_ml
📈 Market analysis complete
👥 Found 6 competitors
💻 Tech feasibility: high
💰 Recommended model: subscription
⚠️ Identified 5 risks

============================================================
📊 Validation Score: 72/100
💡 Recommendation: 🌟 Strongly Recommended
============================================================
```

Generated Markdown report includes:

| Section | Content |
|---------|---------|
| Comprehensive Score | Visual score bar + recommendation |
| Market Size | TAM/SAM/SOM + growth rate |
| Competitor Analysis | Competitor comparison table |
| Technical Assessment | Complexity, timeline, cost |
| Business Model | Profit model, Unit Economics |
| Risk Matrix | Risk level + mitigation strategies |
| Next Steps | 5 actionable next-step recommendations |

## Supported Industries

| Industry | Keyword Examples |
|----------|-------------------|
| AI/ML | AI, big model, GPT, LLM, AIGC |
| SaaS | enterprise software, B2B, subscription, CRM |
| FinTech | payment, finance, insurance, wealth management |
| E-commerce | ecommerce, shopping, marketplace, retail |
| Education | online education, learning, MOOC, training |
| Healthcare | medical, health, consultation, registration |
| Social | social, community, IM, communication |
| Gaming | gaming, mobile games, esports |
| HR Tech | recruitment, HR, human resources |
| Logistics | logistics, warehousing, delivery, supply chain |

## Output Report Example

```markdown
# 🚀 Startup Idea Validation Report

**Idea**: AI-powered customer service system for SMEs  
**Validation Time**: 2026-05-04  
**Industry**: ai_ml  
**Version**: 1.0.0

---

## 📊 Comprehensive Score

| Score | ██████████░░░░░░░░ | 72/100 |
|-------|----------------------|--------------|
| Conclusion | 🌟 **Strongly Recommended** |  |

---

## 🎯 Executive Summary

🌟 Strongly Recommended: This idea has great market potential and is technically 
[... full report content ...]
```

## Development

```bash
# Clone repository
git clone https://github.com/zhan1206/startup-idea-validator.git
cd startup-idea-validator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run validation
python scripts/startup_validator.py --idea "your startup idea"
```

## Contributing

Contributions welcome! 

1. Fork this repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
