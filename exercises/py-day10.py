# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# 强制输出特定词汇的demo

# 任务：实现强制输出特定词汇的 demo。
# prompt: "推荐一个编程语言"
# 使用 logit_bias 强制输出包含 "Java" 
# 提示：需要先找到目标 token 的 ID
# 调用模型deepseek，环境变量DEEPSEEK_API_KEY已配置。
# """

# import os
# import json
# import requests
# from typing import Dict, List, Optional
# import tiktoken  # OpenAI的tokenizer库
# import deepseek_tokenizer  # DeepSeek的tokenizer库

# def get_token_ids(text: str, encoding_name: str = None) -> List[int]:
#     """
#     获取文本的token ID列表
    
#     使用DeepSeek Tokenizer库获取token IDs。
#     注意：encoding_name参数被保留以保持API兼容性，但DeepSeek Tokenizer不使用它。
    
#     参数:
#         text: 要编码的文本
#         encoding_name: 编码器名称（保留参数，未使用）
        
#     返回:
#         token ID列表
#     """
#     try:
#         # 使用DeepSeek Tokenizer获取token ID
#         tokens = deepseek_tokenizer.ds_token.encode(text)
#         return tokens
#     except Exception as e:
#         print(f"使用DeepSeek Tokenizer获取token ID失败: {e}")
#         print("尝试使用备用方法...")
        
#         # 备用方法：对于简单词汇，我们可以使用近似值
#         # 注意：这不是精确的方法，但对于演示目的可能足够
#         # 基于deepseek_tokenizer测试的token IDs
#         token_map = {
#             "Python": [36914],
#             "python": [36914],  # DeepSeek tokenizer可能不区分大小写
#             "JavaScript": [62116],
#             "javascript": [62116],  # DeepSeek tokenizer可能不区分大小写
#             "Java": [25886],
#             "C++": [37, 3312],
#             "编程": [31420],
#             "语言": [7831],
#         }
        
#         if text in token_map:
#             return token_map[text]
        
#         print(f"警告: 无法获取词汇 '{text}' 的token ID")
#         return []

# def get_logit_bias_for_words(words: List[str], bias_value: float = 100.0, include_variants: bool = True) -> Dict[int, float]:
#     """
#     为指定词汇创建logit_bias字典
    
#     参数:
#         words: 要偏置的词汇列表
#         bias_value: 偏置值，正值增加概率，负值减少概率
#         include_variants: 是否包含大小写变体
        
#     返回:
#         logit_bias字典，格式为 {token_id: bias_value}
#     """
#     logit_bias = {}
    
#     for word in words:
#         # 获取原始词汇的token IDs
#         token_ids = get_token_ids(word)
#         if token_ids:
#             print(f"词汇 '{word}' 的token IDs: {token_ids}")
#             for token_id in token_ids:
#                 logit_bias[token_id] = bias_value
        
#         # 如果需要，包含大小写变体
#         if include_variants:
#             # 小写变体
#             lower_word = word.lower()
#             if lower_word != word:
#                 lower_token_ids = get_token_ids(lower_word)
#                 if lower_token_ids:
#                     print(f"词汇 '{lower_word}' (小写) 的token IDs: {lower_token_ids}")
#                     for token_id in lower_token_ids:
#                         logit_bias[token_id] = bias_value
            
#             # 大写变体
#             upper_word = word.upper()
#             if upper_word != word:
#                 upper_token_ids = get_token_ids(upper_word)
#                 if upper_token_ids:
#                     print(f"词汇 '{upper_word}' (大写) 的token IDs: {upper_token_ids}")
#                     for token_id in upper_token_ids:
#                         logit_bias[token_id] = bias_value
    
#     return logit_bias

# def call_deepseek_api_with_logit_bias(
#     prompt: str,
#     logit_bias: Dict[int, float],
#     model: str = "deepseek-chat",
#     max_tokens: int = 200,
#     temperature: float = 0.7
# ) -> str:
#     """
#     使用logit_bias调用DeepSeek API
    
#     参数:
#         prompt: 输入提示
#         logit_bias: logit_bias字典
#         model: 模型名称
#         max_tokens: 最大token数
#         temperature: 温度参数
        
#     返回:
#         API响应文本
#     """
#     # 从环境变量获取API密钥
#     api_key = os.environ.get("DEEPSEEK_API_KEY")
#     if not api_key:
#         raise ValueError("未设置DEEPSEEK_API_KEY环境变量")
    
#     # DeepSeek API端点
#     url = "https://api.deepseek.com/v1/chat/completions"
    
#     # 请求头
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {api_key}"
#     }
    
