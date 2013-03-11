#!/usr/bin/pythonwh
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import logging.handlers
import datetime
import shutil

log=logging.getLogger('main') 
log.setLevel(logging.DEBUG) 
formatter=logging.Formatter('%(asctime)s.%(msecs)d %(levelname)s in \'%(module)s\' at \
	line %(lineno)d: %(message)s','%Y-%m-%d %H:%M:%S') 
# handler = TimedCompressedRotatingFileHandler('/var/log/videowf/folder_monitor.log', when='midnight', interval=1)
handler=logging.FileHandler('testlog.log', 'a') 
handler.setFormatter(formatter)
# handler.setLevel(logging.DEBUG)
log.addHandler(handler) 

# logging.basicConfig(filename="testlog.log", 
#                     format=formatter, level=logging.DEBUG)

log.info('\n'*3 + ' '*5 + '*'*50)
# log.info('-'*50)
log.info(datetime.datetime.now())
# log.info('-'*50)
log.info("---Start log---")


args = sys.argv # get arguments 
path_list = [] # a variable for list extracted form txt file
dest_folder = '/home/russel/DEV/py/catdv_file_copier/output/' # destination folder for copied files



# Check destination folder existing and fix name (if without end "/"")
def check_destfolder(dest_folder):
	if os.path.isdir(dest_folder):
		if dest_folder.split('/')[-1]!='':
			dest_folder += '/'
		log.info("Destination folder exists and OK: %s" % dest_folder)
		

# Get path-list from txt file to array
def get_path_list(f):
	paths = f.readlines()
	for line in paths:
		if len(line)!=-1:
			if line[-1].find('\n')!=-1:
				path_list.append(line[:-1])
			else:
				path_list.append(line)
	log.info("Path list from txt: %s" % path_list)


# Try to open txt file. Its path was sent as argument
def open_txt():
	try:
		f = open(args[1], 'r')
	except Exception as e:
		log.error("The error occured while opening txt file: %s" % e[1])
	else:
		get_path_list(f)
	finally:
		f.close()


# Try copy file
def copy_file(filename, dest_folder):
	new_filename = make_new_name(filename, dest_folder)
	log.info("The new filename created: %s " % new_filename)
	try:
		shutil.copy2(filename, new_filename)
	except Exception:
		log.error("The error occured while copying file: %s" % e[1])
	else:
		log.info("And copied successfully!")


# Make new filename with proper destination
def make_new_name(filename, dest_folder):
	name = filename.split('/')[-1]
	new_name = name[:name.find('.original')] + name[name.find('.original')+len('.original'):]
	new_filename = dest_folder + new_name
	return new_filename


def main():
	global dest_folder
	check_destfolder(dest_folder)
	if len(args) == 2:
		log.info("There are one argument received.")
		if args[1].find('.txt') != -1:
			log.info("And it is txt object.")
			open_txt()
			for path in path_list:
				copy_file(path, dest_folder)
		else:
			log.error("There not txt object as argument received.")
	else:
		log.error("The number of argument seems doesn't proper: %d items" % (len(args)-1))


if __name__ == '__main__':
	main()


log.info("---End log at %s---\n" %datetime.datetime.now())
log.info('\n' + ' '*5 + '*'*50)