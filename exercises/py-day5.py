#!/usr/bin/env python3
"""
信息抽取器 - 从产品评论中提取结构化信息

任务要求：
- 输入：一段产品评论文字
- 输出：结构化 JSON，包含 sentiment(positive/neutral/negative), keywords(list), score(1-5)
- 使用 Pydantic 定义输出模型，调用 LLM(deepseek) 强制输出该格式

已实现功能：
1. 使用 Pydantic 定义严格的输出模型 (ReviewAnalysis)
2. 集成 DeepSeek API 进行智能分析
3. 提供完整的错误处理和验证
4. 包含示例和测试代码

使用方法：
1. 设置环境变量 DEEPSEEK_API_KEY
2. 运行 python info_extractor.py 查看示例
3. 或导入 InfoExtractor 类到自己的项目中使用

文件结构：
- info_extractor.py: 主实现文件
- test_extractor.py: 测试文件
- requirements.txt: 依赖列表
"""

import os
import sys

# 添加项目根目录到Python路径，以便导入info_extractor模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from info_extractor import InfoExtractor, ReviewAnalysis, Sentiment

def demonstrate_extractor():
    """演示信息抽取器的使用"""
    print("信息抽取器演示")
    print("=" * 60)
    
    # 示例评论
    reviews = [
        "这款手机真的太棒了！拍照效果清晰，电池续航超长，运行速度飞快。性价比很高，强烈推荐！",
        "产品质量一般，外观还可以但功能不够完善。客服态度不错，但产品本身有待改进。",
        "非常失望！买来一周就出现故障，售后服务也很差，完全不值这个价格。",
        "物美价廉，功能齐全，操作简单，非常适合初学者使用。",
        "中规中矩的产品，没有什么特别突出的优点，但也没有什么明显的缺点。"
    ]
    
    # 检查API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not api_key:
        print("未设置 DEEPSEEK_API_KEY 环境变量")
        print("\n请先设置环境变量：")
        print("Windows: set DEEPSEEK_API_KEY=你的API密钥")
        print("Linux/Mac: export DEEPSEEK_API_KEY='你的API密钥'")
        print("\n获取API密钥: https://platform.deepseek.com/api_keys")
        print("\n示例输出格式：")
        
        # 显示示例输出
        example = ReviewAnalysis(
            sentiment=Sentiment.POSITIVE,
            keywords=["拍照效果", "电池续航", "运行速度", "性价比", "推荐"],
            score=5
        )
        print(example.model_dump_json(indent=2))
        return
    
    try:
        # 创建信息抽取器
        extractor = InfoExtractor(api_key=api_key)
        
        print(f"使用API密钥: {api_key[:10]}...")
        print(f"可用模型: deepseek-chat")
        print()
        
        # 分析每条评论
        for i, review in enumerate(reviews, 1):
            print(f"评论 {i}: {review[:50]}...")
            print("-" * 40)
            
            try:
                # 提取信息
                analysis = extractor.extract(review)
                
                # 显示结果
                print(f"情感分析: {analysis.sentiment.value}")
                print(f"关键词: {', '.join(analysis.keywords)}")
                print(f"评分: {analysis.score}/5")
                print(f"完整JSON输出:")
                print(analysis.model_dump_json(indent=2))
                print()
                
            except Exception as e:
                print(f"分析失败: {e}")
                print()
                
    except Exception as e:
        print(f"初始化失败: {e}")
        print("\n可能的原因：")
        print("1. API密钥无效")
        print("2. 网络连接问题")
        print("3. API服务不可用")


def quick_usage_example():
    """快速使用示例"""
    print("\n" + "=" * 60)
    print("快速使用示例")
    print("=" * 60)
    
    print("""
# 方法1: 直接运行示例
# python info_extractor.py

# 方法2: 在代码中使用
from info_extractor import InfoExtractor

# 初始化（会自动读取环境变量 DEEPSEEK_API_KEY）
extractor = InfoExtractor()

# 或者直接提供API密钥
# extractor = InfoExtractor(api_key="your-api-key-here")

# 分析评论
review_text = "这款产品非常好用，质量很棒！"
result = extractor.extract(review_text)

# 获取结构化数据
print(f"情感: {result.sentiment}")
print(f"关键词: {result.keywords}")
print(f"评分: {result.score}")

# 获取JSON字符串
json_output = result.model_dump_json(indent=2)
print(json_output)

# 或者使用便捷方法
json_output = extractor.extract_to_json(review_text)
print(json_output)
    """)


if __name__ == "__main__":
    demonstrate_extractor()
    quick_usage_example()