# -*- coding: utf-8 -*-
# COPYRIGHT Daniel Falkov, MIT License, all rights reserved. (check https://github.com/Dan149/LinuxTerminalEmulator)
import os
from time import sleep
import platform
from getpass import getpass, getuser
from random import randint
from os import system as term
from datetime import datetime
__version__ = "v0.1a"
root_dir = []
sub_dirs = []

# back-end
def clear():
	if os.name == "nt":
		term("cls")
	else:
		term("clear")

class RootDir:
	def __init__(self, name, need_root=True):
		self.need_root = need_root
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
	def deleteall(self):
		self.content.clear()

class SubDir():
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
		self.storedtext = ""
		self.name = name
		self.parentdir = pdir
		if pdir == "root": # To create a text file in the root directory.
			self.path = "/{}".format(self.name) # not used anymore
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

# root dirs :
home = RootDir("home", False) #arg1 = name, #arg2 = need_root
sys = RootDir("sys")
lib = RootDir("lib")
boot = RootDir("boot")
var = RootDir("var")
tmp = RootDir("tmp")
media = RootDir("media")
userhome = SubDir(str(getuser()), home)
# user home dirs (subdirs) :
Desktop = SubDir("Desktop", userhome) #arg1 = name, arg2 = parent directory
Documents = SubDir("Documents", userhome)
Videos = SubDir("Videos", userhome)
Pictures = SubDir("Pictures", userhome)
Music = SubDir("Music", userhome)
Downloads = SubDir("Downloads", userhome)

# text files:
password = Textfile("password.txt", Documents)
logfile = Textfile("log.txt", tmp)
logfile.openwithoutroot(False)
password.writetext("helloworld")

def log_event(event, subject): # [00:00:00|2000-00-00] subject: event
	now = datetime.now()
	logdt = "[{}|{}]".format(now.strftime("%H:%M:%S"), str(datetime.today()).split()[0])
	logfile.appendtext(f"\n{logdt} {subject}: {event}")
