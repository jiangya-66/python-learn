"""
ChromaDB知识库管理模块
用于将文档存储在ChromaDB向量数据库中
"""

import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple, Optional
import uuid


class ChromaKnowledgeBase:
    """ChromaDB知识库管理类"""
    
    def __init__(self, 
                 collection_name: str = "hyde_demo_kb",
                 persist_directory: str = "./chroma_db",
                 embedding_model_name: str = "all-MiniLM-L6-v2"):
        """
        初始化ChromaDB知识库
        
        Args:
            collection_name: ChromaDB集合名称
            persist_directory: 持久化存储目录
            embedding_model_name: 嵌入模型名称（使用更小的模型）
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model_name
        
        # 初始化ChromaDB客户端
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 加载嵌入模型
        self.embedding_model = None
        self._init_embedding_model()
        
        # 获取或创建集合
        self.collection = self._get_or_create_collection()
        
    def _init_embedding_model(self):
        """初始化嵌入模型"""
        print(f"正在加载嵌入模型 ({self.embedding_model_name})...")
        try:
            # 尝试使用更小的模型，下载更快
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            print("嵌入模型加载完成。")
        except Exception as e:
            print(f"模型加载失败: {e}")
            print("尝试使用本地模型或备用方案...")
            # 如果模型加载失败，使用一个简单的备用方案
            raise
        
    def _get_or_create_collection(self):
        """获取或创建ChromaDB集合"""
        try:
            # 尝试获取现有集合
            collection = self.client.get_collection(name=self.collection_name)
            print(f"已加载现有集合: {self.collection_name}")
            return collection
        except Exception:
            # 创建新集合
            print(f"创建新集合: {self.collection_name}")
            return self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "HyDE演示知识库"}
            )
    
    def add_documents(self, documents: List[str], metadatas: Optional[List[dict]] = None):
        """
        添加文档到知识库
        
        Args:
            documents: 文档列表
            metadatas: 元数据列表（可选）
        """
        if not documents:
            return
            
        print(f"正在添加 {len(documents)} 篇文档到知识库...")
        
        # 生成文档ID
        doc_ids = [str(uuid.uuid4()) for _ in range(len(documents))]
        
        # 生成嵌入向量
        embeddings = self.embedding_model.encode(documents, normalize_embeddings=True)
        
        # 准备元数据
        if metadatas is None:
            metadatas = [{"source": "hyde_demo"} for _ in range(len(documents))]
        
        # 添加到集合
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=documents,
            metadatas=metadatas,
            ids=doc_ids
        )
        
        print(f"成功添加 {len(documents)} 篇文档到知识库。")
        
    def query(self, query_text: str, n_results: int = 5) -> List[Tuple[str, float, dict]]:
        """
        查询知识库
        
        Args:
            query_text: 查询文本
            n_results: 返回结果数量
            
        Returns:
            返回 (文档内容, 相似度分数, 元数据) 列表
        """
        # 生成查询向量
        query_embedding = self.embedding_model.encode(
            [query_text], 
            normalize_embeddings=True
        )[0].tolist()
        
        # 执行查询
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # 转换结果格式
        query_results = []
        if results["documents"] and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                doc = results["documents"][0][i]
                # ChromaDB返回的是距离（越小越相似），转换为相似度分数
                distance = results["distances"][0][i]
                similarity = 1.0 - distance  # 余弦距离转换为相似度
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                query_results.append((doc, similarity, metadata))
        
        return query_results
    
    def get_all_documents(self) -> List[str]:
        """获取所有文档"""
        results = self.collection.get()
        return results["documents"] if results["documents"] else []
    
    def get_document_count(self) -> int:
        """获取文档数量"""
        results = self.collection.get()
        return len(results["documents"]) if results["documents"] else 0
    
    def clear_collection(self):
        """清空集合"""
        self.collection.delete()
        print(f"已清空集合: {self.collection_name}")
        # 重新创建集合
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "HyDE演示知识库"}
        )
    
    def delete_collection(self):
        """删除集合"""
        self.client.delete_collection(name=self.collection_name)
        print(f"已删除集合: {self.collection_name}")


def initialize_knowledge_base() -> ChromaKnowledgeBase:
    """
    初始化知识库并加载默认文档
    
    Returns:
        ChromaKnowledgeBase实例
    """
    # 默认文档（与原始代码相同）
    DEFAULT_DOCUMENTS = [
        # 量子计算相关
        "量子计算机利用量子比特（qubit）的叠加态和纠缠态进行并行计算，其计算能力在特定问题上远超经典计算机。"
        "Shor算法可以在多项式时间内分解大整数，这对当前基于大整数分解的RSA加密体系构成了根本性威胁。",

        "后量子密码学（Post-Quantum Cryptography, PQC）是指能够抵抗量子计算机攻击的密码算法。"
        "NIST已经在2024年发布了首批后量子密码标准，包括基于格的CRYSTALS-Kyber和基于哈希的SPHINCS+。",

        "量子密钥分发（QKD）利用量子力学原理实现理论上无条件安全的密钥交换。"
        "BB84协议是最早的QKD协议，任何窃听行为都会导致量子态坍缩从而被检测到。",

        "Grover算法可以将对称加密的暴力破解速度提升至平方根级别。"
        "这意味着AES-128在量子计算机面前仅相当于AES-64的安全强度，因此建议将对称密钥长度加倍至256位。",

        "量子计算对椭圆曲线密码学（ECC）同样构成威胁。Shor算法可以高效求解离散对数问题，"
        "导致ECDSA、ECDH等广泛使用的公钥方案在量子时代将不再安全。",

        # 经典密码学相关
        "RSA算法基于大整数分解的困难性，是目前互联网上最广泛使用的公钥加密算法之一。"
        "典型的RSA密钥长度为2048位或4096位。",

        "TLS协议是互联网安全通信的基石，它结合了非对称加密进行密钥交换和对称加密进行数据传输，"
        "从而在效率和安全性之间取得平衡。",

        # 量子计算进展
        "2023年IBM推出了1121量子比特的Condor处理器，但纠错能力仍然是实现大规模量子计算的主要挑战。"
        "目前的量子计算机处于NISQ（含噪声中等规模量子）时代。",

        "量子纠错码（如Surface Code）通过冗余编码来保护量子信息免受噪声干扰。"
        "实现真正实用的容错量子计算可能需要数百万个物理量子比特。",

        # 无关文档（干扰项）
        "深度学习在自然语言处理领域取得了突破性进展，Transformer架构成为了大语言模型的基础。"
        "GPT、BERT等模型在文本生成和理解任务上表现优异。",

        "区块链技术通过去中心化的分布式账本实现了无需信任第三方的价值转移。"
        "比特币和以太坊是目前最知名的区块链网络。",

        "全球气候变化导致极端天气事件频发，各国纷纷制定碳中和目标。"
        "可再生能源的发展是应对气候变化的关键措施之一。",

        "基因编辑技术CRISPR-Cas9的发现使精确修改DNA成为可能，"
        "在医学、农业等领域展现出巨大的应用潜力。",
    ]
    
    # 创建知识库实例
    kb = ChromaKnowledgeBase()
    
    # 如果知识库为空，则添加默认文档
    if kb.get_document_count() == 0:
        print("知识库为空，正在加载默认文档...")
        kb.add_documents(DEFAULT_DOCUMENTS)
        print(f"知识库初始化完成，共加载 {kb.get_document_count()} 篇文档。")
    else:
        print(f"知识库已存在，包含 {kb.get_document_count()} 篇文档。")
    
    return kb


if __name__ == "__main__":
    # 测试代码
    kb = initialize_knowledge_base()
    print(f"\n知识库文档数量: {kb.get_document_count()}")
    
    # 测试查询
    query = "量子计算对密码学的影响"
    results = kb.query(query, n_results=3)
    
    print(f"\n查询: {query}")
    print("查询结果:")
    for i, (doc, score, metadata) in enumerate(results, 1):
        preview = doc[:80] + "..." if len(doc) > 80 else doc
        print(f"  [{i}] 相似度: {score:.4f}")
        print(f"      {preview}")