# -*- coding: utf-8 -*-
"""
OS Course Exp - 1: consumer and producer

Usage:
	python lab-1.py [number of producer] [number of consumer]

1. 场景1
  * 同一进程内启动一组生产者线程和一组消费者线程
  * 缓冲区为本进程的全局变量
2. 场景2
  * 启动一组生产者进程和一组消费者进程
  * 同一个数据文件为缓冲区
"""
from threading import Thread
from multiprocessing import Process, Queue, Semaphore, Lock, Manager
from codecs import encode, decode
from time import sleep
from random import randint
import sys

# init
# Queue object contain a semaphore mechanism itself
LENGTH = 4
SHARE_ZONE = None
FULL = None
EMPTY = None
MUTEX = None
STATUS = None

DOC = __doc__

def producer(num=None, mode=None, output=None):
	"""
	producer
	:type num: int
	:type mode: int
	:type output: Queue
	"""
	while True:
		# roll the dice, if it is 0, do nothing at this cycle
		roll = randint(0, 1)
		if roll == 1:
			with STATUS:
				when_enter = SHARE_ZONE.qsize()
				if when_enter == LENGTH:
					if mode == 1:
						print 'producer ' + str(num) + ': is waiting' + '\n'
					else:
						output.put('producer ' + str(num) + ': is waiting' + '\n')
			FULL.acquire()
			with MUTEX:
				temp = SHARE_ZONE.qsize()
				SHARE_ZONE.put_nowait('data')
				if mode == 1:
					if when_enter == LENGTH:
						print 'producer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp+1) + ' resume' + '\n'
					else:
						print 'producer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp+1) + '\n'
				else:
					if when_enter == LENGTH:
						output.put('producer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp + 1) + ' resume' + '\n', block = True, timeout = 5)
					else:
						output.put('producer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp + 1) + '\n', block = True, timeout = 5)
			EMPTY.release()
		else:
			pass
		sleep(0.5)
	return

def consumer(num=None, mode=None, output=None, ):
	"""
	consumer
	:type num: int
	:type mode: int
	:type output: Queue
	"""
	while True:
		#roll the dice, if it is 0, do nothing at this cycle
		roll = randint(0, 1)
		if roll == 1:
			with STATUS:
				when_enter = SHARE_ZONE.qsize()
				if when_enter == 0:
					if mode == 1:
						print 'consumer ' + str(num) + ': is waiting' + '\n'
					else:
						output.put('consumer ' + str(num) + ': is waiting' + '\n')
			EMPTY.acquire()
			with MUTEX:
				temp = SHARE_ZONE.qsize()
				SHARE_ZONE.get_nowait()
				if mode == 1:
					if when_enter == 0:
						print 'consumer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp-1) + ' resume' + '\n'
					else:
						print 'consumer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp-1) + '\n'
				else:
					if when_enter == 0:
						output.put( 'consumer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp - 1) + ' resume' + '\n', block = True, timeout = 5)
					else:
						output.put( 'consumer ' + str(num) + ': ' + str(temp) + ' -> ' + str(temp - 1) + '\n', block = True, timeout = 5)
			FULL.release()
		else:
			pass
		sleep(0.5)
	return

def main_func(input_argv=None):
	"""
	主函数
	:type input_argv: list
	"""
	if len(input_argv) > 3:
		producer_count = int(input_argv[1])
		consumer_count = int(input_argv[2])
		mode = int(input_argv[3])
		if mode == 1 or mode == 2:
			pass
		else:
			raise ValueError
	else:
		print encode(decode(DOC, 'utf-8'), 'gbk')
		raise NameError
	if mode == 1:
		for i in range(0, producer_count):
			tmp_thread = Thread(target = producer, args=(i+1, mode, ))
			tmp_thread.daemon = True
			tmp_thread.start()
		for i in range(0, consumer_count):
			tmp_thread = Thread(target = consumer, args=(i+1, mode, ))
			tmp_thread.daemon = True
			tmp_thread.start()
		while True:
			pass
	if mode == 2:
		output_file = open('lab-1.result', 'w')
		output = Queue(50)
		process_list = list()
		for i in range(0, producer_count):
			tmp_process = Process(target = producer, args = (i + 1, mode, output, ))
			tmp_process.daemon = True
			tmp_process.start()
			process_list.append(tmp_process.pid)
		for i in range(0, consumer_count):
			tmp_process = Process(target = consumer, args = (i + 1, mode, output, ))
			tmp_process.daemon = True
			tmp_process.start()
			process_list.append(tmp_process.pid)
		while True:
			string = output.get(block = True, timeout = 5)
			print string
			output_file.write(string)
	return

if __name__ == "__main__":
#调用主函数
	manager = Manager()
	SHARE_ZONE = Queue(LENGTH)
	FULL = manager.Semaphore(LENGTH)
	EMPTY = manager.Semaphore(0)
	MUTEX = manager.Lock()
	STATUS = manager.Lock()
	main_func(sys.argv)
