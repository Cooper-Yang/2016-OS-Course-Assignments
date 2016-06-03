# -*- coding: utf-8 -*-
'''
# 页式存储逻辑地址到物理地址映射

* 条件：64位地址空间
* 输入：
  * 页记录大小（如 4Byte）
  * 页大小（如 4KB）
  * 页表级数（如，2表示2级页表，n表示n级页表）
  * 逻辑地址（十六进制）
* 输出：物理地址（物理块号，块内偏移）

说明：页表随机产生，为便于验证可令逻辑页号 `n` 的物理页号为 `n`。
'''
import sys
from random import randint

class PageTable(object):
	'''
	Page Table
	'''
	def __init__(self, record_num=None, record_size=None, page_size=None, pointer=None):
		if page_size % record_size != 0:
			raise ValueError
		self.num_of_record = record_num
		self.page = list()
		self.num_of_page = int()
		self.record_per_page = page_size / record_size
		self.pointer = pointer
		self.generate(record_size, page_size)
	def __len__(self):
		return self.num_of_page
	def generate(self, record_size=None, page_size=None):
		'''
		generating Page
		'''
		temp_num = self.num_of_record / self.record_per_page
		temp_rest = self.num_of_record % self.record_per_page
		# if the last page can not be full fill
		if temp_rest != 0:
			temp_num += 1
		for num in range(0, temp_num):
			# if the last page can not be full fill
			if num == temp_num - 1 and temp_rest != 0:
				temp = Page(record_size, page_size, temp_rest)
			temp = Page(record_size, page_size)
			self.page.append(temp)
			self.num_of_page += 1
		return
	def random_data_gen(self, data_set=None):
		'''
		fill random data to all page record
		'''
		temp = list(data_set)
		current = 0
		count = self.page[current].num_of_record
		for _ in range(0, self.num_of_record):
			rand_num = randint(0, len(temp))
			if count != 0:
				self.page[current].data.add(temp[rand_num])
				data_set.pop(rand_num)
				count -= 1
			else:
				current += 1
				count = self.page[current].num_of_record
	def order_data_gen(self):
		'''
		fill ordered data to all page record
		which is the physical block num
		'''
		current = 0
		count = self.page[current].num_of_record
		for num in range(0, self.num_of_record):
			if count != 0:
				self.page[current].data.add(num)
				count -= 1
			else:
				current += 1
				count = self.page[current].num_of_record
		return

class Page(object):
	'''
	Page
	'''
	def __init__(self, record_size=None, page_size=None, record_num=None):
		if record_size > page_size or page_size % record_size != 0:
			raise ValueError
		self.record_size = record_size
		self.size = page_size
		self.data = set()
		# if the last page can not be full fill
		if record_num != None:
			self.num_of_record = record_num
		else:
			self.num_of_record = page_size / record_size

if __name__ == "__main__":
	if len(sys.argv) > 4:
		# record size
		sys.argv[1] = int(sys.argv[1])
		# page size
		sys.argv[2] = int(sys.argv[2])
		# number of level
		sys.argv[3] = int(sys.argv[3])
		sys.argv[4] = int(sys.argv[4], 16)
		ADDR_SPACE = 2 ** 64
		NUM_OF_PHYSICAL_BLOCK = ADDR_SPACE / sys.argv[2]
		RECORD_NUM_OF_LAST_PAGE_TABLE = NUM_OF_PHYSICAL_BLOCK / sys.argv[2] * sys.argv[1]
		# take the TABLE[0] spot when init, so there won't have 'page table level 0'
		TABLE = [[]]
		POINTER = None
		DATA_SET = set(list(range(NUM_OF_PHYSICAL_BLOCK-RECORD_NUM_OF_LAST_PAGE_TABLE, NUM_OF_PHYSICAL_BLOCK)))
		# init page table
		for i in range(0, sys.argv[3]):
			TEMP = PageTable(RECORD_NUM_OF_LAST_PAGE_TABLE, sys.argv[1], sys.argv[2], POINTER)
			RECORD_NUM_OF_LAST_PAGE_TABLE = len(TEMP)
			if i == 0:
				TEMP.order_data_gen()
			else:
				TEMP.random_data_gen(DATA_SET)
			TABLE.append(TEMP)
			POINTER = TEMP
	else:
		raise ValueError