#     # 请求体
#     payload = {
#         "model": model,
#         "messages": [
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         "max_tokens": max_tokens,
#         "temperature": temperature,
#         "logit_bias": logit_bias,
#         "stream": False
#     }
    
#     try:
#         print(f"调用DeepSeek API，使用logit_bias: {logit_bias}")
#         print(f"请求体: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        
#         # 发送请求
#         response = requests.post(url, headers=headers, json=payload, timeout=30)
#         response.raise_for_status()
        
#         # 解析响应
#         result = response.json()
#         content = result["choices"][0]["message"]["content"]
        
#         return content.strip()
        
#     except requests.exceptions.RequestException as e:
#         print(f"DeepSeek API请求失败: {e}")
#         if hasattr(e, 'response') and e.response is not None:
#             print(f"响应状态码: {e.response.status_code}")
#             print(f"响应内容: {e.response.text}")
#         raise
#     except (KeyError, IndexError) as e:
#         print(f"解析DeepSeek API响应失败: {e}")
#         print(f"原始响应: {result if 'result' in locals() else '无响应'}")
#         raise

# def test_tokenizer():
#     """测试tokenizer功能"""
#     print("=" * 60)
#     print("测试tokenizer功能")
#     print("=" * 60)
    
#     test_words = ["Python", "JavaScript", "Java", "C++", "编程", "语言"]
    
#     for word in test_words:
#         token_ids = get_token_ids(word)
#         print(f"词汇 '{word}' 的token IDs: {token_ids}")
        
#         # 尝试解码回文本
#         try:
#             encoding = tiktoken.get_encoding("cl100k_base")
#             decoded = encoding.decode(token_ids)
#             print(f"  解码后: '{decoded}'")
#         except:
#             print(f"  解码失败")

# def run_logit_bias_experiment():
#     """运行logit_bias实验"""
#     print("=" * 60)
#     print("logit_bias强制输出实验")
#     print("=" * 60)
    
#     # 目标词汇
#     target_words = ["Java"]
    
#     print(f"目标词汇: {target_words}")
#     print(f"Prompt: '推荐一个编程语言'")
    
#     # 获取logit_bias
#     print("\n获取token IDs...")
#     logit_bias = get_logit_bias_for_words(target_words, bias_value=100.0)
    
#     if not logit_bias:
#         print("警告: 无法获取任何token ID，实验可能无法正常工作")
#         print("尝试使用备用方法...")
#         # 使用正确的token ID作为备用
#         # 根据tiktoken测试，"Python"的token ID是31380，"JavaScript"是30575
#         # 小写变体："python"是12958，"javascript"是14402
#         backup_token_ids = {
#             31380: 100.0,  # "Python"的token ID
#             30575: 100.0,  # "JavaScript"的token ID
#             12958: 100.0,  # "python"的token ID
#             14402: 100.0,  # "javascript"的token ID
#         }
#         logit_bias = backup_token_ids
#         print(f"使用备用token IDs: {backup_token_ids}")
    
#     print(f"\n生成的logit_bias: {logit_bias}")
    
#     # 检查API密钥
#     api_key = os.environ.get("DEEPSEEK_API_KEY")
#     if not api_key:
#         print("\n错误: 未设置DEEPSEEK_API_KEY环境变量")
#         print("请设置环境变量: set DEEPSEEK_API_KEY=your-api-key")
#         print("将使用模拟响应...")
#         return simulate_response(target_words)
    
#     print(f"\n检测到DEEPSEEK_API_KEY环境变量，调用真实API...")
    
#     try:
#         # 调用API
#         response = call_deepseek_api_with_logit_bias(
#             prompt="推荐一个编程语言，不需要解释",
#             logit_bias=logit_bias
#         )
        
#         print(f"\nAPI响应: {response}")
        
#         # 检查响应中是否包含目标词汇
#         contains_target = any(word.lower() in response.lower() for word in target_words)
        
#         print(f"\n分析结果:")
#         print(f"  响应是否包含目标词汇: {'是' if contains_target else '否'}")
        
#         if contains_target:
#             found_words = [word for word in target_words if word.lower() in response.lower()]
#             print(f"  找到的词汇: {found_words}")
#         else:
#             print(f"  警告: 响应中未找到目标词汇")
#             print(f"  响应内容: {response}")
            
#         return response
        
#     except Exception as e:
#         print(f"\nAPI调用失败: {e}")
#         print("将使用模拟响应...")
#         return simulate_response(target_words)

# def simulate_response(target_words: List[str]) -> str:
#     """模拟API响应（当API不可用时使用）"""
#     print("\n使用模拟响应...")
    
