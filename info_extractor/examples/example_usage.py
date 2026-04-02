#!/usr/bin/env python3
"""
信息抽取器使用示例
演示如何在实际项目中使用信息抽取器
"""

import sys
import os.path as osp
# 获取当前文件所在目录和项目根目录
project_root = osp.dirname(osp.dirname(osp.dirname(osp.abspath(__file__))))
# 添加项目根目录到Python路径（如果尚未添加）
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from info_extractor import InfoExtractor, ReviewAnalysis, Sentiment,summarize_results


def example_with_mock_data():
    """使用模拟数据演示（不调用真实API）"""
    print("示例1: 使用模拟数据演示")
    print("=" * 60)
    
    # 创建模拟的ReviewAnalysis对象
    mock_analysis = ReviewAnalysis(
        sentiment=Sentiment.POSITIVE,
        keywords=["质量", "设计", "性能", "价格"],
        score=4
    )
    
    print("模拟分析结果:")
    print(f"情感: {mock_analysis.sentiment.value}")
    print(f"关键词: {', '.join(mock_analysis.keywords)}")
    print(f"评分: {mock_analysis.score}/5")
    
    # 转换为JSON
    json_output = mock_analysis.model_dump_json(indent=2)
    print("\nJSON输出:")
    print(json_output)
    
    # 从JSON还原
    print("\n从JSON还原对象:")
    restored = ReviewAnalysis.model_validate_json(json_output)
    print(f"还原成功: {restored.sentiment.value}, 评分: {restored.score}")
    
    print("\n" + "=" * 60)


def example_api_usage():
    """演示API使用方式（需要真实API密钥）"""
    print("示例2: API使用方式")
    print("=" * 60)
    
    print("""
# 设置环境变量后使用:
import os
from info_extractor import InfoExtractor

# 方法1: 从环境变量读取
api_key = os.getenv("DEEPSEEK_API_KEY")
extractor = InfoExtractor(api_key=api_key)

# 方法2: 直接提供
# extractor = InfoExtractor(api_key="your-actual-api-key")

# 分析评论
review = "这款产品真的很不错，性价比高，使用方便，强烈推荐！"
try:
    result = extractor.extract(review)
    print(f"情感: {result.sentiment.value}")
    print(f"关键词: {result.keywords}")
    print(f"评分: {result.score}/5")
    print(f"JSON: {result.model_dump_json(indent=2)}")
except Exception as e:
    print(f"分析失败: {e}")
    """)
    
    print("\n" + "=" * 60)


def example_batch_processing():
    """演示批量处理"""
    print("示例3: 批量处理演示")
    print("=" * 60)
    
    # 模拟批量评论
    batch_reviews = [
        "产品质量很好，包装精美，物流速度快。",
        "一般般，没有想象中那么好，但也不差。",
        "太差了，用了一次就坏了，客服态度也不好。"
    ]
    
    print("批量评论分析流程:")
    print("""
def analyze_batch(reviews, extractor):
    results = []
    for i, review in enumerate(reviews, 1):
        try:
            result = extractor.extract(review)
            results.append(result)
            print(f"评论{i}: {result.sentiment.value}, 评分: {result.score}")
        except Exception as e:
            print(f"评论{i}分析失败: {e}")
            results.append(None)
    return results
    
# 统计结果
def summarize_results(results):
    positive = sum(1 for r in results if r and r.sentiment == Sentiment.POSITIVE)
    neutral = sum(1 for r in results if r and r.sentiment == Sentiment.NEUTRAL)
    negative = sum(1 for r in results if r and r.sentiment == Sentiment.NEGATIVE)
    avg_score = sum(r.score for r in results if r) / len([r for r in results if r])
    
    print(f"正面: {positive}, 中性: {neutral}, 负面: {negative}")
    print(f"平均评分: {avg_score:.1f}/5")
    """)
    
    print("\n" + "=" * 60)


def example_custom_validation():
    """演示自定义验证"""
    print("示例4: 自定义验证和扩展")
    print("=" * 60)
    
    print("""
# 扩展模型
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EnhancedReviewAnalysis(ReviewAnalysis):
    summary: str = Field(..., description="评论摘要")
    categories: List[str] = Field(default_factory=list, description="产品类别")
    analyzed_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def is_positive(self):
        return self.sentiment == Sentiment.POSITIVE and self.score >= 4
    
    @property
    def is_critical(self):
        return self.sentiment == Sentiment.NEGATIVE and self.score <= 2

# 使用扩展模型
enhanced_data = {
    "sentiment": "positive",
    "keywords": ["质量", "设计", "性能"],
    "score": 5,
    "summary": "非常满意的购物体验",
    "categories": ["电子产品", "数码配件"]
}

try:
    enhanced = EnhancedReviewAnalysis(**enhanced_data)
    print(f"是否正面: {enhanced.is_positive}")
    print(f"是否关键问题: {enhanced.is_critical}")
    print(f"分析时间: {enhanced.analyzed_at}")
except Exception as e:
    print(f"验证失败: {e}")
    """)
    
    print("\n" + "=" * 60)


def main():
    """主函数"""
    print("信息抽取器使用示例")
    print("=" * 60)
    
    example_with_mock_data()
    example_api_usage()
    example_batch_processing()
    example_custom_validation()
    
    print("\n总结:")
    print("1. 信息抽取器可以轻松集成到现有项目中")
    print("2. 支持单个和批量评论分析")
    print("3. 使用Pydantic确保数据一致性")
    print("4. 完整的错误处理和验证机制")
    print("5. 易于扩展和自定义")
    
    print("\n下一步:")
    print("1. 获取DeepSeek API密钥")
    print("2. 设置环境变量 DEEPSEEK_API_KEY")
    print("3. 运行 python info_extractor.py 测试")
    print("4. 集成到你的项目中")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()