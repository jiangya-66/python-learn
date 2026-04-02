#!/usr/bin/env python3
"""
测试信息抽取器
"""

import os
import sys
import os.path as osp

# 获取当前文件所在目录和项目根目录
current_dir = osp.dirname(osp.abspath(__file__))
project_root = osp.dirname(osp.dirname(current_dir))

# 添加项目根目录到Python路径（如果尚未添加）
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
from info_extractor.src.extractor import InfoExtractor, ReviewAnalysis, Sentiment

def test_without_api_key():
    """测试无API密钥情况下的示例输出"""
    print("测试1: 无API密钥示例")
    print("=" * 50)
    
    # 创建示例分析结果
    example = ReviewAnalysis(
        sentiment=Sentiment.POSITIVE,
        keywords=["拍照效果", "电池续航", "运行速度", "性价比", "推荐"],
        score=5
    )
    
    print("示例输出格式:") 
    print(example.model_dump_json(indent=2))
    print()
    
    # 测试模型验证
    test_data = {
        "sentiment": "negative",
        "keywords": ["故障", "售后服务", "价格", "质量"],
        "score": 2
    }
    
    try:
        analysis = ReviewAnalysis(**test_data)
        print("模型验证成功:")
        print(f"情感: {analysis.sentiment}")
        print(f"关键词: {analysis.keywords}")
        print(f"评分: {analysis.score}")
    except Exception as e:
        print(f"模型验证失败: {e}")
    
    print("\n" + "=" * 50)


def test_with_mock_api():
    """使用模拟数据测试（不调用真实API）"""
    print("测试2: 使用模拟数据")
    print("=" * 50)
    
    # 模拟评论数据
    test_reviews = [
        {
            "text": "这款笔记本电脑性能强劲，屏幕显示效果很棒，但电池续航一般。",
            "expected_sentiment": "neutral",
            "expected_keywords": ["性能", "屏幕显示", "电池续航", "笔记本电脑"],
            "expected_score": 4
        },
        {
            "text": "产品质量太差了，用了一个月就坏了，客服也不理人，非常失望！",
            "expected_sentiment": "negative",
            "expected_keywords": ["质量", "故障", "客服", "失望"],
            "expected_score": 1
        },
        {
            "text": "物超所值！功能齐全，操作简单，外观漂亮，强烈推荐给大家！",
            "expected_sentiment": "positive",
            "expected_keywords": ["物超所值", "功能齐全", "操作简单", "外观", "推荐"],
            "expected_score": 5
        }
    ]
    
    for i, test in enumerate(test_reviews, 1):
        print(f"\n测试用例 {i}:")
        print(f"评论: {test['text']}")
        print(f"预期情感: {test['expected_sentiment']}")
        print(f"预期关键词: {test['expected_keywords']}")
        print(f"预期评分: {test['expected_score']}")
    
    print("\n" + "=" * 50)


def main():
    """主测试函数"""
    print("信息抽取器测试")
    print("=" * 60)
    
    # 测试1: 无API密钥示例
    test_without_api_key()
    
    # 测试2: 模拟数据测试
    test_with_mock_api()
    
    # 检查API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    if api_key:
        print("测试3: 真实API测试（需要有效API密钥）")
        print("=" * 50)
        print(f"检测到API密钥: {api_key[:10]}...")
        print("\n要使用真实API测试，请运行:")
        print("python info_extractor.py")
        print("\n或直接调用:")
        print("""
from info_extractor import InfoExtractor

extractor = InfoExtractor(api_key="你的API密钥")
review = "这款产品非常好用，质量很棒！"
result = extractor.extract(review)
print(result.model_dump_json(indent=2))
        """)
    else:
        print("测试3: 真实API测试（跳过 - 未设置API密钥）")
        print("=" * 50)
        print("要启用真实API测试，请设置环境变量:")
        print("export DEEPSEEK_API_KEY='你的API密钥'  # Linux/Mac")
        print("set DEEPSEEK_API_KEY=你的API密钥       # Windows")
        print("\n获取API密钥: https://platform.deepseek.com/api_keys")
    
    print("\n" + "=" * 60)
    print("测试完成！")


if __name__ == "__main__":
    main()