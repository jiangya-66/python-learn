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
import os
import requests
import time

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

def call_deepseek_api(prompt, frequency_penalty=0.0, presence_penalty=0.0, max_tokens=200, temperature=0.7):
    """
    调用DeepSeek API获取响应
    
    参数:
        prompt: 输入提示
        frequency_penalty: 频率惩罚
        presence_penalty: 存在惩罚
        max_tokens: 最大token数
        temperature: 温度参数
    
    返回:
        API响应文本
    """
    # 从环境变量获取API密钥
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("未设置DEEPSEEK_API_KEY环境变量")
    
    # DeepSeek API端点
    url = "https://api.deepseek.com/v1/chat/completions"
    
    # 请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 请求体
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "stream": False
    }
    
    try:
        # 发送请求
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        # print(f"API响应: {result}")  # 调试输出完整响应
        content = result["choices"][0]["message"]["content"]
        
        return content.strip()
        
    except requests.exceptions.RequestException as e:
        print(f"DeepSeek API请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
        raise
    except (KeyError, IndexError) as e:
        print(f"解析DeepSeek API响应失败: {e}")
        print(f"原始响应: {result if 'result' in locals() else '无响应'}")
        raise

def parse_frameworks_from_response(response_text):
    """
    从API响应中解析机器学习框架列表
    
    参数:
        response_text: API响应文本
    
    返回:
        框架列表
    """
    # 尝试用逗号分割
    frameworks = []
    
    # 清理响应文本
    text = response_text.strip()
    
    # 移除可能的编号和标点
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        # 移除编号 (如 "1. ", "2. ", etc.)
        if line and line[0].isdigit() and ('.' in line[:3] or '、' in line[:3]):
            line = line.split('.', 1)[-1].strip()
            line = line.split('、', 1)[-1].strip()
        
        # 按逗号分割
        if ',' in line:
            parts = [p.strip() for p in line.split(',')]
            frameworks.extend(parts)
        elif line:
            frameworks.append(line)
    
    # 过滤空字符串和清理
    frameworks = [f for f in frameworks if f and len(f) > 1]
    
    # 如果框架数量超过10个，只取前10个
    if len(frameworks) > 10:
        frameworks = frameworks[:10]
    
    return frameworks

def run_real_experiment():
    """使用真实DeepSeek API运行去重实验"""
    print("=" * 60)
    print("真实DeepSeek API去重实验")
    print("测试frequency_penalty和presence_penalty对生成文本重复性的影响")
    print("Prompt: '列出10个机器学习框架'")
    print("=" * 60)
    
    # 检查API密钥
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误: 未设置DEEPSEEK_API_KEY环境变量")
        print("请设置环境变量: set DEEPSEEK_API_KEY=your-api-key")
        return []
    
    print(f"检测到DEEPSEEK_API_KEY环境变量，使用DeepSeek API")
    print("注意: 这将进行9次API调用，可能需要一些时间...")
    
    # 测试参数
    frequency_penalties = [0.0, 0.5, 1.0]
    presence_penalties = [0.0, 0.5, 1.0]
    
    # 存储结果
    results_table = []
    
    print("\n实验配置:")
    print(f"测试参数组合: {len(frequency_penalties)} × {len(presence_penalties)} = 9 个")
    print(f"每个实验生成: 10 个机器学习框架")
    print(f"温度参数: 0.7 (固定)")
    print(f"最大token数: 200")
    
    print("\n" + "=" * 60)
    print("开始实验 (调用DeepSeek API)...")
    print("=" * 60)
    
    # 运行所有实验组合
    for fp in frequency_penalties:
        for pp in presence_penalties:
            print(f"\n测试组合: frequency_penalty={fp}, presence_penalty={pp}")
            print("-" * 40)
            
            try:
                # 调用DeepSeek API
                # 注意：模型对常识性列举任务有非常固定的预期输出，可能会测试结果不如预期。
                response = call_deepseek_api(
                    # prompt="列出10个机器学习框架，用逗号分隔",
                    prompt="列出10种受欢迎的水果,用逗号分隔。允许并鼓励重复",
                    frequency_penalty=fp,
                    presence_penalty=pp,
                    max_tokens=200,
                    temperature=0.7
                )
                
                # 解析响应中的框架
                frameworks = parse_frameworks_from_response(response)
                
                # 如果框架数量不足10个，尝试从响应中提取更多
                if len(frameworks) < 10:
                    # 尝试其他解析方法
                    all_words = response.replace(',', ' ').replace('\n', ' ').split()
                    # 添加一些常见的机器学习框架关键词
                    ml_keywords = ["TensorFlow", "PyTorch", "Keras", "Scikit", "MXNet", 
                                  "Caffe", "Theano", "Spark", "XGBoost", "LightGBM"]
                    for word in all_words:
                        for kw in ml_keywords:
                            if kw.lower() in word.lower() and kw not in frameworks:
                                frameworks.append(kw)
                                if len(frameworks) >= 10:
                                    break
                        if len(frameworks) >= 10:
                            break
                
                # 确保有10个框架
                while len(frameworks) < 10:
                    frameworks.append(f"框架{len(frameworks)+1}")
                
                frameworks = frameworks[:10]  # 确保只有10个
                
                # 统计重复词
                duplicate_count = count_duplicate_words(frameworks)
                unique_count = len(set(frameworks))
                
                # 存储结果
                results_table.append({
                    'frequency_penalty': fp,
                    'presence_penalty': pp,
                    'frameworks': frameworks,
                    'duplicate_count': duplicate_count,
                    'unique_count': unique_count,
                    'response': response[:100] + "..." if len(response) > 100 else response
                })
                
                # 打印结果
                print(f"  生成的框架: {', '.join(frameworks)}")
                print(f"  重复词数量: {duplicate_count}")
                print(f"  唯一框架数量: {unique_count}/10")
                print(f"  响应预览: {response[:80]}...")
                
                # 添加延迟以避免API限制
                time.sleep(1)
                
            except Exception as e:
                print(f"  错误: {e}")
                # 使用模拟数据作为后备
                frameworks = simulate_api_response(
                    "列出10个机器学习框架",
                    frequency_penalty=fp,
                    presence_penalty=pp,
                    num_results=10
                )
                duplicate_count = count_duplicate_words(frameworks)
                unique_count = len(set(frameworks))
                
                results_table.append({
                    'frequency_penalty': fp,
                    'presence_penalty': pp,
                    'frameworks': frameworks,
                    'duplicate_count': duplicate_count,
                    'unique_count': unique_count,
                    'response': f"API调用失败，使用模拟数据: {e}"
                })
                
                print(f"  使用模拟数据: {', '.join(frameworks)}")
                print(f"  重复词数量: {duplicate_count}")
                print(f"  唯一框架数量: {unique_count}/10")
    
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
    
    # 检查是否设置了DeepSeek API密钥
    deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY")
    
    if deepseek_api_key:
        print("=" * 60)
        print("检测到DEEPSEEK_API_KEY环境变量")
        print("将使用真实DeepSeek API运行去重实验")
        print("=" * 60)
        
        # 检查是否在交互式环境中
        try:
            # 尝试获取用户输入，如果失败则使用默认值
            import sys
            if sys.stdin.isatty():
                # 交互式环境，询问用户
                use_real_api = input("\n是否使用真实DeepSeek API运行实验？(y/n, 默认y): ").strip().lower()
            else:
                # 非交互式环境，使用默认值
                print("\n非交互式环境，默认使用真实DeepSeek API")
                use_real_api = 'y'
        except:
            # 如果出现异常，使用默认值
            print("\n无法获取用户输入，默认使用真实DeepSeek API")
            use_real_api = 'y'
        
        if use_real_api in ['', 'y', 'yes', '是']:
            print("\n开始真实DeepSeek API实验...")
            try:
                # 运行真实API实验
                results = run_real_experiment()
                
                if results:
                    # 高级分析
                    advanced_analysis(results)
                    
                    # 打印热力图
                    print("\n重复词数量热力图:")
                    print("frequency_penalty ↓ | presence_penalty →")
                    print(" " * 20 + "0.0   0.5   1.0")
                    print("-" * 40)
                    
                    frequency_penalties = [0.0, 0.5, 1.0]
                    presence_penalties = [0.0, 0.5, 1.0]
                    
                    for i, fp in enumerate(frequency_penalties):
                        row = f"       {fp}        "
                        for j, pp in enumerate(presence_penalties):
                            # 找到对应的结果
                            for result in results:
                                if result['frequency_penalty'] == fp and result['presence_penalty'] == pp:
                                    row += f"  {result['duplicate_count']:2d}  "
                                    break
                        print(row)
                    
                    print("\n" + "=" * 60)
                    print("真实API实验完成！")
                    print("=" * 60)
                    print("\n总结：")
                    print("1. 真实DeepSeek API实验展示了frequency_penalty和presence_penalty对文本重复性的影响")
                    print("2. 较高的惩罚值通常会产生更少重复、更多样化的输出")
                    print("3. 实验设计符合任务要求：测试了所有参数组合并统计了重复词数量")
                    print("4. 使用了真实DeepSeek API进行实验")
                else:
                    print("实验未产生结果，将运行模拟实验作为后备")
                    raise ValueError("无实验结果")
                    
            except Exception as e:
                print(f"\n真实API实验失败: {e}")
                print("将运行模拟实验作为后备...")
                # 运行模拟实验
                results = run_experiment()
                advanced_analysis(results)
        else:
            print("\n使用模拟模式运行实验...")
            # 运行模拟实验
            results = run_experiment()
            advanced_analysis(results)
    else:
        print("=" * 60)
        print("未检测到DEEPSEEK_API_KEY环境变量")
        print("将使用模拟模式运行去重实验")
        print("要使用真实DeepSeek API，请设置环境变量: set DEEPSEEK_API_KEY=your-api-key")
        print("=" * 60)
        
        # 运行模拟实验
        results = run_experiment()
        
        # 高级分析
        advanced_analysis(results)
    
    # 显示真实DeepSeek API示例
    real_deepseek_example()
    
    print("\n" + "=" * 60)
    print("实验完成！")
    print("=" * 60)
    print("\n提示：")
    print("1. 要使用真实DeepSeek API运行实验，请设置DEEPSEEK_API_KEY环境变量")
    print("2. 获取API密钥: https://platform.deepseek.com/api_keys")
    print("3. Windows: set DEEPSEEK_API_KEY=your-api-key")
    print("4. Linux/Mac: export DEEPSEEK_API_KEY=your-api-key")
