# -*- coding: utf-8 -*-
"""
OS Course Exp - 1: consumer and producer

Usage:
	python lab-1.py [number of producer and consumer]
	
	To prevent ultimate blocking, the input number will set both producer and consumer number
	
	Will automatically setting number to 8 if not specified
"""
from threading import Thread
from threading import Lock
from threading import Semaphore
from time import sleep
import Queue
import random
import sys

# init
# Queue object contain a semaphore mechanism itself
LENGTH = 4
SHARE_ZONE = Queue.Queue(LENGTH)
FULL = Semaphore(LENGTH)
EMPTY = Semaphore(0)
MUTEX = Lock()
STATUS = Lock()
DATA = 'whatever'
RESULT = list()

def producer(num=None):
	"""
	producer
	:type num: int
	"""
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
	"""
	consumer
	:type num: int
	"""
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
	"""
	主函数，生产者数量必须与消费者数量相同，否则会死锁
	:type input_argv: list
	"""
	if len(input_argv) == 1:
		task_count = 8
	elif len(input_argv) > 1:
		task_count = int(input_argv[1])
	else:
		raise ValueError
	outputfile = open('lab-1.result', 'w')

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
		outputfile.close()
	print 'completed !'
	return

if __name__ == "__main__":
#调用主函数
	main_func(sys.argv)
