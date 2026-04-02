"""
信息抽取器 - 工具函数
包含一些辅助函数和工具
"""

import os
from typing import List

from .models import ReviewAnalysis, Sentiment

def validate_api_key(api_key: str = None) -> str:
    """
    验证API密钥
    
    Args:
        api_key: 可选的API密钥，如果为None则从环境变量读取
        
    Returns:
        str: 有效的API密钥
        
    Raises:
        ValueError: 如果API密钥无效
    """
    key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise ValueError(
            "DeepSeek API密钥未提供。请提供api_key参数或设置环境变量DEEPSEEK_API_KEY"
        )
    return key


def summarize_results(results: List[ReviewAnalysis]) -> dict:
    """
    汇总分析结果
    
    Args:
        results: ReviewAnalysis对象列表
        
    Returns:
        dict: 汇总统计信息
    """
    if not results:
        return {
            "total": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "avg_score": 0.0
        }
    
    valid_results = [r for r in results if r is not None]
    total = len(valid_results)
    
    positive = sum(1 for r in valid_results if r.sentiment == Sentiment.POSITIVE)
    neutral = sum(1 for r in valid_results if r.sentiment == Sentiment.NEUTRAL)
    negative = sum(1 for r in valid_results if r.sentiment == Sentiment.NEGATIVE)
    
    avg_score = sum(r.score for r in valid_results) / total if total > 0 else 0.0
    
    return {
        "total": total,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "avg_score": round(avg_score, 2)
    }


def format_results_for_display(analysis: ReviewAnalysis) -> str:
    """
    格式化分析结果用于显示
    
    Args:
        analysis: ReviewAnalysis对象
        
    Returns:
        str: 格式化后的字符串
    """
    return f"""
情感分析: {analysis.sentiment.value}
关键词: {', '.join(analysis.keywords)}
评分: {analysis.score}/5
完整JSON输出:
{analysis.model_dump_json(indent=2)}
"""