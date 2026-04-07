# 项目知识

此文件为 Codebuff 提供项目上下文：目标、命令、约定和注意事项。

## 概述
本项目包含两部分：
1. **Codebuff 代理类型定义** — `.agents/types/` 目录提供了定义代理所需的 TypeScript 模式和接口，具有完整的类型安全性。
2. **简易 RAG 系统** — `rag_ai_history.py` 使用 ChromaDB 实现了一个基于"人工智能历史"文本的检索增强生成（RAG）演示。

## 快速开始
- 安装：
  - TypeScript 类型定义：无需安装步骤（纯类型定义，没有 package.json 或构建工具）。
  - RAG 系统：需要安装 Python 依赖：`pip install chromadb numpy`。
- 开发：
  - 编辑 `.agents/types/` 中的文件以更新类型定义。
  - 编辑 `rag_ai_history.py` 以修改 RAG 系统的文本、嵌入函数或检索逻辑。
- 运行 RAG 演示：`python rag_ai_history.py`
- 测试：未配置测试运行器。可通过运行 `python rag_ai_history.py` 验证 RAG 系统功能。

## 架构
- 关键目录和文件：
  - `.agents/types/` — Codebuff 代理编写的核心类型定义。
    - `agent-definition.ts` — 主要的 `AgentDefinition` 接口（模型、工具、提示词、输入/输出模式、handleSteps）。
    - `tools.ts` — `ToolName` 联合类型、`ToolParamsMap` 以及各工具的参数接口。
    - `util-types.ts` — 共享工具类型：JSON 类型、消息类型、MCP 配置、日志记录器、JSON Schema。
  - `rag_ai_history.py` — 简易 RAG 系统，包含：
    - `CharNgramEmbeddingFunction` — 基于字符 n-gram 的离线嵌入函数（无需联网下载模型），使用 MD5 哈希将 n-gram 映射到固定维度（384）的向量空间。
    - `AI_HISTORY_TEXTS` — 10 段关于"人工智能历史"的中文文本（涵盖 1950–2022 年重要事件）。
    - `build_collection()` — 将文本向量化并存入 ChromaDB（持久化到 `./chroma_db`）。
    - `retrieve(query, collection, top_k=3)` — 根据查询检索最相关的 top_k 段文本。
    - `main()` — 演示入口，执行 3 个示例查询。
  - `./chroma_db/` — ChromaDB 持久化存储目录（运行时自动生成）。

## 依赖
- **Python 包**：
  - `chromadb` >= 1.5.5 — 向量数据库，用于存储和检索嵌入向量。
  - `numpy` — 数值计算，用于嵌入向量的生成与归一化。

## 约定
- 格式化/代码检查：未配置代码检查工具。
  - TypeScript：遵循现有风格——无分号、2 空格缩进、单引号。
  - Python：遵循 PEP 8 风格，使用类型注解。
- 应遵循的模式：
  - 在 `tools.ts` 中为每个工具的参数导出接口。
  - 使用联合类型表示枚举（例如 `ToolName`、`ModelName`）。
  - 保持文件职责单一：每个文件只关注一个问题。
- 应避免的事项：
  - TypeScript 部分不要添加运行时代码——仅包含类型定义。
  - 不要使用 `any` 类型；优先使用显式类型。
  - RAG 系统避免依赖需要联网下载的嵌入模型（当前使用离线 n-gram 方案）。
