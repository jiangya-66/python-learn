"""
信息抽取器 - 主提取器类
从产品评论中提取结构化信息
"""

import json
import os
from typing import Optional
from openai import OpenAI

# 从相对路径导入模块 加.（相对导入）
from .models import ReviewAnalysis, Sentiment

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

