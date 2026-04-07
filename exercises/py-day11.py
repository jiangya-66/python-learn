"""
py-day11.py - 使用RAG技术检索计算机技术发展史

任务要求：
1. 准备10段关于"计算机技术发展史"的文本
2. 调用rag_ai_history子项目中的方法，向量化并存入ChromaDB
3. 根据query返回最相关的3段文本
4. 注意：rag_ai_history子项目中的方法不要重新创建，直接在py-day11.py中导入
"""

import sys
import os

# 添加rag_ai_history目录到Python路径，以便导入其中的模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rag_ai_history'))

# 导入rag_ai_history中的方法
from rag_ai_history import CharNgramEmbeddingFunction, build_collection, retrieve

# ── 1. 准备10段关于"计算机技术发展史"的文本 ──────────────────────────────

COMPUTER_HISTORY_TEXTS = [
    # 1. 早期计算设备
    '公元前3000年左右，古代中国发明了算盘，这是人类历史上最早的计算工具之一，'
    '通过珠子的移动进行加减乘除运算，一直沿用至今。',
    
    # 2. 机械计算时代
    '1642年，法国数学家布莱兹·帕斯卡发明了帕斯卡计算器，这是世界上第一台机械式计算器，'
    '能够进行加减运算，开启了机械计算的时代。',
    
    # 3. 分析机概念
    '1837年，英国数学家查尔斯·巴贝奇提出了分析机的概念，被认为是现代计算机的理论先驱，'
    '包含了输入、处理、存储和输出等现代计算机的基本组件。',
    
    # 4. 电子计算机诞生
    '1946年，美国宾夕法尼亚大学研制出ENIAC（电子数字积分计算机），这是世界上第一台通用电子计算机，'
    '重达30吨，占地167平方米，每秒能进行5000次加法运算。',
    
    # 5. 晶体管革命
    '1947年，贝尔实验室的威廉·肖克利、约翰·巴丁和沃尔特·布拉顿发明了晶体管，'
    '取代了笨重、耗电的真空管，使计算机体积大幅缩小，可靠性显著提高。',
    
    # 6. 集成电路时代
    '1958年，杰克·基尔比发明了集成电路，将多个晶体管集成在一块半导体芯片上，'
    '开启了微电子革命，为个人计算机的出现奠定了基础。',
    
    # 7. 微处理器诞生
    '1971年，英特尔公司推出了世界上第一款微处理器Intel 4004，包含2300个晶体管，'
    '主频740kHz，标志着计算机进入微处理器时代。',
    
    # 8. 个人计算机革命
    '1977年，苹果公司推出了Apple II个人计算机，配备了彩色显示器和键盘，'
    '成为第一款大规模生产的个人计算机，推动了个人计算机的普及。',
    
    # 9. 图形用户界面
    '1984年，苹果公司推出了Macintosh计算机，首次引入了图形用户界面（GUI）和鼠标操作，'
    '使计算机操作更加直观和用户友好。',
    
    # 10. 互联网与移动计算
    '1990年代，万维网（World Wide Web）的发明和互联网的普及彻底改变了计算机的使用方式，'
    '而2007年苹果iPhone的发布则开启了移动计算的新时代。',
]

# ── 2. 自定义构建函数，使用计算机历史文本 ──────────────────────────────

def build_computer_history_collection(
    collection_name: str = "computer_history",
    persist_dir: str = "./chroma_db",
) -> object:
    """
    将计算机历史文本向量化并存入ChromaDB
    
    参数:
        collection_name: 集合名称
        persist_dir: ChromaDB存储目录
        
    返回:
        ChromaDB集合对象
    """
    # 创建嵌入函数
    embedding_fn = CharNgramEmbeddingFunction()
    
    # 创建持久化客户端
    import chromadb
    client = chromadb.PersistentClient(path=persist_dir)
    
    # 删除已存在的集合（如果存在）
    try:
        client.delete_collection(collection_name)
        print(f"已删除已存在的集合: {collection_name}")
    except Exception:
        pass
    
    # 创建新集合
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
    )
    
    # 添加文档到集合
    collection.add(
        documents=COMPUTER_HISTORY_TEXTS,
        ids=[f"computer_doc_{i}" for i in range(len(COMPUTER_HISTORY_TEXTS))],
        metadatas=[{"index": i, "topic": "computer_history"} for i in range(len(COMPUTER_HISTORY_TEXTS))],
    )
    
    print(f"已将 {len(COMPUTER_HISTORY_TEXTS)} 段计算机历史文本存入 ChromaDB")
    print(f"集合名称: {collection_name}")
    print(f"存储路径: {persist_dir}")
    
    return collection

# ── 3. 检索函数封装 ──────────────────────────────────────────────────

def retrieve_computer_history(
    query: str,
    collection: object,
    top_k: int = 3,
) -> list:
    """
    检索与查询最相关的计算机历史文本
    
    参数:
        query: 查询字符串
        collection: ChromaDB集合对象
        top_k: 返回最相关的结果数量
        
    返回:
        包含检索结果的列表
    """
    results = retrieve(query, collection, top_k)
    
    # 将距离转换为相似度（相似度 = 1 - 距离）
    for item in results:
        item['similarity'] = 1 - item['distance']
    
    return results

# ── 4. 主程序 ───────────────────────────────────────────────────────

def main():
    """主函数：演示完整的RAG流程"""
    print("=" * 70)
    print("计算机技术发展史RAG检索系统")
    print("=" * 70)
    
    # 构建集合
    print("\n1. 正在构建计算机历史知识库...")
    collection = build_computer_history_collection()
    
    # 测试查询
    print("\n2. 测试检索功能...")
    
    test_queries = [
        "最早的计算机是什么？",
        "晶体管对计算机发展的影响",
        "个人计算机的发展历程",
        "图形用户界面是什么时候出现的？",
        "互联网与移动计算的关系",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"查询: {query}")
        print('='*60)
        
        results = retrieve_computer_history(query, collection)
        
        for item in results:
            print(f"\n  [Top {item['rank']}] (相似度: {item['similarity']:.4f}, ID: {item['id']})")
            print(f"  {item['document']}")
    
    print("\n" + "=" * 70)
    print("检索完成！")
    print("=" * 70)

# ── 5. 交互式查询功能 ────────────────────────────────────────────────

def interactive_query():
    """交互式查询模式"""
    print("=" * 70)
    print("计算机技术发展史交互式检索系统")
    print("=" * 70)
    
    # 构建集合
    print("\n正在加载计算机历史知识库...")
    collection = build_computer_history_collection()
    
    print("\n知识库加载完成！")
    print("输入查询语句（输入 'exit' 或 'quit' 退出）")
    print("-" * 70)
    
    while True:
        try:
            query = input("\n请输入查询: ").strip()
            
            if query.lower() in ['exit', 'quit', '退出']:
                print("感谢使用，再见！")
                break
            
            if not query:
                print("查询不能为空，请重新输入。")
                continue
            
            print(f"\n查询: {query}")
            print("-" * 50)
            
            results = retrieve_computer_history(query, collection)
            
            if not results:
                print("未找到相关结果。")
                continue
            
            for item in results:
                print(f"\n[结果 {item['rank']}] (相似度: {item['similarity']:.4f})")
                print(f"{item['document']}")
                print()
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断。")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")
            print("请重新输入查询。")

# ── 程序入口 ────────────────────────────────────────────────────────

if __name__ == "__main__":
    # 运行主演示程序
    main()
    
    # 如果想要交互式查询，可以取消下面的注释
    # interactive_query()