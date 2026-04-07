# Python 学习项目

这是一个Python学习项目，包含多个Python编程练习和一个完整的信息抽取器应用。

## 项目结构

```
.
├── README.md                    # 项目说明文档
├── pyproject.toml              # Python项目配置文件
├── .gitignore                  # Git忽略文件
├── sampling_results.json       # 采样参数对比实验结果
├── configs/                    # 配置文件目录
│   └── config.json            # 配置文件
├── exercises/                  # Python练习文件目录
│   ├── py-day1.py             # 异步编程基础：协程和并发IO操作
│   ├── py-day2.py             # 异步编程练习：并发请求限流器
│   ├── py-day3.py             # Pydantic高级功能
│   ├── py-day4.py             # Pydantic配置管理练习
│   ├── py-day5.py             # 信息抽取器演示
│   ├── py-day8.py             # 采样参数对比：测试temperature和top_p对LLM输出的影响
│   ├── py-day9.py             # 去重实验：测试frequency_penalty和presence_penalty对重复性的影响
│   ├── py-day10.py            # logit_bias强制输出特定词汇的demo
│   ├── py-day11.py            # 使用RAG技术检索计算机技术发展史
├── info_extractor/             # 信息抽取器子项目
│   ├── __init__.py             # 包初始化文件
│   ├── README.md               # 信息抽取器详细文档
│   ├── requirements.txt        # 依赖列表
│   ├── src/                   # 源代码目录
│   │   ├── __init__.py        # 源代码包初始化
│   │   ├── models.py          # 数据模型定义（ReviewAnalysis, Sentiment）
│   │   ├── extractor.py       # 信息抽取器主实现（InfoExtractor类）
│   │   ├── utils.py           # 工具函数（验证API密钥、汇总结果等）
│   │   └── main.py            # 主程序入口（修复了导入问题）
│   ├── tests/                 # 测试文件目录
│   │   └── test_extractor.py  # 测试文件
│   └── examples/              # 示例文件目录
│       └── example_usage.py   # 使用示例
└── rag_ai_history/            # RAG（检索增强生成）AI历史检索系统
    ├── rag_ai_history.py      # RAG系统主程序：基于ChromaDB的AI历史检索
    └── knowledge.md           # 项目知识文档
```

## 文件说明

### 1. 异步编程练习

**py-day1.py** - 异步编程基础
- 使用 `asyncio` 实现协程函数
- 模拟不同的IO操作（网络请求、文件读取、数据库查询）
- 使用 `asyncio.gather()` 并发执行任务

**py-day2.py** - 并发请求限流器
- 使用 `asyncio.Semaphore` 实现并发控制
- 模拟100个API请求，限制同时最多5个执行
- 展示异步编程中的资源管理

### 2. Pydantic数据验证练习

**py-day3.py** - Pydantic高级功能
- 基础模型定义和数据验证
- 嵌套模型和自定义验证器
- 数据转换和序列化
- 泛型支持和递归模型
- FastAPI集成示例

**py-day4.py** - Pydantic配置管理
- 从JSON文件加载配置
- 使用 `ConfigDict` 进行模型配置
- 字段验证和别名生成器
- 环境变量支持

### 3. 信息抽取器应用

**py-day5.py** - 信息抽取器演示
- 集成信息抽取器功能
- 提供多个示例评论分析
- 展示完整的API使用流程

