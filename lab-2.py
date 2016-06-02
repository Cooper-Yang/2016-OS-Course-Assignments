# -*- coding: utf-8 -*-
'''
# 银行家算法程序

* 输入
  * `p`: 进程数量
  * `r`：资源数量
  * 各进程的 `max`, `allocation`

* 输出
  * 若产生死锁，打印提示：`死锁状态`。
  * 否则，给出一种调度顺序。
'''

from random import randint

TYPE_OF_RESOURCE = 4
MAX_RESOURCE = 100
MIN_RESOURCE = 50
NUM_OF_PROCESS = 10
PROCESS_LIST = list()
PROCESS_COUNT = int()

class Node(object):
	'''
	A Node of an unordered link list
	'''
	def __init__(self):
		self.data = ''
		self.next = None

class LinkList(object):
	'''
	an unordered link list
	0				1		2		3		4		...		n
	master												head
	master do not stroage any data

	there is no 'free' or 'clean' to an Node object
	quote:'Once the last reference to an object is gone, the object will be garbage collected'
	'''
	def __init__(self):
		self.master = Node()
		self.head = self.master
		self.len = int()
	def __len__(self):
		return self.len
	def append(self, new_node=None):
		'''
		Append a node to the end of the lisk list
		'''
		self.head.next = new_node
		self.head = new_node
		self.len += 1
		return True
	def delete(self, position=None):
		'''
		Delete the node of the given position
		'''
		if position < self.len:
			return False
		temp = self.master
		#moving temp to the node right before the target node position
		for i in range(0, position-1):
			temp = temp.next
		if position == self.len:
			self.head = temp
			self.len -= 1
			return True
		else:
			temp_next = temp.next.next
			temp.next = temp_next
			self.len -= 1
		return True

class System(object):
	'''
	System Attribute
	'''
	def __init__(self, type_num=None, max_res=None, min_res=None):
		self.resource = list()
		self.available = list()
		self.generate(type_num, max_res, min_res)
	def generate(self, type_num=None, max_res=None, min_res=None):
		'''
		using module random to generate the system attribute
		'''
		if type_num is None and max_res is None and min_res is None:
			type_num = TYPE_OF_RESOURCE
			max_res = MAX_RESOURCE
			min_res = MIN_RESOURCE
		elif max_res is None and min_res is None:
			max_res = MAX_RESOURCE
			min_res = MIN_RESOURCE
		elif type != None and max_res != None and min_res != None:
			pass
		else:
			raise ValueError
		for i in range(0, type_num):
			rand_num = randint(min_res, max_res)
			self.resource.append(rand_num)
			self.available.append(0)
		return

class Process(object):
	'''
	Process Attribute
	'''
	def __init__(self, max_value=None, min_value=None):
		self.max = int()
		self.allocation = int()
		self.need = int()
		self.generate(max_value, min_value)
	def generate(self, max_value=None, min_value=None):
		'''
		using module random to generate the process attribute
		'''
		if max_value != None and min_value != None:
			self.max = randint(min_value, max_value)
			self.allocation = randint(min_value, self.max)
			self.need = self.max - self.allocation
		else:
			raise ValueError

def main_func():
	'''
	主函数
	'''
	system_res = System()
	for i in range(0, NUM_OF_PROCESS):
		pass

if __name__ == "__main__":
	#调用主函数
	main_func()
  