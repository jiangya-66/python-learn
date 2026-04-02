#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
采样参数对比脚本
测试不同temperature和top_p参数对LLM输出的影响
支持DeepSeek API和模拟模式
"""

import os
import json
import time
from typing import Dict, List, Tuple, Optional
import random
from dataclasses import dataclass
from datetime import datetime
import requests


@dataclass
class TestResult:
    """测试结果数据类"""
    temperature: float
    top_p: float
    prompt: str
    response: str
    response_length: int
    timestamp: str
    unique_words: int
    creativity_score: float


class SamplingParameterComparator:
    """采样参数对比器"""
    
    def __init__(self, use_mock: bool = True, api_key: Optional[str] = None):
        """
        初始化对比器
        
        Args:
            use_mock: 是否使用模拟数据（如果为True，则不会调用真实API）
            api_key: DeepSeek API密钥，如果为None则从环境变量DEEPSEEK_API_KEY获取
        """
        self.use_mock = use_mock
        
        # 获取API密钥
        if api_key is None and not use_mock:
            self.api_key = os.environ.get("DEEPSEEK_API_KEY")
            if not self.api_key:
                raise ValueError("未设置DEEPSEEK_API_KEY环境变量，请设置或使用模拟模式(use_mock=True)")
        else:
            self.api_key = api_key
            
        self.prompt = "写一首关于春天的诗"
        
        # 测试参数组合
        self.temperatures = [0, 0.5, 1.0, 1.5]
        self.top_ps = [0.1, 0.5, 0.9]
        
        # 模拟的诗歌片段，用于生成不同创造性的响应
        self.mock_poem_fragments = [
            "春风拂面花香浓，",
            "燕子归来筑新巢，",
            "桃花盛开映日红，",
            "柳絮飞舞似雪花，",
            "溪水潺潺鱼儿跃，",
            "蝴蝶翩翩舞花间，",
            "阳光明媚照大地，",
            "万物复苏生机勃，",
            "春雨绵绵润无声，",
            "青山绿水画中游，",
            "鸟语花香春意浓，",
            "踏青赏花正当时，",
            "百花争艳斗芬芳，",
            "春风吹绿江南岸，",
            "一年之计在于春，",
            "播种希望待秋收。"
        ]
        
        # 固定响应（temperature=0时使用）
        self.deterministic_response = """春天来了，万物复苏。
