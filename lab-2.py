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
from copy import deepcopy

TYPE_OF_RESOURCE = 8
MAX_RESOURCE = 400
MIN_RESOURCE = 50
NUM_OF_PROCESS = 20

MAX_P_VALUE = 20
MIN_P_VALUE = 10

PROCESS_LIST = list()

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
		elif type != None and max_res is None and min_res is None:
			max_res = MAX_RESOURCE
			min_res = MIN_RESOURCE
		elif type != None and max_res != None and min_res != None:
			pass
		else:
			raise ValueError
		for _ in range(0, type_num):
			rand_num = randint(min_res, max_res)
			self.resource.append(rand_num)
			# don't forget to change here if you want to change the init value of system available resource
			self.available = deepcopy(self.resource)
		return

class Process(object):
	'''
	Process
	'''
	def __init__(self, type_num=None, min_value=None, max_value=None):
		'''
		the input min_value and max_value should be a list
		'''
		if type_num is None and min_value is None and max_value is None:
			type_num = TYPE_OF_RESOURCE
			min_value = MIN_P_VALUE
			max_value = MAX_P_VALUE
		elif type_num != None and min_value is None and max_value is None:
			min_value = MIN_P_VALUE
			max_value = MAX_P_VALUE
		elif type_num != None and min_value != None and max_value != None:
			pass
		else:
			raise ValueError

		self.res = list()
		self.name = str()
		for i in range(0, type_num):
			resource = ProcessAttr(min_value[i], max_value[i])
			self.res.append(resource)
			resource = None
		return

class ProcessAttr(object):
	'''
	Process Attribute
	'''
	def __init__(self, min_value=None, max_value=None):
		self.max = int()
		self.allocation = int()
		self.need = int()
		self.generate(min_value, max_value)
	def generate(self, min_value=None, max_value=None):
		'''
		using module random to generate the process attribute
		'''
		if max_value != None and min_value != None:
			self.max = randint(min_value, max_value)
			# ajust here to get a better look of resource allocation
			self.allocation = randint(min_value, self.max)
			self.need = self.max - self.allocation
		elif max_value is None and min_value is None:
			self.max = randint(MIN_P_VALUE, MAX_P_VALUE)
			self.allocation = randint(MIN_P_VALUE, self.max)
			self.need = self.max - self.allocation
		else:
			raise ValueError

def main_func():
	'''
	主函数
	'''
	#output_list = list()
	output_line = list()
	system_res = System()
	'''
	add coustom system resource info here

	system_res.resource = []
	system_res.available = []
	'''
	# min value of a allocation resource of a process's max
	min_list = list()
	for _ in range(0, TYPE_OF_RESOURCE):
		min_list.append(0)
	# init process in this system
	for i in range(0, NUM_OF_PROCESS):
		temp = Process(TYPE_OF_RESOURCE, min_list, randint(system_res.available, system_res.resource))
		temp.name = 'Process' + str(i).rjust(3)
		for j in range(0, TYPE_OF_RESOURCE):
			system_res.available[j] = system_res.available[j] - temp.res[j].allocation
			if system_res.available[j] < 0:
				system_res.available[j] = 0
		PROCESS_LIST.append(temp)
		# output the init state of all process
		max_attr = ' max -'
		allocation_attr = ' allocation -'
		need_attr = ' need -'
		for j in range(0, TYPE_OF_RESOURCE):
			max_attr = max_attr + str(temp.res[j].max).rjust(4)
			allocation_attr = allocation_attr + str(temp.res[j].allocation).rjust(4)
			need_attr = need_attr + str(temp.res[j].need).rjust(4)
		line = temp.name + ':' + max_attr + allocation_attr + need_attr + '\n'
		output_line.append(line)
	'''
	add coustom process resource info here

	PROCESS_LIST[0] = Process()
	PROCESS_LIST[0].res[0].max = int()
	PROCESS_LIST[0].res[0].allocation = int()
	PROCESS_LIST[0].res[0].need = int()
	PROCESS_LIST[0].res[1]
	...
	PROCESS_LIST[0].res[n]
	PROCESS_LIST[0].name = ''
	PROCESS_LIST[1]
	...
	PROCESS_LIST[n]

	for i in range(0, len(PROCESS_LIST)):
		max_attr = ' max -'
		allocation_attr = ' allocation -'
		need_attr = ' need -'
		for j in range(0, TYPE_OF_RESOURCE):
			max_attr = max_attr + str(temp.res[j].max).rjust(4)
			allocation_attr = allocation_attr + str(temp.res[j].allocation).rjust(4)
			need_attr = need_attr + str(temp.res[j].need).rjust(4)
		line = temp.name + ':' + max_attr + allocation_attr + need_attr + '\n'
		output_line.append(line)
		del max_attr
		del allocation_attr
		del need_attr
		del line
		del temp
	'''
	# output the init state of system
	resource_attr = ' resource -'
	available_attr = ' available -'
	for j in range(0, TYPE_OF_RESOURCE):
		resource_attr = resource_attr + str(system_res.resource[j]).rjust(4)
		available_attr = available_attr + str(system_res.available[j]).rjust(4)
	line = '\nSystem :' + resource_attr + available_attr + '\n\n'
	output_line.append(line)
	# banker's algorithm
	count = NUM_OF_PROCESS
	while count != 0:
		# a list that log all process that a going to pop from the PROCESS_LIST at the end of this cycle
		pop_list = list()
		for proc in PROCESS_LIST:
			for i in range(0, TYPE_OF_RESOURCE):
				if proc.res[i].need > system_res.available[i]:
					break
				else:
					# tell if this loop is ended by 'break' or ended natruely
					i += 1
			if i != TYPE_OF_RESOURCE:
				continue
			elif i == TYPE_OF_RESOURCE:
				output_line.append(proc.name + '\n')
				pop_list.append(proc)
				for j in range(0, TYPE_OF_RESOURCE):
					system_res.available[j] = system_res.available[j] + proc.res[j].allocation
		# pop
		for i in range(0, len(pop_list)):
			temp = PROCESS_LIST.index(pop_list[i])
			PROCESS_LIST.pop(temp)
		count = len(PROCESS_LIST)
		# see if dead lock happened
		if len(pop_list) == 0:
			output_line.append('!!!DEAD LOCK !!! \n')
			break
	for line in output_line:
		print line
	outputfile = open('lab-2.result', 'w')
	outputfile.writelines(output_line)
	outputfile.close()

if __name__ == "__main__":
	# 调用主函数
	main_func()
  