**info_extractor/** - 完整的信息抽取器项目
- 使用Pydantic定义严格的输出模型
- 集成DeepSeek LLM进行智能分析
- 支持情感分析、关键词提取和评分
- 完整的错误处理和验证

### 4. LLM参数调优实验

**py-day8.py** - 采样参数对比实验
- 测试不同temperature和top_p参数对LLM输出的影响
- 支持DeepSeek API和模拟模式
- 自动分析响应创造性、长度和词汇多样性
- 生成详细的对比报告和可视化结果
- 保存实验结果到JSON文件

**py-day9.py** - 去重实验
- 测试frequency_penalty和presence_penalty对生成文本重复性的影响
- 模拟API响应，根据惩罚参数调整重复概率
- 统计输出中的重复词数量
- 提供真实DeepSeek API实验代码示例
- 生成热力图展示不同参数组合的效果

### 5. RAG（检索增强生成）AI历史检索系统

**rag_ai_history/** - RAG AI历史检索系统
- 基于ChromaDB向量数据库实现
- 使用自定义字符n-gram嵌入函数，无需联网下载模型
- 包含10段关于人工智能历史的中文文本（1950-2022年重要事件）
- 支持语义检索和相似度查询
- 提供完整的检索增强生成演示

## 快速开始

### 环境要求
- Python 3.8+
- pip 包管理器

### 安装依赖

```bash
# 安装信息抽取器依赖
cd info_extractor
pip install -r requirements.txt

# 或者全局安装（核心功能）
pip install pydantic openai

# 完整安装（包含异步支持和环境变量管理）
pip install pydantic openai aiohttp aiofiles python-dotenv requests

# 安装LLM参数调优实验依赖
pip install requests  # 用于DeepSeek API调用

# 安装RAG AI历史检索系统依赖
pip install chromadb numpy  # 用于向量数据库和数值计算
```

### 运行示例

```bash
# 运行异步编程示例
python exercises/py-day1.py
python exercises/py-day2.py

# 运行Pydantic示例
python exercises/py-day3.py
python exercises/py-day4.py

# 运行信息抽取器演示（需要DeepSeek API密钥）
python exercises/py-day5.py

# 运行LLM参数调优实验
python exercises/py-day8.py  # 采样参数对比实验
python exercises/py-day9.py  # 去重实验

# 运行信息抽取器主程序（修复了导入问题）
python info_extractor/src/main.py

# 或者使用模块方式运行
cd info_extractor
python -m src.main

# 运行RAG AI历史检索系统
python rag_ai_history/rag_ai_history.py
```

## 信息抽取器使用

### 1. 获取API密钥
1. 访问 [DeepSeek平台](https://platform.deepseek.com/api_keys)
2. 注册并获取API密钥
3. 设置环境变量：

```bash
# Windows
set DEEPSEEK_API_KEY=你的API密钥

# Linux/Mac
export DEEPSEEK_API_KEY='你的API密钥'
```

### 2. 基本用法

```python
from info_extractor import InfoExtractor

# 初始化（自动读取环境变量）
extractor = InfoExtractor()

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
```

### 3. 输出示例

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

## 学习目标

通过本项目，您可以学习：

1. **异步编程**：协程、任务、信号量等概念
2. **数据验证**：使用Pydantic进行严格的数据验证
3. **API集成**：如何集成第三方API服务
4. **LLM参数调优**：temperature、top_p、frequency_penalty、presence_penalty等参数对生成结果的影响
5. **实验设计**：如何设计科学实验来测试不同参数的效果
6. **项目结构**：合理的Python项目组织方式
7. **错误处理**：完善的异常处理和用户反馈
8. **向量数据库**：使用ChromaDB进行向量存储和检索
9. **检索增强生成（RAG）**：构建基于向量检索的AI应用

## 技术栈

- **Python 3.8+**：主要编程语言
- **asyncio**：异步编程框架
- **Pydantic**：数据验证和设置管理
- **DeepSeek API**：大语言模型服务
- **requests**：HTTP请求库（用于API调用）
- **aiohttp/aiofiles**：异步HTTP和文件操作
- **ChromaDB**：向量数据库，用于存储和检索嵌入向量
- **numpy**：数值计算库，用于向量操作和数学运算

## 注意事项

1. **API限制**：DeepSeek API有调用频率和配额限制
2. **成本**：使用API会产生费用，请关注用量
3. **网络**：需要稳定的网络连接
4. **错误处理**：建议在生产环境中添加重试机制

## 许可证

jiangya@ License

## 支持

如有问题或建议，请查看各个文件的注释或提交Issue。

## 更新日志

- **2024年**：项目创建，包含Python学习练习
- **2025年**：添加信息抽取器功能
- **2026年4月**：修复信息抽取器中的循环导入问题，优化项目结构
- **2026年4月**：添加LLM参数调优实验（py-day8.py和py-day9.py）
- **2026年4月**：添加RAG AI历史检索系统（rag_ai_history/）
- **持续更新**：根据学习进度添加新功能

---

**提示**：本项目适合Python中级学习者，涵盖了异步编程、数据验证和API集成等实用技能。建议按照文件编号顺序学习。