# -*- coding: utf-8 -*-
# COPYRIGHT Daniel Falkov, MIT License, all rights reserved. (check https://github.com/Dan149/LinuxTerminalEmulator)
import os
from time import sleep
from getpass import getpass, getuser
from os import system as term

root_dir = []
sub_dirs = []

# back-end
def clear():
	if os.name == "nt":
		term("cls")
	else:
		term("clear")

class Dir:
	def __init__(self, name):
		self.need_root = True
		self.type = "dir"
		self.parentdir = None
		self.name = name
		self.path = "/{}".format(self.name) # not used anymore
		self.content = [] # container for all subdirs
		self.mkdirs = [] # container for user made subdirs
		root_dir.append(self)
	def debug_info_template(self, name, path, parentdir):
		print("Dirctory name: " + name)
		print("Directory Path: " + path)
		print("Parent directory: " + parentdir + "\n")
	def debug_info(self):
		self.debug_info_template(self.name, self.path, None)

class Subdir():
	def __init__(self, name, pdir): #pdir = parentdir
		self.need_root = False # default
		self.type = "dir"
		self.content = []
		self.name = name
		self.parentdir = pdir
		sub_dirs.append(self)
		self.init_path(self.parentdir)
	def init_path(self, parentdir):
		self.path = "/{}/{}".format(self.parentdir.name, self.name)
		self.parentdir.content.append(self)
	def debug_info(self):
		Dir.debug_info_template(self, self.name, self.path, self.parentdir.name)

class Textfile:
	def __init__(self, name, pdir):
		self.need_root = False
		self.type = "txt"
		self.storedtext = None
		self.name = name + ".txt"
		self.parentdir = pdir
		if pdir == "root": # To create a text file in the root directory.
			self.path = "/{}".format(self.name)
			root_dir.append(self)
		else:
			self.path = "/{}/{}".format(self.parentdir.name, self.name)
			self.parentdir.content.append(self)
	def openwithoutroot(self, bool_in):
		if bool_in == True:
			self.need_root = False
		if bool_in == False:
			self.need_root = True
	def writetext(self, text):
		self.storedtext = text
	def appendtext(self, text):
		self.storedtext = self.storedtext + " " + text

#root dirs :
home = Dir("home") #arg1 = name
sys = Dir("sys")
lib = Dir("lib")
boot = Dir("boot")
var = Dir("var")

#home dirs (subdirs) :
Desktop = Subdir("Desktop", home) #arg1 = name, arg2 = parent directory
Documents = Subdir("Documents", home)
Videos = Subdir("Videos", home)
Pictures = Subdir("Pictures", home)
Music = Subdir("Music", home)
Downloads = Subdir("Downloads", home)

