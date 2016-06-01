# -*- coding: utf-8 -*-
'''
计算机操作系统，实验一：生产者消费者问题

共享缓冲区中放置一个数字，取值范围为[0, 10]，初值为0。生产者将此值加1，消费者将此值减1。

1. 场景1
  * 同一进程内启动一组生产者线程和一组消费者线程
  * 缓冲区为本进程的全局变量
2. 场景2
  * 启动一组生产者进程和一组消费者进程
  * 同一个数据文件为缓冲区

* 输入
  * `p`：生产者数量
  * `c`：消费者数量
* 输出

  打印当前共享缓冲区中的数值，或者生产者消费者的状态。如
```
Producer 1: 0 -> 1
Consumer 2: 1 -> 0
Consumer 3: waiting
...
Producer 0: 0 -> 1
Consumer 3: (resume) 1 -> 0
...
Producer 1: 9 -> 10
Producer 2: waiting
Consumer 1: 10 -> 9
Producer 2: (resume) 9 -> 10
```
'''
from threading import Thread
from threading import Lock
import Queue
import random
import sys

#init
#Queue object contain a semaphoe machinism itself
SHARE_ZONE = Queue.Queue(10)
READ_SIZE_LOCK = Lock()
FULL_LOCK = Lock()
MUTEX = Lock()
DATA = 'whatever'

def producer(num=None):
	'''
	producer
	'''
	with READ_SIZE_LOCK:
		temp = SHARE_ZONE.qsize()
	SHARE_ZONE.put(DATA)
	print	'producer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp-1)
	return

def consumer(num=None):
	'''
	consumer
	'''
	with READ_SIZE_LOCK:
		temp = SHARE_ZONE.qsize()
	SHARE_ZONE.get(DATA)
	print 'consumer ' + str(num) + ': ' + str(SHARE_ZONE) + ' -> ' + str(temp)
	return

def main_func(input_argv=None):
	'''
	主函数
	'''
	if len(input_argv) < 2:
		task_count = 8
	else:
		task_count = int(input_argv[1])

	remaining = task_count + task_count
	producer_count = task_count
	consumer_count = task_count

	while remaining != 0:
		#roll the dice, if 0 start consumer, if 1 start producer
		#if 0 but no consumer and there is producer remain, start producer
		#if 1 but no producer and there is consumer remain, start consumer
		roll = random.randint(0, 1)
		if (roll == 0 and consumer_count > 0) or (roll == 1 and producer_count <= 0 and consumer_count > 0):
			consumer_count -= 1
			tmp_thread = Thread(target=consumer, args=(consumer_count))
			tmp_thread.start()
			remaining -= 1
		elif (roll == 1 and producer_count > 0) or (roll == 0 and consumer_count <= 0 and producer_count > 0):
			producer_count -= 1
			tmp_thread = Thread(target=producer, args=(producer_count))
			tmp_thread.start()
			remaining -= 1
	print 'completed !'
	return

if __name__ == "__main__":
#调用主函数
	main_func(sys.argv)
