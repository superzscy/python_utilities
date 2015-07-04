import os
import sys
from collections import OrderedDict
from os.path import join, getsize

def readable_size(size):
	for unit in ['K', 'M']:
		if abs(size) < 1024.0:
			return "%.1f%sB" % (size, unit)
		size /= 1024.0
	return "%.1f%s" % (size, 'GB')

def main(argv_list):
	path = argv_list[0]
	count = 0
	if(len(argv_list) > 1):
		count = int(argv_list[1])
	print("Start Finding in " + path)
	file_list = []
	if path is None:
		raise Exception("path is invalid");
	size_dict = {}
	for root, dirs, files in os.walk(path):
		for name in files:
			file_path = join(root, name)
			size = getsize(file_path) / 1024
			#if(size > 1):
			size_dict[file_path] = size

	#sort
	od = OrderedDict(sorted(size_dict.items(), key=lambda item:item[1], reverse = True))
	print_count = 0
	for key, value in od.items():
		if(count != 0):
			if(print_count > count):
				break;
			else:
				print_count += 1
		print("%s %s" %(readable_size(value), key))
		#print("%s %s" %( value, key))

def test():
	dict = [('a', 1), ('c', 5), ('b', 3)]
	dict = sorted(dict, key=lambda item:item[1])
	print(dict)

if __name__ == "__main__":
	main(sys.argv[1:])
	#test()