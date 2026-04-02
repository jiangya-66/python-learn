#!/usr/bin/env python3
"""
信息抽取器 - 主入口点
"""

import os
import sys
import os.path as osp

# 获取当前文件所在目录和项目根目录
project_root = osp.dirname(osp.dirname(osp.dirname(osp.abspath(__file__))))
# 添加项目根目录到Python路径（如果尚未添加）
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 不加.（绝对导入）需确保项目根目录在sys.path中
from info_extractor import InfoExtractor, ReviewAnalysis, Sentiment,summarize_results

def main():
    """示例用法"""
    # 示例评论
    sample_reviews = [
        "这款手机真的太棒了！拍照效果清晰，电池续航超长，运行速度飞快。性价比很高，强烈推荐！",
        "产品质量一般，外观还可以但功能不够完善。客服态度不错，但产品本身有待改进。",
        "非常失望！买来一周就出现故障，售后服务也很差，完全不值这个价格。"
    ]
    
    print("信息抽取器示例")
    print("=" * 50)

    # 申明一个列表来存储分析结果
    analysis_results = []
    
    # 尝试从环境变量获取API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        print("警告: 未设置DEEPSEEK_API_KEY环境变量")
        print("请设置环境变量或直接在代码中提供API密钥")
        print("\n示例输出格式:")
        example = ReviewAnalysis(
            sentiment=Sentiment.POSITIVE,
            keywords=["拍照效果", "电池续航", "运行速度", "性价比"],
            score=5
        )
        print(example.model_dump_json(indent=2))
        return
    
    try:
        # 创建信息抽取器
        extractor = InfoExtractor(api_key=api_key)
        
        for i, review in enumerate(sample_reviews, 1):
            print(f"\n示例 {i}:")
            print(f"评论: {review}")
            print("-" * 30)
            
            try:
                # 提取信息
                analysis = extractor.extract(review)
                analysis_results.append(analysis)
                
                # 打印结果
                print(f"情感: {analysis.sentiment.value}")
                print(f"关键词: {', '.join(analysis.keywords)}")
                print(f"评分: {analysis.score}/5")
                print(f"完整JSON:\n{analysis.model_dump_json(indent=2)}")
                
            except Exception as e:
                print(f"分析失败: {e}")
        
        # 汇总统计信息
        summary = summarize_results(analysis_results)
        print("\n汇总统计信息:")
        print(f"总评论数: {summary['total']}")
        print(f"正面评论: {summary['positive']}")
        print(f"中性评论: {summary['neutral']}")
        print(f"负面评论: {summary['negative']}")
        print(f"平均评分: {summary['avg_score']}/5")
       
    except Exception as e:
        print(f"初始化失败: {e}")
        print("\n请确保:")
        print("1. 已设置正确的DEEPSEEK_API_KEY环境变量")
        print("2. API密钥有效且有足够的余额")
        print("3. 网络连接正常")

if __name__ == "__main__":
    main()