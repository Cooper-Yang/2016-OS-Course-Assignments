# -*- coding: utf-8 -*-
"""
OS Course Exp - 3: visual memory

Usage:
	python lab-3.py [record size] [page size] [number of level] [input address(hex) like 0x123]

	if you have not type anything, default value is 2**4, 2**12, 4, '0x1111111111111111'

InputError will raise if:
	arguments less than four
	record size, page size, number of level not pure digit
	input address not well formated
	input address < page size
	number of level < 1

:type sys.argv[1]: int
:type sys.argv[2]: int
:type sys.argv[3]: int
:type sys.argv[4]: str

****只在输出的时候生成随机地址****

# 页式存储逻辑地址到物理地址映射

* 条件：64位地址空间
* 输入：
  * 页记录大小（如 4Byte）
  * 页大小（如 4KB）
  * 页表级数（如，2表示2级页表，n表示n级页表）
  * 逻辑地址（十六进制）
* 输出：物理地址（物理块号，块内偏移）

说明：页表随机产生，为便于验证可令逻辑页号 `n` 的物理页号为 `n`。
"""
import sys
from random import randint

ADDR_SPACE = 2 ** 64

DOC = __doc__
class InputError(Exception):
	"""
	when input illegal
	"""
	def __str__(self):
		print DOC
		return

class System(object):
	"""
	Define system resource
	"""
	def __init__(self, ):
		self.used = set()
	def alloc_address(self):
		"""
		allocate an available block from the system resource randomly, will return the block number
		"""
		address_num = randint(0, ADDR_SPACE)
		while address_num in self.used is True:
			address_num = randint(0, ADDR_SPACE)
		self.used.add(address_num)
		return address_num

SYSTEM = System()

class PageTable(object):
	"""
	Page Table
	"""
	def __init__(self, record_num=None, record_size=None, page_size=None, pointer=None, is_ordered=False):
		"""
		:type record_num: int
		:type record_size: int
		:type page_size: int
		:type pointer: PageTable
		:type is_ordered: bool
		"""
		if page_size % record_size != 0:
			raise InputError
		self.num_of_record = record_num
		self.record_per_page = page_size / record_size
		self.num_of_page = self.num_of_record / self.record_per_page
		if self.num_of_record % self.record_per_page == 0:
			pass
		else:
			self.num_of_page += 1
		self.pointer = pointer
		self.is_ordered = is_ordered
	def __len__(self):
		return self.num_of_page
	def get_data(self, record_num=None):
		"""
		get the data of the specified record number
		:type record_num: int
		"""
		if self.is_ordered is True:
			data = int(record_num)
		else:
			data = int(SYSTEM.alloc_address())
		return data

if __name__ == "__main__":
	LINES = list()
	if len(sys.argv) == 1:
		sys.argv = [0, 2**2, 2**12, 4, '0x1111111111111111']
		LINE = 'using default value ...\n\n'
		print LINE
		LINES.append(LINE)
	if len(sys.argv) > 4:
		try:
			# record size
			sys.argv[1] = int(sys.argv[1])
			# page size
			sys.argv[2] = int(sys.argv[2])
			# number of level
			sys.argv[3] = int(sys.argv[3])
			if sys.argv[3] < 1:
				raise InputError
			sys.argv[4] = int(sys.argv[4], 16)
			if sys.argv[4] < sys.argv[2]:
				raise InputError
		except ValueError:
			raise InputError
		RECORD_NUM_OF_LAST_PAGE_TABLE = ADDR_SPACE / sys.argv[2]
		TABLE = []
		POINTER = None
		# init page table
		for i in range(0, sys.argv[3]):
			if i == 0:
				TEMP = PageTable(RECORD_NUM_OF_LAST_PAGE_TABLE, sys.argv[1], sys.argv[2], POINTER, is_ordered=True)
			else:
				TEMP = PageTable(RECORD_NUM_OF_LAST_PAGE_TABLE, sys.argv[1], sys.argv[2], POINTER)
			TABLE.insert(0, TEMP)
			RECORD_NUM_OF_LAST_PAGE_TABLE = len(TEMP)
			POINTER = TEMP
		# calculating the physical address
		TRACE = list()
		OFFSET = int(sys.argv[4] % sys.argv[2])
		PHY_BLOCK_NUM = int()
		TEMP = sys.argv[4] / sys.argv[2]
		TRACE.insert(0, TEMP)
		for i in range(0, sys.argv[3] - 1):
			try:
				i = (sys.argv[3] - 2) % i
			except ZeroDivisionError:
				if sys.argv[3] - 2 < 0:
					i = 0
				else:
					i = sys.argv[3] - 2
			TEMP = TEMP / TABLE[i].record_per_page
			TRACE.insert(0, TEMP)
		# print the result
		for i in range(0, sys.argv[3]):
			RESULT = TABLE[i].get_data(TRACE[i])
			line = 'Trace - PageTable' + str(i).rjust(3) + ':'
			line = line + ' page - ' + hex(TRACE[i]/TABLE[i].record_per_page).rjust(10)
			line = line + ' offset - ' + hex(TRACE[i]%TABLE[i].record_per_page).rjust(10)
			line = line + ' data - ' + hex(RESULT).rjust(10) + '\n'
			print line
			LINES.append(line)
		LINE = '\nPhysical Block (Hex): ' + hex(RESULT).rjust(12) + ' Offset: ' + hex(OFFSET) + '\n'
		print LINE
		LINES.append(LINE)
		LINE = 'Physical Block (Dec): ' + str(RESULT).rjust(12) + ' Offset: ' + str(OFFSET) + '\n'
		print LINE
		LINES.append(LINE)
		OUTPUT_FILE = open('lab-3.result', 'w')
		OUTPUT_FILE.writelines(LINES)
	else:
		raise InputError
