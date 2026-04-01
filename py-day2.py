# 任务：实现一个并发请求限流器
# 模拟100个API请求，但同时最多只有5个在执行
# 使用 asyncio.Semaphore(5) 实现
import asyncio
import time

async def api_call(i, sem):
    # 使用信号量限制并发请求数量
    async with sem:
        print(f"请求 {i} 开始")
        await asyncio.sleep(0.2)
        print(f"请求 {i} 完成")
        return f"结果 {i}"

# 主函数，创建信号量并执行任务
async def main():
    start_time = time.time()
    # 创建一个信号量，限制同时执行的请求数量为5
    sem = asyncio.Semaphore(5)
    # 创建100个任务，每个任务调用api_call函数
    tasks = [api_call(i, sem) for i in range(1, 101)]
    results = await asyncio.gather(*tasks)
    print(f"全部请求完成，数量: {len(results)}")
    end_time = time.time()
    print(f"总耗时: {end_time - start_time:.2f} 秒")

if __name__ == '__main__':
    asyncio.run(main())
