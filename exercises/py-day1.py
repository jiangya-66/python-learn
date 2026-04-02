# # 编写协程函数，分别输出0到10之间的偶数和奇数，间隔1秒钟。
# import asyncio

# async def print_evens():
#     for i in range(0, 11, 2):
#         print("偶数",i)
#         await asyncio.sleep(1)

# async def print_odds():
#     for i in range(1, 11, 2):
#         print("奇数",i)
#         await asyncio.sleep(1)

# async def main():
#     await asyncio.gather(print_evens(), print_odds())

# asyncio.run(main()) 

# 任务：写3个异步函数，分别模拟不同的IO操作（如网络请求、文件读取、数据库查询）
# 然后用 asyncio.gather() 并发执行它们

import asyncio
import aiohttp
import aiofiles
import time

async def network_request():
    """使用aiohttp模拟网络请求"""
    print("开始网络请求...")
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get') as response:
            data = await response.json()
            print("网络请求完成")
            return f"网络请求结果: {data['url']}"

async def file_read():
    """使用aiofiles模拟文件读取"""
    print("开始文件读取...")
    # 读取当前文件自身作为示例
    async with aiofiles.open(__file__, 'r', encoding='utf-8') as f:
        content = await f.read()
        print("文件读取完成")
        return f"文件读取结果: 读取了 {len(content)} 个字符"

async def db_query():
    """模拟数据库查询"""
    print("开始数据库查询...")
    await asyncio.sleep(1.5)  # 模拟1.5秒的数据库查询延迟
    print("数据库查询完成")
    return "数据库查询结果"

async def main():
    print("开始并发执行IO操作...")
    start_time = time.time()
    results = await asyncio.gather(
        network_request(),
        file_read(),
        db_query()
    )
    end_time = time.time()
    print("所有操作完成，结果：", results)
    print(f"总执行时间: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    asyncio.run(main())