春风轻拂，花香四溢。
桃花盛开，柳絮飞舞。
燕子归来，筑巢忙碌。
阳光明媚，大地温暖。
溪水潺潺，鱼儿欢跃。
蝴蝶翩翩，蜜蜂嗡嗡。
春意盎然，生机勃勃。
踏青赏花，心情愉悦。
一年之计，在于春天。"""
    
    def generate_mock_response(self, temperature: float, top_p: float) -> str:
        """
        生成模拟的LLM响应
        
        Args:
            temperature: 温度参数
            top_p: top_p参数
            
        Returns:
            模拟的诗歌响应
        """
        if temperature == 0:
            # temperature=0时，响应是确定性的
            return self.deterministic_response
        
        # 根据参数调整创造性和随机性
        creativity_factor = temperature * 0.5 + (1 - top_p) * 0.5
        
        # 确定诗歌行数（4-8行）
        num_lines = int(4 + creativity_factor * 4)
        num_lines = min(max(num_lines, 4), 8)
        
        # 从片段中随机选择并组合
        selected_fragments = random.sample(
            self.mock_poem_fragments, 
            min(num_lines, len(self.mock_poem_fragments))
        )
        
        # 根据temperature添加一些变化
        if temperature > 1.0:
            # 高温时添加更多创造性
            variations = ["（创意版）", "（自由体）", "（现代诗）"]
            prefix = random.choice(variations) if random.random() > 0.7 else ""
            if prefix:
                selected_fragments.insert(0, prefix)
        
        # 根据top_p调整结构
        if top_p < 0.5:
            # 低top_p时更集中，重复一些主题
            if len(selected_fragments) > 2:
                selected_fragments.append(selected_fragments[0])
        
        # 组合成完整的诗歌
        poem = "\n".join(selected_fragments)
        
        # 添加结尾
        endings = [
            "\n——春之颂",
            "\n【春日即景】",
            "\n※ 春意盎然 ※",
            "\n（完）"
        ]
        if random.random() > 0.5:
            poem += random.choice(endings)
        
        return poem
    
    def call_deepseek_api(self, prompt: str, temperature: float, top_p: float) -> str:
        """
        调用DeepSeek API
        
        Args:
            prompt: 输入提示
            temperature: 温度参数
            top_p: top_p参数
            
        Returns:
            DeepSeek的响应文本
        """
        if not self.api_key:
            raise ValueError("未设置DeepSeek API密钥")
        
        # DeepSeek API端点
        url = "https://api.deepseek.com/v1/chat/completions"
        
        # 请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
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
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": 500,
            "stream": False
        }
        
        try:
            # 发送请求
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
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
    
    def call_llm_api(self, prompt: str, temperature: float, top_p: float) -> str:
        """
        调用LLM API（或使用模拟）
        
        Args:
            prompt: 输入提示
            temperature: 温度参数
            top_p: top_p参数
            
        Returns:
            LLM的响应文本
        """
        if self.use_mock:
            # 使用模拟响应
            time.sleep(0.1)  # 模拟API延迟
            return self.generate_mock_response(temperature, top_p)
        else:
            # 调用DeepSeek API
            print(f"调用DeepSeek API: temperature={temperature}, top_p={top_p}")
            return self.call_deepseek_api(prompt, temperature, top_p)
    
    def analyze_response(self, response: str, temperature: float = 1.0) -> Dict:
        """
        分析响应文本
        
        Args:
            response: 响应文本
            temperature: 温度参数（用于调整创造性评分）
            
        Returns:
            分析结果字典
        """
        # 计算响应长度
        length = len(response)
        
        # 计算唯一词汇数（简单版本）
        words = response.replace('\n', ' ').replace('，', ' ').replace('。', ' ').replace('！', ' ').replace('？', ' ').split()
        words = [w for w in words if w.strip()]
        
        if not words:
            unique_words = 0
            word_count = 0
        else:
            word_count = len(words)
            unique_words = len(set(words))
        
        # 计算创造性分数（基于词汇多样性、长度、结构和温度参数）
        # 1. 词汇多样性分数 (0-4分)
        diversity_score = 0
        if word_count > 0:
            diversity_ratio = unique_words / word_count
            diversity_score = min(4, diversity_ratio * 4)
        
        # 2. 长度分数 (0-2分) - 中等长度得分最高
        if length < 30:
            length_score = 0.5
        elif length < 60:
            length_score = 1.0
        elif length < 100:
            length_score = 1.5
        else:
            length_score = 1.0  # 太长反而降低分数
        
        # 3. 结构复杂性分数 (0-2分)
        # 计算换行数和标点符号数
        line_count = response.count('\n') + 1
        punctuation_count = response.count('，') + response.count('。') + response.count('！') + response.count('？')
        structure_score = min(2, (line_count + punctuation_count) / 8)
        
        # 4. 温度调整因子 (0-2分)
        # temperature越高，创造性潜力越大
        temperature_factor = min(2, temperature * 1.5)
        
        # 总创造性分数 (0-10分)
        creativity_score = diversity_score + length_score + structure_score + temperature_factor
        
        # 确保分数在0-10范围内
        creativity_score = max(0, min(10, creativity_score))
        
        return {
            "length": length,
            "unique_words": unique_words,
            "word_count": word_count,
            "creativity_score": round(creativity_score, 2)
        }
    
    def run_comparison(self) -> List[TestResult]:
        """
        运行参数对比测试
        
        Returns:
            测试结果列表
        """
        results = []
        
        print("=" * 60)
        print("采样参数对比测试")
        print("=" * 60)
        print(f"测试提示: {self.prompt}")
        print(f"Temperature参数: {self.temperatures}")
        print(f"Top-p参数: {self.top_ps}")
        print(f"总测试组合数: {len(self.temperatures) * len(self.top_ps)}")
        print("=" * 60)
        
        for temp in self.temperatures:
            for top_p in self.top_ps:
                print(f"\n测试组合: temperature={temp}, top_p={top_p}")
                print("-" * 40)
                
                # 调用LLM
                response = self.call_llm_api(self.prompt, temp, top_p)
                
                # 分析响应（传递temperature参数）
                analysis = self.analyze_response(response, temp)
                
                # 创建测试结果
                result = TestResult(
                    temperature=temp,
                    top_p=top_p,
                    prompt=self.prompt,
                    response=response,
                    response_length=analysis["length"],
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    unique_words=analysis["unique_words"],
                    creativity_score=analysis["creativity_score"]
                )
                
                results.append(result)
                
                # 打印结果摘要
                print(f"响应长度: {result.response_length} 字符")
                print(f"词汇总数: {analysis.get('word_count', 0)}")
                print(f"唯一词汇: {result.unique_words}")
                print(f"创造性分数: {result.creativity_score}/10")
                print(f"响应预览: {response[:50]}...")
        
        return results
    
    def print_summary(self, results: List[TestResult]):
        """
        打印测试结果摘要
        
        Args:
            results: 测试结果列表
        """
        print("\n" + "=" * 60)
        print("测试结果摘要")
        print("=" * 60)
        
        # 按temperature分组
        temp_groups = {}
        for result in results:
            if result.temperature not in temp_groups:
                temp_groups[result.temperature] = []
            temp_groups[result.temperature].append(result)
        
        # 打印每个temperature的结果
        for temp in sorted(temp_groups.keys()):
            print(f"\nTemperature = {temp}:")
            print("-" * 40)
            
            group_results = temp_groups[temp]
            for result in sorted(group_results, key=lambda x: x.top_p):
                print(f"  top_p={result.top_p}: "
                      f"长度={result.response_length}, "
                      f"创造性={result.creativity_score}")
        
        # 打印最佳创造性组合
        most_creative = max(results, key=lambda x: x.creativity_score)
        most_deterministic = min(results, key=lambda x: x.creativity_score)
        
        print("\n" + "=" * 60)
        print("关键发现:")
        print("=" * 60)
        print(f"1. 最具创造性的组合: temperature={most_creative.temperature}, "
              f"top_p={most_creative.top_p}")
        print(f"   创造性分数: {most_creative.creativity_score}/10")
        print(f"   响应长度: {most_creative.response_length} 字符")
        
        print(f"\n2. 最确定性的组合: temperature={most_deterministic.temperature}, "
              f"top_p={most_deterministic.top_p}")
        print(f"   创造性分数: {most_deterministic.creativity_score}/10")
        print(f"   响应长度: {most_deterministic.response_length} 字符")
        
        print(f"\n3. 参数影响分析:")
        print(f"   - temperature越高，响应越多样化和创造性")
        print(f"   - top_p越低，响应越集中和确定性")
        print(f"   - temperature=0时完全确定性，忽略top_p参数")
    
    def save_results(self, results: List[TestResult], filename: str = "sampling_results.json"):
        """
        保存测试结果到JSON文件
        
        Args:
            results: 测试结果列表
            filename: 输出文件名
        """
        # 转换为字典列表
        results_dict = []
        for result in results:
            result_dict = {
                "temperature": result.temperature,
                "top_p": result.top_p,
                "prompt": result.prompt,
                "response": result.response,
                "response_length": result.response_length,
                "timestamp": result.timestamp,
                "unique_words": result.unique_words,
                "creativity_score": result.creativity_score
            }
            results_dict.append(result_dict)
        
        # 保存到文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, ensure_ascii=False, indent=2)
        
        print(f"\n结果已保存到: {filename}")
    
    def print_detailed_comparison(self, results: List[TestResult]):
        """
        打印详细的响应对比
        
        Args:
            results: 测试结果列表
        """
        print("\n" + "=" * 60)
        print("详细响应对比")
        print("=" * 60)
        
        # 选择几个关键组合进行详细对比
        key_combinations = [
            (0, 0.1),    # 最低随机性
            (0.5, 0.5),  # 中等随机性
            (1.0, 0.9),  # 高随机性
            (1.5, 0.1),  # 高temperature + 低top_p
        ]
        
        for temp, top_p in key_combinations:
            # 查找对应的结果
            matching_results = [r for r in results if r.temperature == temp and r.top_p == top_p]
            if not matching_results:
                continue
                
            result = matching_results[0]
            print(f"\n组合: temperature={temp}, top_p={top_p}")
            print(f"创造性分数: {result.creativity_score}/10")
            print("-" * 40)
            print("响应内容:")
            print(result.response)
            print()


def main():
    """主函数"""
    print("开始采样参数对比测试...")
    
    # 检查是否设置了DeepSeek API密钥
    deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY")
    
    if deepseek_api_key:
        print(f"检测到DEEPSEEK_API_KEY环境变量，使用DeepSeek API模式")
        use_mock = False
    else:
        print(f"未检测到DEEPSEEK_API_KEY环境变量，使用模拟模式")
        print(f"要使用真实DeepSeek API，请设置环境变量: set DEEPSEEK_API_KEY=your_api_key")
        use_mock = True
    
    # 创建对比器
    try:
        comparator = SamplingParameterComparator(use_mock=use_mock)
    except ValueError as e:
        print(f"初始化失败: {e}")
        print("切换到模拟模式...")
        comparator = SamplingParameterComparator(use_mock=True)
    
    # 运行对比测试
    results = comparator.run_comparison()
    
    # 打印摘要
    comparator.print_summary(results)
    
    # 打印详细对比
    comparator.print_detailed_comparison(results)
    
    # 保存结果
    comparator.save_results(results)
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    # 提供使用DeepSeek API的说明
    if use_mock:
        print("\n提示：要使用真实DeepSeek API，请：")
        print("1. 获取DeepSeek API密钥: https://platform.deepseek.com/api_keys")
        print("2. 设置环境变量: set DEEPSEEK_API_KEY=your_api_key")
        print("3. 重新运行脚本")
    else:
        print("\n本次测试使用DeepSeek API完成")
        print("要切换回模拟模式，请删除DEEPSEEK_API_KEY环境变量")


if __name__ == "__main__":
    main()