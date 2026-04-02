# 信息抽取器 (Information Extractor)

一个使用 Python 构建的信息抽取器，可以从产品评论中提取结构化信息。

## 功能特性

- **输入**: 一段产品评论文字
- **输出**: 结构化 JSON，包含:
  - `sentiment`: 情感分析 (positive/neutral/negative)
  - `keywords`: 关键词列表
  - `score`: 评分 (1-5分)
- **技术栈**:
  - 使用 Pydantic 定义严格的输出模型
  - 调用 DeepSeek LLM 进行智能分析
  - 强制输出指定 JSON 格式

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 获取 API 密钥

1. 访问 [DeepSeek 平台](https://platform.deepseek.com/api_keys)
2. 注册并获取 API 密钥
3. 设置环境变量:

```bash
# Windows
set DEEPSEEK_API_KEY=你的API密钥

# Linux/Mac
export DEEPSEEK_API_KEY='你的API密钥'
```

### 3. 运行示例

```bash
# 运行主示例
python info_extractor.py

# 运行测试
python test_extractor.py

# 运行演示
python py-day5.py
```

## 使用方法

### 基本用法

```python
from info_extractor import InfoExtractor

# 初始化（自动读取环境变量）
extractor = InfoExtractor()

# 或者直接提供API密钥
# extractor = InfoExtractor(api_key="your-api-key-here")

# 分析评论
review_text = "这款手机拍照效果很棒，电池续航也很给力！"
result = extractor.extract(review_text)

# 访问结果
print(f"情感: {result.sentiment}")      # positive/neutral/negative
print(f"关键词: {result.keywords}")      # ['拍照效果', '电池续航', ...]
print(f"评分: {result.score}/5")         # 1-5

# 获取JSON字符串
json_output = result.model_dump_json(indent=2)
print(json_output)

# 或者使用便捷方法
json_output = extractor.extract_to_json(review_text)
```

### 输出示例

```json
{
  "sentiment": "positive",
  "keywords": [
    "拍照效果",
    "电池续航",
    "运行速度",
    "性价比"
  ],
  "score": 5
}
```

## 项目结构

```
.
├── info_extractor.py      # 主实现文件
├── test_extractor.py      # 测试文件
├── requirements.txt      # 依赖列表
└── README.md            # 项目文档
```

## 核心组件

### 1. Pydantic 模型 (`ReviewAnalysis`)

```python
from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class ReviewAnalysis(BaseModel):
    sentiment: Sentiment
    keywords: List[str]
    score: int = Field(ge=1, le=5)
```

### 2. 信息抽取器类 (`InfoExtractor`)

- 自动验证输入输出
- 集成 DeepSeek API
- 完整的错误处理
- 支持 JSON 格式输出

### 3. 系统提示词

精心设计的系统提示词确保 LLM 输出指定格式:

```python
system_prompt = """你是一个专业的产品评论分析助手...
请严格按照以下JSON格式输出分析结果：
{
    "sentiment": "positive|neutral|negative",
    "keywords": ["关键词1", "关键词2", ...],
    "score": 1-5
}
..."""
```

## 测试

项目包含完整的测试用例:

```bash
# 运行所有测试
python test_extractor.py

# 测试输出:
# 1. 无API密钥示例测试
# 2. 模拟数据测试
# 3. 真实API测试（需要设置API密钥）
```

## 错误处理

- API 密钥验证
- JSON 格式验证
- 网络错误处理
- 输入验证

## 扩展功能

### 自定义模型

```python
# 扩展输出模型
class ExtendedReviewAnalysis(ReviewAnalysis):
    summary: str
    categories: List[str]
```

### 批量处理

```python
def batch_extract(reviews: List[str]) -> List[ReviewAnalysis]:
    results = []
    for review in reviews:
        result = extractor.extract(review)
        results.append(result)
    return results
```

### 异步支持

```python
import asyncio
from info_extractor import InfoExtractor

async def async_extract(review: str):
    extractor = InfoExtractor(api_key="your-key")
    return await extractor.extract_async(review)
```

## 注意事项

1. **API 限制**: DeepSeek API 有调用频率和配额限制
2. **成本**: 使用 API 会产生费用，请关注用量
3. **网络**: 需要稳定的网络连接
4. **错误处理**: 建议在生产环境中添加重试机制

## 许可证

jiangya@ License

## 支持

如有问题或建议，请提交 Issue 或联系维护者。