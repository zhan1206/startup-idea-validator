# Example: Validating a Startup Idea
# Run: python scripts/startup_validator.py --idea "面向中小企业的 AI 客服系统"

from startup_validator import StartupIdeaValidator

# Example 1: AI Customer Service
idea1 = "面向中小企业的 AI 客服系统"
validator1 = StartupIdeaValidator(idea1)
report1 = validator1.validate(deep_analysis=True)

print(f"想法: {report1.idea}")
print(f"评分: {report1.validation_score}/100")
print(f"建议: {report1.recommendation}")
print(f"市场规模: {report1.market_analysis['tam']}")

# Example 2: EdTech
idea2 = "面向 3-6 岁儿童的在线编程教育平台"
validator2 = StartupIdeaValidator(idea2)
report2 = validator2.validate()

print(f"\n想法: {report2.idea}")
print(f"评分: {report2.validation_score}/100")
print(f"建议: {report2.recommendation}")

# Example 3: B2B SaaS
idea3 = "面向连锁餐饮企业的库存管理系统"
validator3 = StartupIdeaValidator(idea3)
report3 = validator3.validate(deep_analysis=True)

print(f"\n想法: {report3.idea}")
print(f"评分: {report3.validation_score}/100")
print(f"建议: {report3.recommendation}")
print(f"商业模式: {report3.business_model['name']}")
