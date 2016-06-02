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
from threading import Semaphore
from time import sleep
import Queue
import random
import sys

#init
#Queue object contain a semaphoe machinism itself
LENGTH = 4
SHARE_ZONE = Queue.Queue(LENGTH)
FULL = Semaphore(LENGTH)
EMPTY = Semaphore(0)
MUTEX = Lock()
STATUS = Lock()
DATA = 'whatever'
RESULT = list()

def producer(num=None):
	'''
	producer
	'''
	with STATUS:
		when_enter = SHARE_ZONE.qsize()
		if when_enter == LENGTH:
			RESULT.append('producer ' + str(num) + ': is waiting' + '\n')
	FULL.acquire()
	with MUTEX:
		temp = SHARE_ZONE.qsize()
		SHARE_ZONE.put_nowait(DATA)
		if when_enter == LENGTH:
			RESULT.append('producer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp+1) + ' resume' + '\n')
		else:
			RESULT.append('producer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp+1) + '\n')
	EMPTY.release()
	return

def consumer(num=None):
	'''
	consumer
	'''
	with STATUS:
		when_enter = SHARE_ZONE.qsize()
		if when_enter == 0:
			RESULT.append('consumer ' + str(num) + ': is waiting' + '\n')
	EMPTY.acquire()
	with MUTEX:
		temp = SHARE_ZONE.qsize()
		SHARE_ZONE.get_nowait()
		if when_enter == 0:
			RESULT.append('consumer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp-1) + ' resume' + '\n')
		else:
			RESULT.append('consumer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp-1) + '\n')
	FULL.release()
	return

def main_func(input_argv=None):
	'''
	主函数，生产者数量必须与消费者数量相同，否则会死锁
	'''
	if len(input_argv) == 1:
		task_count = 8
	elif len(input_argv) == 2:
		task_count = int(input_argv[1])
	else:
		task_count = int(input_argv[1])
	outputfile = open('result.txt', 'w')

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
			tmp_thread = Thread(target=consumer, args=(consumer_count, ))
			tmp_thread.daemon = True
			tmp_thread.start()
			remaining -= 1
		elif (roll == 1 and producer_count > 0) or (roll == 0 and consumer_count <= 0 and producer_count > 0):
			producer_count -= 1
			tmp_thread = Thread(target=producer, args=(producer_count, ))
			tmp_thread.daemon = True
			tmp_thread.start()
			remaining -= 1
	sleep(2)
	for lines in RESULT:
		print lines
	if outputfile != None:
		outputfile.writelines(RESULT)
	print 'completed !'
	return

if __name__ == "__main__":
#调用主函数
	main_func(sys.argv)
