# -*- coding: utf-8 -*-
"""
OS Course Exp - 1: consumer and producer

Usage:
	python lab-1.py [number of producer] [number of consumer] [number of message]

1. 场景1
  * 同一进程内启动一组生产者线程和一组消费者线程
  * 缓冲区为本进程的全局变量
2. 场景2
  * 启动一组生产者进程和一组消费者进程
  * 同一个数据文件为缓冲区
"""
import threading
import multiprocessing
from multiprocessing import Queue
from codecs import encode, decode
from time import sleep
from random import randint
import sys

# init
# Length of Queue object
LENGTH = 4
# number of message you want to display
NUM_OF_MESSAGE = 20

DOC = __doc__

def producer(share_zone=None, full=None, empty=None, mutex=None, status=None, num=None, mode=None, output=None):
	"""
	producer
	:type share_zone: Queue
	:type full: Semaphore
	:type empty: Semaphore
	:type mutex: Lock
	:type status: Lock
	:type num: int
	:type mode: int
	:type output: Queue
	"""
	while True:
		# roll the dice, if it is 0, do nothing at this cycle
		roll = randint(0, 1)
		if roll == 1:
			with status:
				when_enter = share_zone.qsize()
				if when_enter == LENGTH:
					if mode == 1:
						print 'producer ' + str(num) + ': is waiting' + '\n'
					else:
						output.put('producer ' + str(num) + ': is waiting' + '\n')
			full.acquire()
			with mutex:
				temp = share_zone.qsize()
				share_zone.put('data')
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
			empty.release()
		else:
			pass
		sleep(0.5)
	return

def consumer(share_zone=None, full=None, empty=None, mutex=None, status=None, num=None, mode=None, output=None):
	"""
	consumer
	:type full: Semaphore
	:type empty: Semaphore
	:type mutex: Lock
	:type status: Lock
	:type num: int
	:type mode: int
	:type output: Queue
	"""
	while True:
		#roll the dice, if it is 0, do nothing at this cycle
		roll = randint(0, 1)
		if roll == 1:
			with status:
				when_enter = share_zone.qsize()
				if when_enter == 0:
					if mode == 1:
						print 'consumer ' + str(num) + ': is waiting' + '\n'
					else:
						output.put('consumer ' + str(num) + ': is waiting' + '\n')
			empty.acquire()
			with mutex:
				temp = share_zone.qsize()
				share_zone.get()
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
			full.release()
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
		try:
			message_num = int(input_argv[4])
		except IndexError:
			message_num = NUM_OF_MESSAGE
		if mode == 1 or mode == 2:
			pass
		else:
			raise ValueError
	else:
		print encode(decode(DOC, 'utf-8'), 'gbk')
		raise NameError
	if mode == 1:
		share_zone = Queue(LENGTH)
		full = threading.Semaphore(LENGTH)
		empty = threading.Semaphore(0)
		mutex = threading.Lock()
		status = threading.Lock()
		for i in range(0, producer_count):
			tmp_thread = threading.Thread(target=producer, args=(share_zone, full, empty, mutex, status, i+1, mode, ))
			tmp_thread.daemon = True
			tmp_thread.start()
		for i in range(0, consumer_count):
			tmp_thread = threading.Thread(target=consumer, args=(share_zone, full, empty, mutex, status, i+1, mode, ))
			tmp_thread.daemon = True
			tmp_thread.start()
		while True:
			pass
	if mode == 2:
		share_zone = multiprocessing.Queue(LENGTH)
		full = multiprocessing.Semaphore(LENGTH)
		empty = multiprocessing.Semaphore(0)
		mutex = multiprocessing.Lock()
		status = multiprocessing.Lock()
		# open output file
		output_file = open('lab-1.result', 'w')
		output = multiprocessing.Queue(50)
		process_list = list()
		for i in range(0, producer_count):
			tmp_process = multiprocessing.Process(target=producer, args=(share_zone, full, empty, mutex, status, i+1, mode, output, ))
			tmp_process.daemon = True
			tmp_process.start()
			process_list.append(tmp_process)
		for i in range(0, consumer_count):
			tmp_process = multiprocessing.Process(target=consumer, args=(share_zone, full, empty, mutex, status, i+1, mode, output, ))
			tmp_process.daemon = True
			tmp_process.start()
			process_list.append(tmp_process)
		count = 0
		while count < message_num:
			string = output.get(block = True)
			print string
			output_file.write(string)
			count += 1
		output_file.close()

if __name__ == "__main__":
#调用主函数
	main_func(sys.argv)
