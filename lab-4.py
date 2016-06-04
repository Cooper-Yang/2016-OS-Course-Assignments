# -*- coding: utf-8 -*-
"""
OS Course Exp - 4: i-Node

Usage:
	python lab-4.py [file_name] [owner] [file_size Byte] [level] [block_size] [record_size] [content fold = 0 or 1]

# 混合索引逻辑地址到物理地址映射

* 条件：自定义混合索引 `inode` 结构
  * 必须包括一次，二次，和三次间接块
  * 逻辑块 `n` 对应物理块 `n`
* 输入：文件逻辑地址
* 输出
  1. 输出 `inode` 详细信息（间接块不展开）
  2. 物理地址（物理块号，块内偏移）
"""
from random import randint
from time import strftime

import sys

TOTAL_BLOCK = 2**32

class System(object):
	"""
	Define system resource
	"""
	def __init__(self, ):
		self.used = set()
	def alloc_block(self):
		"""
		allocate an available block from the system resource randomly, will return the block number
		"""
		block_num = randint(0, TOTAL_BLOCK)
		while block_num in self.used is True:
			block_num = randint(0, TOTAL_BLOCK)
		self.used.add(block_num)
		return block_num
	def free_block(self, block_num=None):
		"""
		do not free an unused block !!!
		:type block_num: int
		"""
		temp = list(self.used)
		temp.pop(temp.index(block_num))
		self.used = set(temp)
		return

SYSTEM = System()

class Block(object):
	"""
	Data Block
	"""
	def __init__(self, num=None, num_of_record=None):
		"""
		:type num: int
		:type num_of_record: int
		"""
		self.num = num
		self.data = list()
		self.num_of_record = num_of_record
	def data_append(self, input_data):
		"""
		:type input_data: int
		"""
		self.data.append(input_data)
	def get_content(self, offset=None):
		"""
		get content of specified offset
		:type offset: int
		"""
		temp = list(self.data)
		return temp[offset]

class BlockIndex(object):
	"""
	Structure of direct and indirect block index
	"""
	def __init__(self, level=None, data_size=None, block_size=None, record_size=None, record_list=None):
		"""
		:type level: int
		:type data_size: int
		:type block_size: int
		:type record_size: int
		:type record_list: list
		"""
		self.data_size = data_size
		# is 0 if is direct
		self.level_num = level
		self.index_list = list()
		self.block_list = list()
		if level == 0 and record_list is None:
			self.num_of_record = None
			self.record_per_block = None
			self.block_size = block_size
			if data_size % block_size != 0:
				self.num_of_block = data_size / block_size + 1
			else:
				self.num_of_block = data_size / block_size
			# allocation direct block
			temp_a = 0
			while temp_a < self.num_of_block:
				self.index_list.append(SYSTEM.alloc_block())
				temp_a += 1
			self.index_list.sort()
		elif level > 0 and record_list is not None:
			self.block_size = block_size
			self.record_size = record_size
			self.record_per_block = block_size / record_size
			# number of record the input data have
			self.num_of_record = len(record_list)
			# number of block the input data need
			if data_size % block_size != 0:
				self.num_of_block = len(record_list) / self.record_per_block + 1
				self.is_full_fill = False
			else:
				self.num_of_block = len(record_list) / self.record_per_block
				self.is_full_fill = True
			self.put_input_record_into_block(record_list)
			self.index_list.sort()
		else:
			raise ValueError
	def put_input_record_into_block(self, input_record=None):
		"""
		put the previous level BlockIndex's data into this level's block
		:type input_record: list
		"""
		if self.is_full_fill is False and self.num_of_record < self.record_per_block:
			special_num = self.num_of_record
			block_remain = self.num_of_record
		elif self.is_full_fill is False and self.num_of_record > self.record_per_block:
			special_num = self.num_of_record % self.record_per_block
			block_remain = self.record_per_block
		else:
			special_num = None
			block_remain = self.record_per_block
		block_num = SYSTEM.alloc_block()
		self.index_list.append(block_num)
		temp = Block(block_num, block_remain)
		counter = 0
		current = 0
		while counter < self.num_of_record:
			if block_remain != 0:
				temp.data_append(input_record[counter])
				block_remain -= 1
			else:
				self.block_list.append(temp)
				block_num = SYSTEM.alloc_block()
				self.index_list.append(block_num)
				current += 1
				if current == self.num_of_block - 1 and self.is_full_fill is False:
					temp = Block(block_num, special_num)
				else:
					temp = Block(block_num, self.record_per_block)
				block_remain = temp.num_of_record
				temp.data_append(input_record[counter])
				block_remain -= 1
			counter += 1
		# append the last Block or due to the mechanism of while it will be dropped
		self.block_list.append(temp)
	def get_info(self, content_fold=True):
		"""
		Return specified size of data according to specified index
		:type content_fold: bool
		"""
		lines = list()
		if self.level_num == 0:
			lines.append('Direct Block Index Table:\n')
		else:
			lines.append('Level ' + str(self.level_num) + ' Block Index Table:\n')
			lines.append('\thave ' + str(self.num_of_record) + ' records\n')
		lines.append('\thave ' + str(self.num_of_block) + ' blocks\n')
		lines.append('\ttake ' + str(self.num_of_block * self.block_size) + ' Byte space\n')
		if self.level_num == 0:
			if content_fold is True:
				pass
			else:
				hex_list = list()
				k = 0
				while k < len(self.index_list):
					hex_list.append(hex(self.index_list[k]))
					k += 1
				lines.append(str(hex_list) + '\n')
		else:
			k = 0
			while k < len(self.block_list):
				lines.append('Block ' + str(k).rjust(4) + ' : address - ' + hex(self.block_list[k].num)+' :\n')
				l = 0
				hex_list = list()
				while l < self.block_list[k].num_of_record:
					if content_fold is True:
						hex_list.append(hex(l))
					else:
						hex_list.append(hex(self.block_list[k].data[l]))
					l += 1
				k += 1
				lines.append(str(hex_list) + '\n')
		lines.append('\n')
		return lines

