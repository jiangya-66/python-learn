'''
# 任务：用 ChromaDB 搭建简易 RAG
# 1. 准备 10 段关于“人工智能历史”的文本
# 2. 向量化并存入 ChromaDB
# 3. 用python 实现检索函数，根据 query 返回最相关的 3 段文本
'''

import hashlib
import re
from collections import Counter

import chromadb
import numpy as np


# ── 自定义离线嵌入函数（基于字符 n-gram） ─────────────────────────────
# 定义一个名为 CharNgramEmbeddingFunction 的类，
# 它遵循 ChromaDB 的嵌入函数标准规范（继承:chromadb.EmbeddingFunction），
# 并且专门用于处理字符串列表类型的输入（泛型标注:list[str]）。
class CharNgramEmbeddingFunction(chromadb.EmbeddingFunction[list[str]]):
    """基于字符 n-gram 的轻量嵌入函数，无需联网下载模型。"""

    # tuple：告诉程序，这个参数必须是一个元组。
    # [int, int]：这是泛型写法，进一步规定了元组内部的结构，表示这个元组必须包含两个整数。
    # = (1, 3)：默认值。如果调用函数时不传这个参数，就默认使用 (1, 3)
    def __init__(self, dim: int = 384, ngram_range: tuple[int, int] = (1, 3)):
        self.dim = dim
        self.ngram_range = ngram_range

    def _extract_ngrams(self, text: str) -> list[str]:
        text = re.sub(r'\s+', '', text.lower())
        ngrams: list[str] = []
        for n in range(self.ngram_range[0], self.ngram_range[1] + 1):
            for i in range(len(text) - n + 1):
                ngrams.append(text[i:i + n])
        return ngrams

    def _text_to_vector(self, text: str) -> list[float]:
        ngrams = self._extract_ngrams(text)
        counts = Counter(ngrams)
        # 创建一个长度为 384（self.dim）的一维数组，里面全部填满 0，
        # 并且规定每个数字都必须是 32位浮点数（float32），最后把这个数组赋值给变量 vec。
        # vec=[0.0, 0.0, 0.0, ..., 0.0] (共 384 个 0.0)
        vec = np.zeros(self.dim, dtype=np.float32)
        '''
        核心映射：的是把任意字符串变成一个固定的数字索引（0 到 383 之间）
        我们把它拆成三步看：
        1. gram.encode('utf-8')：这步先把字符串（如 "人工"）转换成 UTF-8 编码的字节流。
        2. hashlib.md5(...).hexdigest()
        这是一个哈希函数。它把刚才的字节流变成一个很长的、看起来随机的十六进制字符串（比如 "a1b2c3..."）。
        关键点：哈希的特性是“确定性”。只要输入相同（都是 "人工"），输出的哈希值永远是一样的。 这保证了同一个词每次都会被映射到同一个位置。
        3. int(..., 16) % self.dim
        int(..., 16)：把那个很长的十六进制字符串转换成一个巨大的十进制整数。
        % self.dim：这是取模运算（求余数）。
        假设 self.dim 是 384。无论前面的整数有多大，除以 384 后的余数一定在 0 到 383 之间。
        结果：这就把无限的字符串空间，强行“折叠”进了有限的 384 个格子里。
        ➕ 累加计数：vec[idx] += count
        vec[idx]：找到向量 vec 中第 idx 个格子。
        += count：把该词出现的次数加到这个格子里。
        含义：
        如果 "人工" 的哈希余数是 5，出现 2 次，那么 vec[5] 就加 2。
        如果 "智能" 的哈希余数也是 5（这叫哈希冲突），出现 1 次，那么 vec[5] 就再加 1，变成 3。
        '''
        for gram, count in counts.items():
            idx = int(hashlib.md5(gram.encode('utf-8')).hexdigest(), 16) % self.dim
            vec[idx] += count
        # 向量归一化：把 vec 中的所有数字除以它们的欧几里得范数（L2 范数），使得整个向量的长度变为 1。
        norm = np.linalg.norm(vec)
        if norm > 0:
            # NumPy 的广播机制：当你对一个数组进行操作时，如果操作数的形状不完全匹配，NumPy 会自动“广播”较小的数组，使其形状与较大的数组兼容。
            vec = vec / norm
        return vec.tolist()

    def __call__(self, input: list[str]) -> list[list[float]]:
        return [self._text_to_vector(text) for text in input]


# ── 1. 准备 10 段关于"人工智能历史"的文本 ──────────────────────────────

