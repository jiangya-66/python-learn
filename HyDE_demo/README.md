# HyDE (Hypothetical Document Embeddings) 演示

## 项目概述

本项目演示了HyDE（Hypothetical Document Embeddings）技术，通过让LLM先生成假设性答案，将"问题语言"转化为"文档语言"，从而提升语义检索的准确性。

## 主要特性

1. **HyDE技术演示**：对比直接使用原问题检索和使用假设答案检索的效果差异
2. **ChromaDB向量数据库**：知识库现在存储在ChromaDB中，支持持久化存储和高效检索
3. **DeepSeek集成**：使用DeepSeek LLM生成假设性答案
4. **多语言支持**：支持中文文档和查询

## 项目结构

```
HyDE-demo/
├── hyde_demo.py              # 主程序
├── chroma_knowledge_base.py  # ChromaDB知识库管理模块
├── test_chroma.py            # ChromaDB测试脚本
├── test_chroma_simple.py     # ChromaDB简单测试
├── knowledge.md              # 项目知识文档
├── README.md                 # 项目说明文档
├── chroma_db/                # ChromaDB数据存储目录（自动创建）
└── .agents/                  # Codebuff代理类型定义
```

## 安装依赖

```bash
pip install chromadb sentence-transformers openai numpy
```

## 环境变量设置

需要设置DeepSeek API密钥：

```bash
# Windows
set DEEPSEEK_API_KEY=your_api_key_here

# Linux/Mac
export DEEPSEEK_API_KEY=your_api_key_here
```

## 使用方法

### 1. 运行主程序

```bash
python hyde_demo.py
```

程序将：
1. 初始化ChromaDB知识库（如果不存在则创建并加载默认文档）
2. 使用DeepSeek为问题"量子计算对密码学的影响"生成假设性答案
3. 分别使用原问题和假设答案查询知识库
4. 对比两种检索方式的结果差异

### 2. 测试ChromaDB知识库

```bash
# 测试基本功能
python test_chroma_simple.py

# 测试完整功能
python test_chroma.py
```

### 3. 直接使用知识库模块

```python
from chroma_knowledge_base import ChromaKnowledgeBase, initialize_knowledge_base

# 初始化知识库
kb = initialize_knowledge_base()

# 查询文档
results = kb.query("量子计算", n_results=5)

# 添加新文档
kb.add_documents(["新文档内容"])

# 获取文档数量
count = kb.get_document_count()
```

## ChromaDB知识库管理

### 主要功能

- **持久化存储**：文档和向量存储在本地`chroma_db`目录中
- **自动初始化**：首次运行时自动创建知识库并加载默认文档
- **高效检索**：支持基于向量的语义相似度检索
- **元数据支持**：可以为文档添加自定义元数据

### 默认文档

知识库包含13篇关于量子计算、密码学和相关技术的文档，包括：
- 量子计算原理和算法（Shor算法、Grover算法）
- 后量子密码学（PQC）标准
- 经典密码学（RSA、TLS）
- 量子计算进展和挑战
- 干扰项文档（深度学习、区块链等）

## 技术实现

### 核心组件

1. **ChromaKnowledgeBase类**：封装ChromaDB操作
   - 文档添加、查询、管理
   - 向量编码和存储
   - 集合管理

2. **HyDE流程**：
   - 问题 → DeepSeek LLM → 假设性答案
   - 假设答案 → 向量编码 → ChromaDB检索
   - 对比分析检索结果

3. **向量模型**：使用`sentence-transformers`的`all-MiniLM-L6-v2`模型进行文本编码

### 修改说明

原始代码使用内存中的列表存储文档，现已修改为：
- 移除`DOCUMENTS`常量
- 添加`chroma_knowledge_base.py`模块
- 修改主程序使用ChromaDB进行检索
- 保持原有API兼容性

## 预期输出

运行程序将显示：
1. 知识库初始化信息
2. DeepSeek生成的假设性答案
3. 两种检索方式的结果对比
4. 统计分析（共同命中、单独命中、相似度对比等）

## 扩展和定制

### 添加自定义文档

```python
from chroma_knowledge_base import ChromaKnowledgeBase

kb = ChromaKnowledgeBase()
new_documents = ["自定义文档1", "自定义文档2"]
kb.add_documents(new_documents)
```

### 修改检索参数

```python
# 修改返回结果数量
results = kb.query("查询文本", n_results=10)

# 使用不同模型
kb = ChromaKnowledgeBase(embedding_model_name="paraphrase-multilingual-MiniLM-L12-v2")
```

### 清空知识库

```python
kb.clear_collection()  # 清空但保留集合
# 或
kb.delete_collection() # 完全删除集合
```

## 注意事项

1. 首次运行需要下载嵌入模型，可能需要较长时间
2. 需要有效的DeepSeek API密钥
3. ChromaDB数据存储在`chroma_db`目录中，可以安全删除
4. 默认使用较小的`all-MiniLM-L6-v2`模型以加快下载速度

## 故障排除

### 模型下载失败
- 检查网络连接
- 尝试设置HF镜像：`set HF_ENDPOINT=https://hf-mirror.com`
- 使用更小的模型

### ChromaDB错误
- 确保有写入权限
- 检查`chroma_db`目录是否被占用
- 尝试删除`chroma_db`目录重新初始化

### DeepSeek API错误
- 检查API密钥是否正确设置
- 确认账户有可用额度
- 检查网络连接