# password.openwithoutroot(False) # need to be root in order to read or modify file
# root_text_file = Textfile("root-text-file", "root") # Example of a root text file construction
# root_text_file.writetext("I'm in the root directory !")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Terminal:
	log_event("LTE start.", "[INFO]")
	executed = False # used by the "cd" command
	isroot = False
	launched = True
	current_path = None # the path to the current directory, ["\n"] if root
	current_dir = None # the directory you are in, None if root
	passwd = "helloworld"
	def __init__(self):
		self.current_path = ["\b"] # root path init
		clear()
		print(f"\nLinuxTerminalEmulator {__version__} | Created by Dan149.\n")
		self.main()

	def reboot(self):
		try:
			sleep(1.5)
			clear()
			print("""
	+-----------------------------------------------------------------+
	|                                                                 |
	|                   LTE OS alpha | Rebooting...                   |
	|                                                                 |
	|                                                                 |
	|       COPYRIGHT Dan149, all rights reserved, MIT license.       |
	|                                                                 |
	+-----------------------------------------------------------------+
""")
			sleep(3)
			print("\nAdmin Password: OK")
			sleep(1)
			print("Root directories: OK")
			sleep(2)
			if os.name == "nt":
				print(f"OS: Windows {platform.release()} (nt)")
			elif os.name == "posix":
				print("OS: Linux/Mac (posix)")
			else:
				print(f"OS: Unknown ({os.name})")
			sleep(randint(1,3))
			print("Modules: OK")
			sleep(randint(1,3))
			print("User files: OK")
			sleep(randint(1,3))
			print("All clear, starting up.")
			sleep(randint(1,3))
			term("python3 script.py")
			quit()
		except KeyboardInterrupt:
			print("KeyboardInterrupt")
			quit()

	def enable_root(self):
		for x in range(3):
			enter_passwd = getpass("\nEnter admin password: ")
			if enter_passwd == self.passwd:
				self.isroot = True
				print("You are now root.")
				log_event("Root user enabled.", "[INFO]")
				break
			else:
				print("Wrong password, try again.")
				log_event("Root user upgrade failed.", "[ERROR]")
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
									if select_s[1] == root_dir[x].name:
										if root_dir[x].type == "dir":
											self.current_path.append(root_dir[x].name)
											self.current_dir = root_dir[x]
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
								if select_s[1] == root_dir[x].name:
									if root_dir[x].type == "txt":
										if root_dir[x].need_root == False:
											print(root_dir[x].storedtext)
										elif self.isroot:
											print(root_dir[x].storedtext)
										else:
											self.enable_root()
											if self.isroot:
												print(root_dir[x].storedtext)
											else:
												pass
									else:
										print("Error: cat only works with text files.")
									break
								else:
									pass
						else:
							for x in range(len(self.current_dir.content)):
								if select_s[1] == self.current_dir.content[x].name:
									if self.current_dir.content[x].type == "txt":
										if self.current_dir.content[x].need_root == False:
											print(self.current_dir.content[x].storedtext)
										elif self.isroot:
											print(self.current_dir.content[x].storedtext)
										else:
											self.enable_root()
											if self.isroot:
												print(self.current_dir.content[x].storedtext)
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
							print(root_dir[x].name, end=" ")
						print("")
					else:
						if len(self.current_dir.content) > 0:
							print("")
							for x in range(len(self.current_dir.content)):
								print(self.current_dir.content[x].name, end=" ")
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
							log_event("Root user password changed.", "[INFO]")
						else:
							print("Error: confirmation failed.")
							log_event("Root user password change failed", "[ERROR]")
					else:
						pass
				elif select_s[0] == "rm":
					if len(select_s) == 2:
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
								if select_s[1] == "*":
									root_dir.clear()
									print("Removed.")
								else:
									pass
							else:
								pass
						else:
							if not self.current_dir.need_root:
								for x in range(len(self.current_dir.content)):
									if select_s[1] == self.current_dir.content[x].name:
										del self.current_dir.content[x]
										print("Removed.")
										break
									else:
										pass
								if select_s[1] == "*":
									for x in range(len(self.current_dir.content)):
										self.current_dir.content.clear()
									print("Removed.")
								else:
									pass
							else:
								if not self.isroot:
									self.enable_root()
								else:
									pass
								if self.isroot:
									for x in range(len(self.current_dir.content)):
										if select_s[1] == self.current_dir.content[x].name:
											del self.current_dir.content[x]
											print("Removed.")
											break
										else:
											pass
									if select_s[1] == "*":
										for x in range(len(self.current_dir.content)):
											self.current_dir.content.clear()
										print("Removed.")
									else:
										pass
					else:
						print("Error: wrong argument.")

				elif select_s[0] == "mkdir":
					make = True
					if len(self.current_path) == 1:
						if not self.isroot:
							self.enable_root()
						else:
							pass
						if self.isroot:
							for x in range(len(root_dir)):
								if select_s[1] == root_dir[x].name:
									print("Error: directory already exists.")
									make = False
									break
								else:
									pass
							if make:
								select_s[1] = RootDir(select_s[1])
								print("Directory created.")
							else:
								pass
						else:
							pass
					else:
						if not self.current_dir.need_root:
							for x in range(len(self.current_dir.content)):
								if select_s[1] == self.current_dir.content[x].name:
									print("Error: directory already exists.")
									make = False
									break
								else:
									pass
							if make:
								select_s[1] = SubDir(select_s[1], self.current_dir)
								print("Directory created.")
							else:
								pass
						else:
							if not self.isroot:
								self.enable_root()
							else:
								pass
							if self.isroot:
								for x in range(len(self.current_dir.content)):
									if select_s[1] == self.current_dir.content[x].name:
										print("Error: directory already exists.")
										make = False
										break
									else:
										pass
								if make:
									select_s[1] = SubDir(select_s[1], self.current_dir)
									print("Directory created.")
								else:
									pass
				# elif select_s[0] == "nano":
				# 	if len(self.current_path) == 1:
				# 		if not self.isroot:
				# 			self.enable_root()
				# 		else:
				# 			pass
				# 		if self.isroot:
				# 			text = []
				# 			create = True
				# 			writting = True
				# 			line = 1
				# 			print(f"Writting in {select_s[1]}, Ctrl+C to save and exit.")
				# 			try:
				# 				while writting:
				# 					towrite = input(f"line {line} | ")
				# 					text.append(towrite)
				# 					line = line + 1
				# 			except KeyboardInterrupt:
				# 				break
				# 				for x in range(len(root_dir)):
				# 					if select_s[1] == root_dir[x].name:
				# 						if root_dir[x].type == "txt":
				# 							for x in range(len(text)):
				# 								root_dir[x].appendtext("\n" + towrite)
				# 							create = False
				# 							break
				# 						else:
				# 							print("Error: nano only work with text files.")
				# 							create = False
				# 							break
				# 					else:
				# 						pass
				# 				if create:
				# 					select_s[1] = Textfile(select_s[1], "root")
				# 					print(f"Writting in {select_s[1]}, Ctrl+C to save and exit.")
				# 					try:
				# 						while writting:
				# 							towrite = input(f"line {line} | ")
				# 							text.append(towrite)
				# 							line = line + 1
				# 					except KeyboardInterrupt:
				# 						break
				# 						for x in range(len(text)):
				# 							select_s[1].writetext(towrite + "\n")
				# 		else:
				# 			pass

				elif select_s[0] == "sleep":
						if len(select_s) == 2:
							sleep_time = int(select_s[1])
							sleep(sleep_time)
						else:
							print("Error: sleep take one argument: sleep [seconds]")
				elif select == "sudo su" or select == "sudo bash" or select == "sudo zsh":
					self.enable_root()
				elif select == "exit" or select == "logout":
					if self.isroot:
						self.isroot = False
						log_event("Root user disabled.", "[INFO]")
					else:
						self.launched = False
						quit()
				elif select == "reboot":
					confirm_reboot = input("\nRebooting will reset data, continue ? [y/N]\n>> ")
					if confirm_reboot == "yes" or confirm_reboot == "y" or confirm_reboot == "YES" or confirm_reboot == "Yes" or confirm_reboot == "Y":
						self.launched = False
						self.reboot()
				elif select == "init1":
					sleep(3)
					clear()
					sleep(2)
					print("\n     Loading assets.")
					sleep(3.5)
					clear()
					print("\n     Loading assets..")
					sleep(2.5)
					clear()
					print("\n     Loading assets...")
					sleep(3)
					clear()
					print("\n     Loading assets: Done!")
					sleep(2)
				elif select == "clear":
					clear()
				elif select == "credits":
					print("\n © Daniel Falkov (Dan149 on Github) all rights reserved, MIT License.")
				elif select == "python":
					term("python")
					log_event("Launching default Python.", "[INFO]")
				elif select == "python2":
					term("python2")
					log_event("Launching Python2.", "[INFO]")
				elif select == "python3":
					term("python3")
					log_event("Launching Python3.", "[INFO]")
				elif select == "help" or select == "?":
					fhlp = open("help", "r")
					hlp = fhlp.read()
					fhlp.close()
					print(hlp)
				elif select == "version":
					print(f"LinuxTerminalEmulator {__version__}")
				else:
					print("Error: command not found.")
					log_event(f"Command '{select}' not found.", "[ERROR]")
		except KeyboardInterrupt:
			print("\n\nKeyboardInterrupt")
			self.launched = False
			quit()

#   Execution   #
Terminal()
