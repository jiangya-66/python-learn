"""
HyDE (Hypothetical Document Embeddings) 演示

流程：
1. 给定一个复杂问题，让 DeepSeek LLM 生成一段假设性答案
2. 用假设答案进行向量检索
3. 对比直接用原问题检索的结果差异

修改：知识库现在存储在ChromaDB向量数据库中
"""

import os
import sys
import numpy as np
from openai import OpenAI

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from sentence_transformers import SentenceTransformer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'HyDE_demo'))

# 导入ChromaDB知识库模块
from chroma_knowledge_base import initialize_knowledge_base

# ============================================================================
# 1. 知识库（存储在ChromaDB中）
# ============================================================================

# 注意：DOCUMENTS常量已移除，文档现在存储在ChromaDB中

# ============================================================================
# 2. 初始化模型
# ============================================================================

def init_deepseek_client() -> OpenAI:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


# ============================================================================
# 3. 核心函数
# ============================================================================

def generate_hypothetical_answer(client: OpenAI, question: str) -> str:
    """使用 DeepSeek 为给定问题生成一段假设性答案（HyDE 的关键步骤）"""
    print("=" * 60)
    print("步骤1: 使用 DeepSeek 生成假设性答案")
    print("=" * 60)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位学术专家。请针对用户的问题，撰写一段详细的、百科全书式的回答。"
                    "回答应包含具体的技术细节、算法名称和实际影响。"
                    "直接给出回答内容，不要加任何前缀。"
                ),
            },
            {"role": "user", "content": question},
        ],
        temperature=0.1,
        max_tokens=512,
    )
    answer = response.choices[0].message.content or ""
    print(f"\n假设性答案:\n{answer}\n")
    return answer


def print_results(title: str, results: list[tuple[int, float, str]]) -> None:
    """格式化打印检索结果"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    for rank, (idx, score, doc) in enumerate(results, 1):
        preview = doc[:80] + "..." if len(doc) > 80 else doc
        print(f"  [{rank}] 文档#{idx:<2d}  相似度: {score:.4f}")
        print(f"      {preview}")
    print()

# ============================================================================
# 4. 对比分析
# ============================================================================

def compare_results(
    direct_results: list[tuple[int, float, str]],
    hyde_results: list[tuple[int, float, str]],
) -> None:
    """对比两种检索方式的结果差异"""
    print("=" * 60)
    print("  结果对比分析")
    print("=" * 60)

    direct_ids = {idx for idx, _, _ in direct_results}
    hyde_ids = {idx for idx, _, _ in hyde_results}

    common = direct_ids & hyde_ids
    only_direct = direct_ids - hyde_ids
    only_hyde = hyde_ids - direct_ids

    print(f"\n  两种方法共同检索到的文档: {sorted(common)}")
    print(f"  仅「直接检索」命中的文档:  {sorted(only_direct)}")
    print(f"  仅「HyDE检索」命中的文档:  {sorted(only_hyde)}")

    direct_scores = [s for _, s, _ in direct_results]
    hyde_scores = [s for _, s, _ in hyde_results]
    print(f"\n  直接检索 - 平均相似度: {np.mean(direct_scores):.4f}  最高: {max(direct_scores):.4f}")
    print(f"  HyDE检索 - 平均相似度: {np.mean(hyde_scores):.4f}  最高: {max(hyde_scores):.4f}")

    print("\n  排名变化:")
    direct_rank = {idx: rank for rank, (idx, _, _) in enumerate(direct_results, 1)}
    hyde_rank = {idx: rank for rank, (idx, _, _) in enumerate(hyde_results, 1)}
    all_ids = direct_ids | hyde_ids
    for doc_id in sorted(all_ids):
        d_rank = direct_rank.get(doc_id, "-")
        h_rank = hyde_rank.get(doc_id, "-")
        print(f"    文档#{doc_id}: 直接检索排名={d_rank}, HyDE检索排名={h_rank}")

    print()

# ============================================================================
# 5. 主流程
# ============================================================================

def main() -> None:
    # “直接检索”的相似度更高：HyDE检索通常比精炼的问题更“发散”，导致向量距离变远。
    question = "量子计算对密码学的影响"

    # “HyDE检索”的相似度更高：调整prompt，将 temperature=0.7 改为 0.1 或 0。让生成的答案更确定、更接近事实，减少发散性。
    # question = "量子计算对密码学的影响。请用一句话概括核心答案，不要解释，不要废话。"

    top_k = 5

    print("=" * 60)
    print("  HyDE演示 - 知识库存储在ChromaDB中")
    print("=" * 60)
    
    print(f"\n原始问题: {question}")
    print(f"检索数量: Top-{top_k}\n")

    # 初始化知识库
    print("正在初始化ChromaDB知识库...")
    kb = initialize_knowledge_base()
    print(f"知识库文档数量: {kb.get_document_count()} 篇文档\n")

    # 初始化DeepSeek客户端
    client = init_deepseek_client()

    # 步骤1: 生成假设性答案
    hypothetical_answer = generate_hypothetical_answer(client, question)

    # 步骤2: 分别使用原问题和假设答案查询知识库
    print("=" * 60)
    print("步骤2: 向量检索")
    print("=" * 60)
    
    # 使用原问题查询
    print("\n使用原问题查询知识库...")
    direct_query_results = kb.query(question, n_results=top_k)
    
    # 使用假设答案查询
    print("使用假设答案查询知识库...")
    hyde_query_results = kb.query(hypothetical_answer, n_results=top_k)
    
    # 转换结果格式以保持兼容性
    direct_results = [(i, score, doc) for i, (doc, score, _) in enumerate(direct_query_results)]
    hyde_results = [(i, score, doc) for i, (doc, score, _) in enumerate(hyde_query_results)]

    print_results("方式A: 直接用原问题检索", direct_results)
    print_results("方式B: HyDE — 用假设性答案检索", hyde_results)

    # 步骤3: 对比分析
    compare_results(direct_results, hyde_results)

    print("=" * 60)
    print("  结论")
    print("=" * 60)
    print(
        "  HyDE 通过让 LLM 先生成假设性答案，将「问题语言」转化为「文档语言」，\n"
        "  使检索向量更贴近知识库中的文档表示，从而提升语义检索的准确性。\n"
        "  尤其在问题较为抽象或使用口语化表达时，HyDE 的优势更为明显。\n"
    )
    print("  知识库现在存储在ChromaDB向量数据库中，支持持久化存储和高效检索。\n")


if __name__ == "__main__":
    main()