AI_HISTORY_TEXTS = [
    '1950年，艾伦·图灵发表了著名论文《计算机器与智能》，提出了"图灵测试"的概念，'
    '成为人工智能哲学基础的重要里程碑。',

    '1956年，约翰·麦卡锡在达特茅斯会议上首次提出"人工智能"（Artificial Intelligence）'
    '这一术语，标志着AI作为一门独立学科的正式诞生。',

    '1966年，约瑟夫·维森鲍姆开发了ELIZA聊天程序，这是最早的自然语言处理程序之一，'
    '能够模拟心理治疗师与人进行简单对话。',

    '1997年，IBM的深蓝（Deep Blue）超级计算机击败了国际象棋世界冠军加里·卡斯帕罗夫，'
    '展示了人工智能在特定领域超越人类专家的能力。',

    '2006年，杰弗里·辛顿提出深度学习的概念，通过多层神经网络实现特征的自动提取，'
    '为现代人工智能的爆发奠定了理论基础。',

    '2011年，IBM Watson在美国电视智力竞赛节目《危险边缘》中击败了人类冠军选手，'
    '展示了AI在自然语言理解和知识推理方面的巨大进步。',

    '2012年，Alex Krizhevsky设计的AlexNet在ImageNet图像识别竞赛中大幅领先，'
    '掀起了深度学习在计算机视觉领域的革命浪潮。',

    '2016年，谷歌DeepMind的AlphaGo以4:1击败围棋世界冠军李世石，'
    '证明了深度强化学习在复杂策略博弈中的强大潜力。',

    '2017年，谷歌发表论文《Attention Is All You Need》，提出了Transformer架构，'
    '彻底改变了自然语言处理领域，成为GPT和BERT等模型的基础。',

    '2022年底，OpenAI发布ChatGPT，基于GPT-3.5大语言模型，以对话形式提供智能助手服务，'
    '迅速引爆全球对生成式人工智能的关注与讨论。',
]


# ── 2. 向量化并存入 ChromaDB ──────────────────────────────────────

def build_collection(
    collection_name: str = "ai_history",
    persist_dir: str = "./chroma_db",) -> chromadb.Collection:
    """将 AI_HISTORY_TEXTS 向量化并存入 ChromaDB，返回 collection。"""
    # 创建一个持久化的 ChromaDB 客户端，指定存储路径为 persist_dir。
    client = chromadb.PersistentClient(path=persist_dir)

    try:
        # 删除同名 collection（如果存在），以保证每次运行都是全新的数据。
        client.delete_collection(collection_name)
    except Exception:
        pass

    embedding_fn = CharNgramEmbeddingFunction()
    # 创建一个新的 collection，指定名称和嵌入函数。
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
    )

    '''
    这两行代码通过循环，把原本只有“内容”的文本列表，扩展成了“内容 + 唯一ID + 原始索引”的完整数据结构。
    | 序号 | 原始文本 (`documents`) | 生成的 ID (`ids`) | 生成的元数据 (`metadatas`) |
    | :--- | :--- | :--- | :--- |
    | 0 | "图灵在1950年..." | `"doc_0"` | `{"index": 0}` |
    | 1 | "1956年达特茅斯..." | `"doc_1"` | `{"index": 1}` |
    | 2 | "2012年深度学习..." | `"doc_2"` | `{"index": 2}` |
    '''
    collection.add(
        documents=AI_HISTORY_TEXTS,
        ids=[f"doc_{i}" for i in range(len(AI_HISTORY_TEXTS))],
        metadatas=[{"index": i} for i in range(len(AI_HISTORY_TEXTS))],
    )

    print(f"已将 {len(AI_HISTORY_TEXTS)} 段文本存入 ChromaDB (collection={collection_name!r})")
    return collection


# ── 3. 检索函数：根据 query 返回最相关的 3 段文本 ────────────────────

def retrieve(
    query: str,
    collection: chromadb.Collection,
    top_k: int = 3,
) -> list[dict]:
    """
    根据 query 在 collection 中检索最相关的 top_k 段文本。

    返回值示例::

        [
            {"rank": 1, "document": "...", "distance": 0.32, "id": "doc_5"},
            ...
        ]
    """
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    output = []
    '''results 的结构是一个字典，包含了查询结果的不同方面。
    我们通过 zip 函数把这些方面组合在一起，形成一个个完整的结果项。
    这是 Python 非常优雅的元组解包语法，
    它允许我们同时遍历多个列表（documents、distances、ids），
    并且在每次迭代中得到对应位置的元素。
    | 循环次数 | rank (排名) | doc (文档内容) | dist (距离) | doc_id (ID) |
    | :--- | :--- | :--- | :--- | :--- |
    | 第 1 次 | 1 | "图灵测试..." | 0.1 | "doc_0" |
    | 第 2 次 | 2 | "深度学习..." | 0.2 | "doc_1" |
    | 第 3 次 | 3 | "神经网络..." | 0.3 | "doc_2" |
    '''
    for rank, (doc, dist, doc_id) in enumerate(
        zip(
            results["documents"][0],
            results["distances"][0],
            results["ids"][0],
        ),
        start=1,
    ):
        output.append({
            "rank": rank,
            "document": doc,
            "distance": round(dist, 4),
            "id": doc_id,
        })
    return output


# ── 主程序入口 ─────────────────────────────────────────────────────

def main() -> None:
    collection = build_collection()

    queries = [
        "图灵测试是什么时候提出的？",
        "深度学习的发展历程",
        "AlphaGo与围棋",
    ]

    for q in queries:
        print(f"\n{'='*60}")
        print(f"查询: {q}")
        print('='*60)
        results = retrieve(q, collection)
        for item in results:
            print(f"\n  [Top {item['rank']}] (距离: {item['distance']}, ID: {item['id']})")
            print(f"  {item['document']}")


if __name__ == "__main__":
    main()