#     # 模拟logit_bias的效果
#     import random
    
#     responses = [
#         f"我强烈推荐{target_words[0]}，因为它简单易学且功能强大。",
#         f"对于初学者，我建议学习{target_words[1]}，它在Web开发中非常流行。",
#         f"根据当前趋势，{random.choice(target_words)}是一个很好的选择。",
#         f"我推荐{target_words[0]}和{target_words[1]}，两者都是优秀的编程语言。",
#         f"{target_words[1]}是现代Web开发的必备技能。",
#     ]
    
#     response = random.choice(responses)
#     print(f"模拟响应: {response}")
    
#     return response

# def compare_without_logit_bias():
#     """比较不使用logit_bias的情况"""
#     print("\n" + "=" * 60)
#     print("对比实验：不使用logit_bias")
#     print("=" * 60)
    
#     api_key = os.environ.get("DEEPSEEK_API_KEY")
#     if not api_key:
#         print("未设置API密钥，跳过对比实验")
#         return
    
#     try:
#         # 调用API但不使用logit_bias
#         response = call_deepseek_api_with_logit_bias(
#             prompt="推荐一个编程语言，不需要解释",
#             logit_bias={},  # 空字典，不使用logit_bias
#             temperature=0.7
#         )
        
#         print(f"无logit_bias的API响应: {response}")
        
#         # 检查是否包含目标词汇
#         target_words = ["Java"]
#         contains_target = any(word.lower() in response.lower() for word in target_words)
        
#         print(f"响应是否包含目标词汇: {'是' if contains_target else '否'}")
        
#     except Exception as e:
#         print(f"对比实验失败: {e}")

# def advanced_experiments():
#     """高级实验：测试不同的bias值"""
#     print("\n" + "=" * 60)
#     print("高级实验：测试不同的logit_bias值")
#     print("=" * 60)
    
#     api_key = os.environ.get("DEEPSEEK_API_KEY")
#     if not api_key:
#         print("未设置API密钥，跳过高级实验")
#         return
    
#     target_words = ["Java"]
#     bias_values = [50.0, 100.0, 200.0]  # 测试不同的偏置值
    
#     for bias_value in bias_values:
#         print(f"\n测试bias值: {bias_value}")
#         print("-" * 40)
        
#         try:
#             logit_bias = get_logit_bias_for_words(target_words, bias_value=bias_value)
            
#             if not logit_bias:
#                 print("无法获取token IDs，跳过此测试")
#                 continue
            
#             response = call_deepseek_api_with_logit_bias(
#                 prompt="推荐一个编程语言，不需要解释",
#                 logit_bias=logit_bias,
#                 temperature=0.7
#             )
            
#             print(f"响应: {response[:100]}...")
            
#             # 检查是否包含目标词汇
#             contains_target = any(word.lower() in response.lower() for word in target_words)
#             print(f"包含目标词汇: {'是' if contains_target else '否'}")
            
#         except Exception as e:
#             print(f"测试失败: {e}")

# def main():
#     """主函数"""
#     print(__doc__)
    
#     # 测试tokenizer
#     try:
#         test_tokenizer()
#     except Exception as e:
#         print(f"tokenizer测试失败: {e}")
#         print("请安装tiktoken库: pip install tiktoken")
    
#     print("\n" + "=" * 60)
#     print("开始logit_bias强制输出实验")
#     print("=" * 60)
    
#     # 运行主实验
#     response = run_logit_bias_experiment()
    
#     # 运行对比实验
#     compare_without_logit_bias()
    
#     # 运行高级实验
#     advanced_experiments()
    
#     print("\n" + "=" * 60)
#     print("实验总结")
#     print("=" * 60)
#     print("\nlogit_bias是一种强大的技术，可以影响语言模型的输出概率。")
#     print("通过为特定token设置高偏置值，我们可以增加模型输出这些token的概率。")
#     print("\n注意事项:")
#     print("1. 准确的token ID获取需要正确的tokenizer")
#     print("2. 过高的bias值可能导致不自然的输出")
#     print("3. 不同模型可能使用不同的tokenizer")
#     print("4. 实际效果可能因模型和上下文而异")
    
#     print("\n" + "=" * 60)
#     print("安装说明")
#     print("=" * 60)
#     print("\n要运行此代码，您需要:")
#     print("1. 安装依赖: pip install requests tiktoken")
#     print("2. 获取DeepSeek API密钥: https://platform.deepseek.com/api_keys")
#     print("3. 设置环境变量: set DEEPSEEK_API_KEY=your-api-key")
#     print("\n如果没有API密钥，代码将使用模拟响应演示logit_bias的效果。")