class IndexNode(object):
	"""
	I-node Structure
	"""
	def __init__(self, file_name=None, owner=None, file_size=None, num_of_level=None, block_size=None, record_size=None):
		"""
		:type file_name: str
		:type owner: str
		:type file_size: int
		:type num_of_level: int
		:type block_size: int
		:type record_size: int
		"""
		if block_size % record_size != 0:
			raise ValueError
		self.file_name = file_name
		self.owner = owner
		self.time_stamp = strftime('%Y/%m/%d %X')
		self.file_size = file_size
		self.num_of_level = num_of_level
		self.block_size = block_size
		self.record_size = record_size
		self.record_per_block = block_size / record_size
		self.block_index = list()
		self.generate_index()
	def generate_index(self):
		"""
		generate all direct and indirect index
		"""
		for i in range(0, self.num_of_level+1):
			if i == 0:
				temp = BlockIndex(i, self.file_size, self.block_size, self.record_size)
			else:
				data_size = self.block_index[i-1].num_of_block * self.record_size
				temp = BlockIndex(i, data_size, self.block_size, self.record_size, self.block_index[i-1].index_list)
			self.block_index.append(temp)
		return
	def output(self, content_fold=False):
		"""
		output itself
		:type want_index_list: bool
		"""
		line = list()
		line.append('File Name: ' + str(self.file_name) + '\n')
		line.append('Owner: ' + str(self.owner) + '\n')
		line.append('Time: ' + str(self.time_stamp) + '\n')
		line.append('File Size: ' + str(self.file_size) + ' Byte\n')
		line.append('Index Level: ' + str(self.num_of_level) + '\n\n')
		for i in range(0, self.num_of_level+1):
			line.extend(self.block_index[i].get_info(content_fold))
		return line

if __name__ == "__main__":
	if len(sys.argv) > 6:
		FILE_NAME = str(sys.argv[1])
		OWNER = str(sys.argv[2])
		FILE_SIZE = int(sys.argv[3])
		LEVEL = int(sys.argv[4])
		BLOCK_SIZE = int(sys.argv[4])
		RECORD_SIZE = int(sys.argv[4])
	elif len(sys.argv) == 1:
		FILE_NAME = 'I am awesome'
		OWNER = 'Cooper Yang'
		FILE_SIZE = 1234567
		LEVEL = 3
		BLOCK_SIZE = 2**8
		RECORD_SIZE = 2**2
	else:
		print __doc__
		raise NameError
	MY_FILE = IndexNode(FILE_NAME, OWNER, FILE_SIZE, LEVEL, BLOCK_SIZE, RECORD_SIZE)
	OUTPUT = open('lab-4.result','w')
	if len(sys.argv) > 7 and sys.argv[7] == '1':
		OUTPUT.writelines(MY_FILE.output(content_fold=False))
	else:
		OUTPUT.writelines(MY_FILE.output(content_fold=True))
	print 'completed !'

