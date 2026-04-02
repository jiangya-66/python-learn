"""
信息抽取器 - 数据模型
定义共享的数据结构和类型
"""

from enum import Enum
from typing import List
from pydantic import BaseModel, Field


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