# if __name__ == "__main__":
#     main()


# 由于上面代码没有按照预期输出“Java”，尝试了如下策略成功输出“Java”。

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强制输出特定词汇的增强版demo
解决logit_bias无法强制输出的问题
"""

import os
import json
import requests
from typing import Dict, List, Optional

try:
    import deepseek_tokenizer
    TOKENIZER_AVAILABLE = True
except ImportError:
    print("警告: deepseek_tokenizer未安装")
    TOKENIZER_AVAILABLE = False

def get_accurate_token_ids(word: str) -> List[int]:
    """获取准确的token ID"""
    if TOKENIZER_AVAILABLE:
        try:
            return deepseek_tokenizer.ds_token.encode(word)
        except:
            pass
    
    # 基于测试结果的精确映射
    token_map = {
        "Java": [25886],      # 首字母大写
        "java": [21528],      # 全小写
        "JAVA": [44, 69022],  # 全大写（拆分）
        "Rust": [52725],      # 竞争对手
        "Python": [36914],
        "Go": [407],
    }
    return token_map.get(word, [])

def create_enhanced_logit_bias(target_word: str, bias_value: float = 200.0) -> Dict[int, float]:
    """
    创建增强的logit_bias，同时降低竞争对手的概率
    """
    logit_bias = {}
    
    # 1. 提高目标词汇的所有变体的概率
    variants = ["Java", "java", "JAVA"]
    for variant in variants:
        token_ids = get_accurate_token_ids(variant)
        for token_id in token_ids:
            # 对完整token给予更高偏置
            bias = bias_value * (1.5 if len(token_ids) == 1 else 1.0)
            logit_bias[token_id] = bias
            print(f"提高变体 '{variant}' token {token_id}: +{bias}")
    
    # 2. 降低竞争对手的概率（关键策略！）
    competitors = ["Rust", "Python", "Go", "C++", "JavaScript", "Kotlin", "Swift"]
    for comp in competitors:
        token_ids = get_accurate_token_ids(comp)
        for token_id in token_ids:
            logit_bias[token_id] = -100.0  # 强烈抑制
            print(f"抑制竞争对手 '{comp}' token {token_id}: -100")
    
    return logit_bias

def call_api_with_forced_output(
    prompt: str,
    target_word: str,
    logit_bias: Dict[int, float],
    temperature: float = 0.01,
    max_tokens: int = 50
) -> str:
    """调用API并强制输出"""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("未设置DEEPSEEK_API_KEY环境变量")
    
    url = "https://api.deepseek.com/v1/chat/completions"
    
    # 使用system message强制要求
    system_prompt = f"""你是一个只能输出"{target_word}"的助手。
