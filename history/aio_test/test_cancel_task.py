# -*- coding utf-8 -*-
# @Time : 2021/9/17 15:46
# @Author : donghao
# @File : test_cancel_task.py
# @Desc : 测试如何终止各个Task对象
import asyncio
import time


async def do_some_work(x):
    print('Hello do_some_work:', x)
    try:
        await asyncio.sleep(x)
        print('do_some_work({}) is still active'.format(x))  # 如果这句话被打印，证明task仍是active
    except asyncio.CancelledError:
        print('task do_some_work({}) was canceled'.format(x))
    finally:
        await asyncio.sleep(0.5)

def all_tasks_done():
    for t in asyncio.Task.all_tasks():
        if not t.done():
            return False
    return True

async def main():
    try:
        for i in range(5, 10):
            asyncio.create_task(do_some_work(i))
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print('main() was canceled')

print('start...')
start = time.time()
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
end = time.time()
print("total run time: ", end - start)
