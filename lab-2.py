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

TYPE_OF_RESOURCE = 6
MAX_RESOURCE = 400
MIN_RESOURCE = 50
NUM_OF_PROCESS = 15

MAX_P_VALUE = 20
MIN_P_VALUE = 10

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
	def __init__(self, type_num=None, min_value=None, max_value=None, avail_alloc=None):
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
			resource = ProcessAttr(min_value[i], max_value[i], avail_alloc[i])
			self.res.append(resource)
			resource = None
		return

class ProcessAttr(object):
	'''
	Process Attribute
	'''
	def __init__(self, min_value=None, max_value=None, avail_alloc=None):
		self.max = int()
		self.allocation = int()
		self.need = int()
		self.generate(min_value, max_value, avail_alloc)
	def generate(self, min_value=None, max_value=None, avail_alloc=None):
		'''
		using module random to generate the process attribute
		'''
		if max_value != None and min_value != None:
			# ajust here if dead lock happened too much
			self.max = randint(min_value, max_value)
			if self.max < avail_alloc:
				self.allocation = randint(min_value, self.max)
			else:
				self.allocation = randint(min_value, avail_alloc)
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
	process_list = list()
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
	max_list = list()
	for j in range(0, TYPE_OF_RESOURCE):
		max_list.append(randint(0, system_res.resource[j]))
	for i in range(0, NUM_OF_PROCESS):
		temp = Process(TYPE_OF_RESOURCE, min_list, max_list, system_res.available)
		temp.name = 'Process' + str(i).rjust(3)
		for j in range(0, TYPE_OF_RESOURCE):
			system_res.available[j] = system_res.available[j] - temp.res[j].allocation
		process_list.append(temp)
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
	# dead lock generator, will make dead lock more frequent
	# for i in range(0, TYPE_OF_RESOURCE):
	# 	minus = randint(0, system_res.available[j])
	# 	system_res.available[j] = system_res.available[j] - minus
	# 	system_res.resource[j] = system_res.resource[j] - minus
	'''
	add coustom process resource info here

	process_list[0] = Process()
	process_list[0].res[0].max = int()
	process_list[0].res[0].allocation = int()
	process_list[0].res[0].need = int()
	process_list[0].res[1]
	...
	process_list[0].res[n]
	process_list[0].name = ''
	process_list[1]
	...
	process_list[n]

	for i in range(0, len(process_list)):
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
		# a list that log all process that a going to pop from the process_list at the end of this cycle
		pop_list = list()
		for proc in process_list:
			for i in range(0, TYPE_OF_RESOURCE):
				if proc.res[i].need > system_res.available[i]:
					break
				else:
					# tell if this loop is ended by 'break' or ended natruely
					i += 1
			if i != TYPE_OF_RESOURCE:
				continue
			elif i == TYPE_OF_RESOURCE:
				pop_list.append(proc)
		# pop one Process a time, randomly. this can get us different safe queue
		for i in range(0, len(pop_list)):
			i = randint(0, len(pop_list)-1)
			temp = process_list.index(pop_list[i])
			output_line.append(pop_list[i].name + '\n')
			for j in range(0, TYPE_OF_RESOURCE):
				system_res.available[j] = system_res.available[j] + pop_list[i].res[j].allocation
			process_list.pop(temp)
			break
		count = len(process_list)
		# see if dead lock happened
		if len(pop_list) == 0:
			output_line.append('!!!DEAD LOCK !!! \n')
			return False
	for line in output_line:
		print line
	outputfile = open('lab-2.result', 'w')
	outputfile.writelines(output_line)
	outputfile.close()
	return True

if __name__ == "__main__":
	# 输出一种可调度状态
	STATUS = main_func()
	while STATUS is False:
		STATUS = main_func()

	'''
	# 输出一种死锁状态
	while STATUS is True:
		STATUS = main_func()
	''

  