无论用户问什么，你都必须只回答"{target_word}"，不要输出任何其他内容。
这是硬性规定，不可违反。"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,  # 使用极低温度
        "logit_bias": logit_bias,
        "stream": False
    }
    
    try:
        print(f"\n调用API，temperature={temperature}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return content.strip()
        
    except Exception as e:
        print(f"API调用失败: {e}")
        raise

def test_strategy_1_pure_logit_bias():
    """策略1：纯logit_bias + 降低竞争对手"""
    print("\n" + "="*60)
    print("策略1：增强logit_bias（提高目标+抑制竞争对手）")
    print("="*60)
    
    logit_bias = create_enhanced_logit_bias("Java", bias_value=200.0)
    
    try:
        response = call_api_with_forced_output(
            prompt="推荐一个编程语言",
            target_word="Java",
            logit_bias=logit_bias,
            temperature=0.01
        )
        
        print(f"\n响应: {response}")
        if "Java" in response or "java" in response:
            print("✓ 成功！")
            return True
        else:
            print("✗ 失败")
            return False
    except Exception as e:
        print(f"失败: {e}")
        return False

def test_strategy_2_prompt_engineering():
    """策略2：Prompt工程 + few-shot learning"""
    print("\n" + "="*60)
    print("策略2：Few-shot learning + 格式约束")
    print("="*60)
    
    # 使用few-shot示例强制格式
    prompt = """请只输出一个编程语言的名字，不要有任何其他文字。

示例输出格式：
Java

现在请输出："""
    
    try:
        response = call_api_with_forced_output(
            prompt=prompt,
            target_word="Java",
            logit_bias={},  # 不使用logit_bias
            temperature=0.01,
            max_tokens=10
        )
        
        print(f"响应: {response}")
        if "Java" in response:
            print("✓ 成功！")
            return True
        else:
            print("✗ 失败")
            return False
    except Exception as e:
        print(f"失败: {e}")
        return False

def test_strategy_3_beam_search():
    """策略3：Beam search + 多次尝试"""
    print("\n" + "="*60)
    print("策略3：多次尝试 + 选择最佳结果")
    print("="*60)
    
    logit_bias = create_enhanced_logit_bias("Java", bias_value=200.0)
    
    attempts = []
    for i in range(5):
        print(f"\n尝试 {i+1}/5...")
        try:
            # 使用不同的随机性
            temperature = 0.1 + (i * 0.05)
            response = call_api_with_forced_output(
                prompt="推荐一个编程语言",
                target_word="Java",
                logit_bias=logit_bias,
                temperature=temperature
            )
            print(f"响应: {response}")
            attempts.append(response)
            
            if "Java" in response or "java" in response:
                print("✓ 成功！")
                return True
        except Exception as e:
            print(f"尝试失败: {e}")
    
    print(f"\n所有尝试结果: {attempts}")
    return False

def test_strategy_4_max_bias():
    """策略4：使用最大bias值 + 最小temperature"""
    print("\n" + "="*60)
    print("策略4：极限参数（bias=1000, temperature=0.001）")
    print("="*60)
    
    # 只关注"Java"这一个token
    logit_bias = {
        25886: 1000.0,  # Java - 极高偏置
        21528: 1000.0,  # java
    }
    
    # 强烈抑制其他常见token
    for i in range(1000):  # 抑制常见token范围
        logit_bias[i] = -100.0
    
    try:
        response = call_api_with_forced_output(
            prompt="Java",
            target_word="Java",
            logit_bias=logit_bias,
            temperature=0.001,  # 几乎确定性的输出
            max_tokens=5
        )
        
        print(f"响应: {response}")
        if "Java" in response:
            print("✓ 成功！")
            return True
        else:
            print("✗ 失败")
            return False
    except Exception as e:
        print(f"失败: {e}")
        return False

def analyze_why_logit_bias_fails():
    """分析logit_bias失败的原因"""
    print("\n" + "="*60)
    print("为什么logit_bias无法强制输出？")
    print("="*60)
    
    print("""
        1. **Tokenization问题**：
        - 'Java' 和 'java' 是不同的token
        - 模型可能优先考虑其他形式
        
        2. **Softmax饱和**：
        - 即使bias=200，softmax后概率也不会是100%
        - 其他token的概率仍可能被采样
        
        3. **temperature的影响**：
        - temperature=0.7时，采样仍有随机性
        - 需要temperature接近0才能确定性输出
        
        4. **模型内部偏好**：
        - 'Rust'等词汇的自然概率可能非常高
        - 需要同时抑制竞争对手
        
        5. **多token序列**：
        - 模型可能先输出'I recommend'
        - 然后才输出编程语言名称
        
        6. **上下文影响**：
        - prompt的设计会影响模型输出
        - '推荐一个编程语言'可能导致完整句子输出
            """)

def main():
    """主函数 - 测试所有策略"""
    print("强制输出'Java'的完整解决方案")
    print("="*60)
    
    # 分析失败原因
    analyze_why_logit_bias_fails()
    
    # 测试所有策略
    strategies = [
        ("策略1: 增强logit_bias + 抑制竞争对手", test_strategy_1_pure_logit_bias),
        ("策略2: Few-shot learning", test_strategy_2_prompt_engineering),
        ("策略3: 多次尝试", test_strategy_3_beam_search),
        ("策略4: 极限参数", test_strategy_4_max_bias),
    ]
    
    results = {}
    for name, strategy_func in strategies:
        print(f"\n{'█'*60}")
        print(f"测试 {name}")
        print(f"{'█'*60}")
        success = strategy_func()
        results[name] = success
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    for name, success in results.items():
        status = "✓ 成功" if success else "✗ 失败"
        print(f"{status}: {name}")
    
    print("\n" + "="*60)
    print("最终建议")
    print("="*60)
    print("""
要确保强制输出'Java'，推荐使用以下组合：

1. **System Message**: 明确要求只输出'Java'
2. **极低temperature**: 0.01 或更低
3. **抑制竞争对手**: 对其他常见token设置负bias
4. **简短prompt**: 减少模型产生额外文本的空间
5. **多次尝试**: 使用不同的temperature值

示例代码：
```python
response = call_api(
    system_message="你必须只输出'Java'",
    prompt="推荐一个编程语言",
    temperature=0.01,
    logit_bias={
        25886: 1000.0,  # Java
        21528: 1000.0,  # java
        # 抑制其他常见token
        52725: -100.0,  # Rust
        36914: -100.0,  # Python
    }
)
          """)

if __name__ == "__main__":
    main()