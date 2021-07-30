# -*- coding utf-8 -*-
# @Time : 2021/1/4 16:29
# @Author : DH
# @File : test.py.py
# @Software : PyCharm

import asyncio

async def others(time):
    print("start")
    await asyncio.sleep(time)
    print('end')
    return "睡了" + str(time) + "秒"

async def func(time):
    print("执行协程函数内部代码")
    # await等待对象的值得到结果之后再继续向下走
    response = await others(time)
    print("IO请求结束，结果为：", response)

async def count():
    await asyncio.sleep(1)
    for i in range(10):
        print("打印：", i)

task = [func(5), func(2)]
asyncio.run(asyncio.wait(task))