#text files:
password = Textfile("password", Documents)
password.writetext("HelloWorld!")
# password.openwithoutroot(False) # need to be root in order to read or modify file
# root_text_file = Textfile("root-text-file", "root") # Example of a root text file construction
# root_text_file.writetext("I'm in the root directory !")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Terminal:
	executed = False # used by the "cd" command
	isroot = False
	launched = True
	current_path = None # the path to the current directory, ["\n"] if root
	current_dir = None # the directory you are in, None if root
	passwd = "HelloWorld!"
	def __init__(self):
		self.current_path = ["\b"] # root path init
		clear()
		print("\nLinuxTerminalEmulator alpha | Created by Dan149.\n")
		self.main()

	def enable_root(self):
		for x in range(3):
			enter_passwd = getpass("\nEnter admin password: ")
			if enter_passwd == self.passwd:
				self.isroot = True
				print("You are now root.")
				break
			else:
				print("Wrong password, try again.")
	def print_path(self):
		path = "/".join(self.current_path)
		return path

	def main(self): # front-end
		try:
			while self.launched:
				if not self.isroot:
					select = input("\n[" + getuser() + "@LTE]  " + self.print_path() + "> ")
				else:
					select = input("\n[root@LTE]  " + self.print_path() + "> ")
				select_s = select.split(" ")
				if select_s[0] == "cd":
					if len(select_s) == 2:
						if len(self.current_path) == 1:
								for x in range(len(root_dir)):
									u = x-1
									if select_s[1] == root_dir[u].name:
										if root_dir[u].type == "dir":
											self.current_path.append(root_dir[u].name)
											self.current_dir = root_dir[u]
										else:
											print("Error: cd doesn't work with text files.")
										break
									else:
										pass
						else:
							if select_s[1] == "/" or select_s[1] == "\\" or select_s[1] == "~":
								self.executed = True
								self.current_path = ["\b"]
								self.current_dir = None
							elif select_s[1] == "..":
								self.executed = True
								self.current_path.pop()
								try:
									self.current_dir = self.current_dir.parentdir
								except AttributeError:
									self.current_path = ["\b"]
									self.current_dir = None
							else:
								pass
							if not self.executed:
								for x in range(len(self.current_dir.content)):
									if select_s[1] == self.current_dir.content[x].name:
											if self.current_dir.content[x].type == "dir":
												self.current_path.append(self.current_dir.content[x].name)
												self.current_dir = self.current_dir.content[x]
												break
											else:
												print("Error: cd doesn't work with Text files.")
												break
									else:
										pass
							else:
								self.executed = False
					else:
						print("Error: cd take one argument: cd [dir_name]")

				elif select_s[0] == "cat":
					if len(select_s) == 2:
						if len(self.current_path) == 1:
							for x in range(len(root_dir)):
								u = x-1
								if select_s[1] == root_dir[u].name:
									if root_dir[u].type == "txt":
										if root_dir[u].need_root == False:
											print(root_dir[u].storedtext)
										elif self.isroot:
											print(root_dir[u].storedtext)
										else:
											self.enable_root()
											if self.isroot:
												print(root_dir[u].storedtext)
											else:
												pass
									else:
										print("Error: cat only works with text files.")
									break
								else:
									pass
						else:
							for x in range(len(self.current_dir.content)):
								u = x-1
								if select_s[1] == self.current_dir.content[u].name:
									if self.current_dir.content[u].type == "txt":
										if self.current_dir.content[u].need_root == False:
											print(self.current_dir.content[u].storedtext)
										elif self.isroot:
											print(self.current_dir.content[u].storedtext)
										else:
											self.enable_root()
											if self.isroot:
												print(self.current_dir.content[u].storedtext)
											else:
												pass
									else:
										print("Error: cat only works with text files.")
					else:
						print("Error: cat take one argument: cat [text_file]")
				elif select == "ls":
					if len(self.current_path) == 1: # check if in root dir
						print("")
						for x in range(len(root_dir)):
							u = x-1
							print(root_dir[u].name, end=" ")
						print("")
					else:
						if len(self.current_dir.content) > 0:
							print("")
							for x in range(len(self.current_dir.content)):
								u = x-1
								print(self.current_dir.content[u].name, end=" ")
							print("")
						else:
							print(f"\nFolder {self.current_dir.name} is empty.")
				elif select == "passwd":
					if not self.isroot:
						self.enable_root()
					if self.isroot:
						change_passwd = getpass("Enter new admin password: ")
						confirm_passwd = getpass("Confirm new admin password: ")
						if change_passwd == confirm_passwd:
							self.passwd = confirm_passwd
							password.writetext(self.passwd)
						else:
							print("Error: confirmation failed.")
					else:
						pass
				elif select_s[0] == "rm":
					if len(self.current_path) == 1:
						if not self.isroot:
							self.enable_root()
						else:
							pass
						if self.isroot:
							for x in range(len(root_dir)):
								if select_s[1] == root_dir[x].name:
									del root_dir[x]
									print("Removed.")
									break
								else:
									pass
						else:
							pass
					else:
						for x in range(len(self.current_dir.content)):
							if select_s[1] == self.current_dir.content[x].name:
								del self.current_dir.content[x]
								print("Removed.")
								break
							else:
								pass
				elif select_s[0] == "mkdir":
					if len(self.current_path) == 1:
						if not self.isroot:
							self.enable_root()
						else:
							pass
						if self.isroot:
							select_s[1] = Dir(select_s[1])
							print("Directory created.")
						else:
							pass
					else:
						select_s[1] = Subdir(select_s[1], self.current_dir)

				elif select_s[0] == "sleep":
						if len(select_s) == 2:
							sleep_time = int(select_s[1])
							sleep(sleep_time)
						else:
							print("Error: sleep take one argument: sleep [seconds]")
				elif select == "sudo su" or select == "sudo bash" or select == "sudo zsh":
					self.enable_root()
				elif select == "exit":
					self.launched = False
					quit()
				elif select == "clear":
					clear()
				elif select == "credits":
					print("\n © Daniel Falkov (Dan149 on Github) all rights reserved, MIT License.")
				elif select == "python":
					term("python")
				elif select == "python2":
					term("python2")
				elif select == "python3":
					term("python3")
				elif select == "help" or select == "?":
					print("""
	sudo su / sudo bash / sudo zsh: become root (admin password required)
	cd: enter in a directory (use: cd [dir_name])
	cat: display the content of a textfile (use: cat [file_name])
	mkdir: create a new directory (use: mkdir [new_dir_name])
	rm: remove a file (use: rm [dir_or_file_name]), root required
	ls: list directories in the current directory
	clear: clear the terminal
	python: launch your default python env in the terminal
	python2: launch python2, if installed on the computer
	python3: launch python3
	passwd: change password (admin password required)
	sleep: sleep for an amount of time (use: sleep [seconds])
	credits: display LTE credits
	help: display this message
	exit: exit LTE""")
				else:
					print("Error: command not found.")
		except KeyboardInterrupt:
			self.launched = False
			quit()
Terminal()
