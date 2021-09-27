# -*- coding utf-8 -*-
# @Time : 2021/9/26 17:16
# @Author : donghao
# @File : test_event_loop.py
# @Desc : 测试事件循环的执行规则
import asyncio
import time


async def do_some_work(x):
    try:
        while True:
            print('Hello do_some_work:', x)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print('task do_some_work({}) was canceled'.format(x))

def all_tasks_done():
    for t in asyncio.Task.all_tasks():
        if not t.done():
            return False
    return True

async def main():
    try:
        for i in range(1, 6):
            asyncio.create_task(do_some_work(i))
        while True:
            print("main task:", 0)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print('main() was canceled')

print('start...')
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main())
except KeyboardInterrupt:
    print("键盘中断！")
    for task in asyncio.Task.all_tasks():
        task.cancel()  # 取消所有的Task, 在下轮事件循环中本轮被取消的Task对象将抛出asyncio.CancelledError
    while not all_tasks_done():
        event_loop.stop()  # 停止本次事件循环
        event_loop.run_forever()  # 开启下轮事件循环
finally:
    event_loop.close()




