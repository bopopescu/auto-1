#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
def Test1(rootDir): 
	list_dirs = os.walk(rootDir) 
	for root, dirs, files in list_dirs: 
		for d in dirs: 
			path = os.path.join(root, d) 
			notebook = os.path.basename(d)    
			os.system("~/@Work/Development/geeknote/gnsync.py --path \"%s\"  --notebook  \"%s\" "% (path,notebook) )
			# os.system("echo  \" %s \"    \" %s \" " (path,notebook) )
			# os.system("echo \"%s\" \" %s\""%(path,notebook))

		for f in files: 
			pass
#			print os.path.join(root, f) 



def main():
	Test1(".")


if __name__=="__main__":
	main()
	tmp='haha'
	os.system("echo %s" % (tmp) )

