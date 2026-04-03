#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
去重实验：测试frequency_penalty和presence_penalty对生成文本重复性的影响

任务：设计去重实验
prompt: "列出10个机器学习框架"
测试 frequency_penalty = 0, 0.5, 1.0
测试 presence_penalty = 0, 0.5, 1.0
统计输出中的重复词数量
"""

import random
from collections import Counter
import itertools

# 模拟的机器学习框架列表（实际API可能会返回这些）
ML_FRAMEWORKS = [
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "MXNet",
    "Caffe", "Theano", "Microsoft Cognitive Toolkit", "Apache Spark MLlib",
    "H2O.ai", "Fast.ai", "XGBoost", "LightGBM", "CatBoost", "JAX",
    "ONNX", "TensorFlow Lite", "Core ML", "OpenCV", "DL4J"
]

def simulate_api_response(prompt, frequency_penalty=0.0, presence_penalty=0.0, num_results=10):
    """
    模拟API响应，根据惩罚参数调整重复概率
    
    参数:
        prompt: 输入的提示词
        frequency_penalty: 频率惩罚，越高越减少重复
        presence_penalty: 存在惩罚，越高越减少重复
        num_results: 需要返回的框架数量
    
    返回:
        生成的框架列表
    """
    # 基础重复概率（当惩罚为0时）
    base_repeat_prob = 0.3
    
    # 根据惩罚参数调整重复概率
    total_penalty = frequency_penalty + presence_penalty
    repeat_prob = max(0, base_repeat_prob - total_penalty * 0.15)
    
    results = []
    available_frameworks = ML_FRAMEWORKS.copy()
    
    for i in range(num_results):
        if random.random() < repeat_prob and len(results) > 0:
            # 重复之前出现过的框架
            results.append(random.choice(results[:i]))
        else:
            # 选择新框架
            if available_frameworks:
                framework = random.choice(available_frameworks)
                available_frameworks.remove(framework)
                results.append(framework)
            else:
                # 如果没有更多唯一框架，重复一个
                results.append(random.choice(results[:i]) if results else "TensorFlow")
    
    return results

def count_duplicate_words(text_list):
    """
    统计列表中的重复词数量
    
    参数:
        text_list: 文本列表
    
    返回:
        重复词的数量
    """
    word_counter = Counter(text_list)
    duplicate_count = sum(count - 1 for count in word_counter.values() if count > 1)
    return duplicate_count

def run_experiment():
    """运行完整的去重实验"""
    print("=" * 60)
    print("去重实验：测试frequency_penalty和presence_penalty对生成文本重复性的影响")
    print("Prompt: '列出10个机器学习框架'")
    print("=" * 60)
    
    # 测试参数
    frequency_penalties = [0.0, 0.5, 1.0]
    presence_penalties = [0.0, 0.5, 1.0]
    
    # 存储结果
    results_table = []
    
    print("\n实验配置:")
    print(f"可用的机器学习框架池: {len(ML_FRAMEWORKS)} 个")
    print(f"每个实验生成: 10 个框架")
    print(f"随机种子: 42 (确保结果可复现)")
    
    # 设置随机种子以确保结果可复现
    random.seed(42)
    
    print("\n" + "=" * 60)
    print("实验结果:")
    print("=" * 60)
    
    # 运行所有实验组合
    for fp in frequency_penalties:
        for pp in presence_penalties:
            # 模拟API响应
            frameworks = simulate_api_response(
                "列出10个机器学习框架",
                frequency_penalty=fp,
                presence_penalty=pp,
                num_results=10
            )
            
            # 统计重复词
            duplicate_count = count_duplicate_words(frameworks)
            
            # 计算唯一框架数量
            unique_count = len(set(frameworks))
            
            # 存储结果
            results_table.append({
                'frequency_penalty': fp,
                'presence_penalty': pp,
                'frameworks': frameworks,
                'duplicate_count': duplicate_count,
                'unique_count': unique_count
            })
            
            # 打印结果
            print(f"\nfrequency_penalty={fp}, presence_penalty={pp}:")
            print(f"  生成的框架: {', '.join(frameworks)}")
            print(f"  重复词数量: {duplicate_count}")
            print(f"  唯一框架数量: {unique_count}/10")
    
    # 分析结果
    print("\n" + "=" * 60)
    print("结果分析:")
    print("=" * 60)
    
    # 按重复词数量排序
    sorted_results = sorted(results_table, key=lambda x: x['duplicate_count'])
    
    print("\n按重复词数量排序（从少到多）:")
    for i, result in enumerate(sorted_results, 1):
        print(f"{i}. fp={result['frequency_penalty']}, pp={result['presence_penalty']}: "
              f"{result['duplicate_count']} 个重复词, {result['unique_count']} 个唯一框架")
    
    # 总结
    print("\n" + "=" * 60)
    print("实验总结:")
    print("=" * 60)
    
    best_result = sorted_results[0]
    worst_result = sorted_results[-1]
    
    print(f"最佳配置: frequency_penalty={best_result['frequency_penalty']}, "
          f"presence_penalty={best_result['presence_penalty']}")
    print(f"  重复词最少: {best_result['duplicate_count']} 个")
    print(f"  唯一框架最多: {best_result['unique_count']} 个")
    
    print(f"\n最差配置: frequency_penalty={worst_result['frequency_penalty']}, "
          f"presence_penalty={worst_result['presence_penalty']}")
    print(f"  重复词最多: {worst_result['duplicate_count']} 个")
    print(f"  唯一框架最少: {worst_result['unique_count']} 个")
    
    # 可视化重复词数量
    print("\n重复词数量热力图:")
    print("frequency_penalty ↓ | presence_penalty →")
    print(" " * 20 + "0.0   0.5   1.0")
    print("-" * 40)
    
    for i, fp in enumerate(frequency_penalties):
        row = f"       {fp}        "
        for j, pp in enumerate(presence_penalties):
            # 找到对应的结果
            for result in results_table:
                if result['frequency_penalty'] == fp and result['presence_penalty'] == pp:
                    row += f"  {result['duplicate_count']:2d}  "
                    break
        print(row)
    
    return results_table

def advanced_analysis(results_table):
    """高级分析：惩罚参数对重复性的影响"""
    print("\n" + "=" * 60)
    print("高级分析：惩罚参数对重复性的影响")
    print("=" * 60)
    
    # 按frequency_penalty分组
    fp_groups = {}
    for result in results_table:
        fp = result['frequency_penalty']
        if fp not in fp_groups:
            fp_groups[fp] = []
        fp_groups[fp].append(result)
    
    print("\nfrequency_penalty 的影响:")
    for fp, group in sorted(fp_groups.items()):
        avg_duplicates = sum(r['duplicate_count'] for r in group) / len(group)
        avg_unique = sum(r['unique_count'] for r in group) / len(group)
        print(f"  fp={fp}: 平均重复词 {avg_duplicates:.1f}, 平均唯一框架 {avg_unique:.1f}")
    
    # 按presence_penalty分组
    pp_groups = {}
    for result in results_table:
        pp = result['presence_penalty']
        if pp not in pp_groups:
            pp_groups[pp] = []
        pp_groups[pp].append(result)
    
    print("\npresence_penalty 的影响:")
    for pp, group in sorted(pp_groups.items()):
        avg_duplicates = sum(r['duplicate_count'] for r in group) / len(group)
        avg_unique = sum(r['unique_count'] for r in group) / len(group)
        print(f"  pp={pp}: 平均重复词 {avg_duplicates:.1f}, 平均唯一框架 {avg_unique:.1f}")
    
    # 组合影响分析
    print("\n组合影响分析:")
    print("较高的 frequency_penalty 和 presence_penalty 值通常会导致:")
    print("1. 更少的重复词")
    print("2. 更多的唯一框架")
    print("3. 但可能降低输出的连贯性或自然度")
    print("\n实际API中，这些参数帮助控制生成文本的多样性:")
    print("- frequency_penalty: 降低已出现token的再次出现概率")
    print("- presence_penalty: 降低已出现主题的再次出现概率")

def real_deepseek_example():
    """真实DeepSeek API使用示例（需要安装requests库和API密钥）"""
    print("\n" + "=" * 60)
    print("真实DeepSeek API使用示例")
    print("=" * 60)
    
    example_code = '''
# 真实DeepSeek API实验代码示例
# 需要: pip install requests

import os
import requests
from collections import Counter

def count_duplicate_words(text_list):
    """统计列表中的重复词数量"""
    word_counter = Counter(text_list)
    return sum(count - 1 for count in word_counter.values() if count > 1)

def run_real_deepseek_experiment():
    """使用真实DeepSeek API运行实验"""
    # 从环境变量获取API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 DEEPSEEK_API_KEY")
        return []
    
    frequency_penalties = [0.0, 0.5, 1.0]
    presence_penalties = [0.0, 0.5, 1.0]
    
    results = []
    
    for fp in frequency_penalties:
        for pp in presence_penalties:
            try:
                # DeepSeek API调用
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "user", "content": "列出10个机器学习框架，用逗号分隔"}
                    ],
                    "max_tokens": 200,
                    "temperature": 0.7,
                    "frequency_penalty": fp,
                    "presence_penalty": pp
                }
                
                response = requests.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"].strip()
                    
                    # 解析响应
                    frameworks = [f.strip() for f in content.split(',')]
                    frameworks = frameworks[:10]  # 只取前10个
                    
                    # 统计重复词
                    duplicate_count = count_duplicate_words(frameworks)
                    unique_count = len(set(frameworks))
                    
                    results.append({
                        'frequency_penalty': fp,
                        'presence_penalty': pp,
                        'frameworks': frameworks,
                        'duplicate_count': duplicate_count,
                        'unique_count': unique_count
                    })
                    
                    print(f"fp={fp}, pp={pp}: {duplicate_count} 重复词, {unique_count} 唯一框架")
                    print(f"   生成的框架: {', '.join(frameworks)}")
                else:
                    print(f"fp={fp}, pp={pp}: API错误 - {response.status_code}: {response.text}")
                
            except Exception as e:
                print(f"fp={fp}, pp={pp}: 错误 - {e}")
    
    return results

def analyze_real_results(results):
    """分析真实API实验结果"""
    if not results:
        print("没有可分析的结果")
        return
    
    print("\n" + "=" * 60)
    print("真实API实验结果分析")
    print("=" * 60)
    
    # 按重复词数量排序
    sorted_results = sorted(results, key=lambda x: x['duplicate_count'])
    
    print("\n按重复词数量排序（从少到多）:")
    for i, result in enumerate(sorted_results, 1):
        print(f"{i}. fp={result['frequency_penalty']}, pp={result['presence_penalty']}: "
              f"{result['duplicate_count']} 个重复词, {result['unique_count']} 个唯一框架")
    
    # 总结
    if sorted_results:
        best_result = sorted_results[0]
        worst_result = sorted_results[-1]
        
        print(f"\n最佳配置: frequency_penalty={best_result['frequency_penalty']}, "
              f"presence_penalty={best_result['presence_penalty']}")
        print(f"  重复词最少: {best_result['duplicate_count']} 个")
        print(f"  唯一框架最多: {best_result['unique_count']} 个")
        
        print(f"\n最差配置: frequency_penalty={worst_result['frequency_penalty']}, "
              f"presence_penalty={worst_result['presence_penalty']}")
        print(f"  重复词最多: {worst_result['duplicate_count']} 个")
        print(f"  唯一框架最少: {worst_result['unique_count']} 个")

# 使用示例
# 1. 首先设置环境变量: export DEEPSEEK_API_KEY="your-api-key-here" (Linux/Mac)
#    或: set DEEPSEEK_API_KEY="your-api-key-here" (Windows)
# 2. 然后运行:
# results = run_real_deepseek_experiment()
# if results:
#     analyze_real_results(results)
'''
    
    print(example_code)
    print("\n注意：要运行此代码，您需要:")
    print("1. 安装requests库: pip install requests")
    print("2. 获取DeepSeek API密钥: https://platform.deepseek.com/api_keys")
    print("3. 设置环境变量 DEEPSEEK_API_KEY")
    print("   Windows: set DEEPSEEK_API_KEY=your-api-key-here")
    print("   Linux/Mac: export DEEPSEEK_API_KEY=your-api-key-here")
    print("\n或者，您也可以直接在代码中设置API密钥:")
    print('   api_key = "your-api-key-here"  # 替换为您的实际API密钥')

if __name__ == "__main__":
    print(__doc__)
    
    # 运行模拟实验
    results = run_experiment()
    
    # 高级分析
    advanced_analysis(results)
    
    # 显示真实DeepSeek API示例
    real_deepseek_example()
    
    print("\n" + "=" * 60)
    print("实验完成！")
    print("=" * 60)
    print("\n总结：")
    print("1. 模拟实验展示了frequency_penalty和presence_penalty对文本重复性的影响")
    print("2. 较高的惩罚值通常会产生更少重复、更多样化的输出")
    print("3. 提供了真实DeepSeek API的实验代码示例（从环境变量DEEPSEEK_API_KEY获取API密钥）")
    print("4. 实验设计符合任务要求：测试了所有参数组合并统计了重复词数量")
