"""
信息抽取器 - 从产品评论中提取结构化信息
输入：一段产品评论文字
输出：结构化 JSON，包含 sentiment(positive/neutral/negative), keywords(list), score(1-5)
使用 Pydantic 定义输出模型，调用 LLM(deepseek) 强制输出该格式
"""

import json
import os
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field
from openai import OpenAI


class Sentiment(str, Enum):
    """情感分类枚举"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class ReviewAnalysis(BaseModel):
    """产品评论分析结果模型"""
    sentiment: Sentiment = Field(..., description="情感分析结果: positive/neutral/negative")
    keywords: List[str] = Field(..., description="关键词列表，提取评论中的关键词语")
    score: int = Field(..., ge=1, le=5, description="评分，1-5分")


class InfoExtractor:
    """信息抽取器类"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.deepseek.com"):
        """
        初始化信息抽取器
        
        Args:
            api_key: DeepSeek API密钥，如果为None则从环境变量DEEPSEEK_API_KEY读取
            base_url: DeepSeek API基础URL
        """
        # 优先使用传入的api_key参数，如果没有则尝试从环境变量读取
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError(
                "DeepSeek API密钥未提供。请提供api_key参数或设置环境变量DEEPSEEK_API_KEY"
            )
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=base_url
        )
        
        # 系统提示词，用于指导LLM输出指定格式
        self.system_prompt = """你是一个专业的产品评论分析助手。你的任务是从用户提供的产品评论中提取结构化信息。

请严格按照以下JSON格式输出分析结果：
{
    "sentiment": "positive|neutral|negative",
    "keywords": ["关键词1", "关键词2", "关键词3", ...],
    "score": 1-5
}

分析要求：
1. sentiment（情感）: 根据评论内容判断情感倾向
   - positive: 正面评价，表达满意、推荐、喜欢等
   - neutral: 中性评价，客观描述或既有优点也有缺点
   - negative: 负面评价，表达不满、批评、不推荐等

2. keywords（关键词）: 提取评论中的关键词语，通常是名词或形容词
   - 提取3-8个最重要的关键词
   - 关键词应该简洁明了，反映评论核心内容
   - 避免提取过于通用的词语

3. score（评分）: 根据评论内容给出1-5分的评分
   - 1分: 非常不满意
   - 2分: 不满意
   - 3分: 一般/中性
   - 4分: 满意
   - 5分: 非常满意

请确保输出是有效的JSON格式，不要包含任何额外的文本、解释或markdown格式。"""

    def extract(self, review_text: str) -> ReviewAnalysis:
        """
        从产品评论中提取结构化信息
        
        Args:
            review_text: 产品评论文字
            
        Returns:
            ReviewAnalysis: 分析结果对象
        """
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"请分析以下产品评论：\n\n{review_text}"}
                ],
                temperature=0.1,  # 低温度确保输出一致性
                response_format={"type": "json_object"}
            )
            
            # 解析LLM响应
            result_json = json.loads(response.choices[0].message.content)
            
            # 使用Pydantic模型验证和转换
            analysis = ReviewAnalysis(**result_json)
            return analysis
            
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM响应不是有效的JSON格式: {e}")
        except Exception as e:
            raise RuntimeError(f"信息提取失败: {e}")
    
    def extract_to_json(self, review_text: str) -> str:
        """
        从产品评论中提取结构化信息并返回JSON字符串
        
        Args:
            review_text: 产品评论文字
            
        Returns:
            str: JSON格式的分析结果
        """
        analysis = self.extract(review_text)
        return analysis.model_dump_json(indent=2)


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
                
                # 打印结果
                print(f"情感: {analysis.sentiment.value}")
                print(f"关键词: {', '.join(analysis.keywords)}")
                print(f"评分: {analysis.score}/5")
                print(f"完整JSON:\n{analysis.model_dump_json(indent=2)}")
                
            except Exception as e:
                print(f"分析失败: {e}")
                
    except Exception as e:
        print(f"初始化失败: {e}")
        print("\n请确保:")
        print("1. 已设置正确的DEEPSEEK_API_KEY环境变量")
        print("2. API密钥有效且有足够的余额")
        print("3. 网络连接正常")


if __name__ == "__main__":
    main()