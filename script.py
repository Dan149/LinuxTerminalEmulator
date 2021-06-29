# -*- coding: utf-8 -*-
# COPYRIGHT Daniel Falkov, MIT License, all rights reserved. (check https://github.com/Dan149/LinuxTerminalEmulator)
from os import system as term
from getpass import getpass
import os
from time import sleep

def clear():
	if os.name == "nt":
		term("cls")
	else:
		term("clear")

class Terminal:
	launched = True
	commandexecuted = False
	root = False
	password = "neverstoplearning"
	dirs = ["sys", "lib", "var", "usr", "home", "bin"] # Directories in root
	files = ["password.txt"] # Files in root
	path = "/"
	def __init__(self):
		self.main()
	def ltehelp(self):
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
	exit: exit LTE
""")
	def main(self):
		password = self.password
		try:
			while self.launched:
				dirs = self.dirs
				files = self.files
				select = input(f"\n{self.path}> ")
				select_split = select.split(" ")
				# print(select_split)
				if select_split[0] == "cd":
					self.commandexecuted = True
					try:
						for x in range(len(dirs)):
							u = x-1
							adir = str(dirs[u])
							seldir = str(select_split[1])
							if seldir == "/" or seldir == "~" or seldir == "\\":
								self.path = "/"
							elif adir == seldir:
								if self.path == "/":
									self.path = "/" + seldir + "/"
								else:
									print("Directory not found.")
								# print("True")
							elif adir + "/" == seldir or adir + "\\" == seldir:
								if self.path == "/":
									self.path = "/" + seldir
								else:
									print("Directory not found.")
								# print("True")
							elif "/" + adir == seldir or "\\" + adir == seldir:
									self.path = seldir + "/"
							else:
								pass #print("no dir")
					except IndexError:
						print("ERROR: cd must take an argument. (ie: cd home)")
				elif select_split[0] ==  "cat":
					self.commandexecuted = True
					try:
						file = select_split[1]
						if file == "password.txt" and self.path == "/":
							print(password)
					except IndexError:
						print("ERROR: cat must take an argument. (ie: cat password.txt)")
				elif select_split[0] == "rm":
					try:
						notfound = True
						self.commandexecuted = True
						if self.path == "/":
							if self.root:
								for x in range(len(dirs)):
									u = x-1
									if str(dirs[u]) == str(select_split[1]):
										dirs.pop(dirs.index(str(select_split[1])))
										notfound = False
									else:
										pass
								for x in range(len(files)):
									u = x-1
									if str(files[u]) == str(select_split[1]):
										files.pop(files.index(str(select_split[1])))
										notfound = False
									else:
										pass
								if notfound:
									print("File or directory not found.")
								else:
									pass
							else:
								print("You must be root to remove files.")
						else:
							print("File or directory not found.")
					except IndexError:
						print("ERROR: rm must take an argument. (ie: rm lib)")
				elif str(select_split[0]) == "sleep":
					self.commandexecuted = True
					try:
						if len(select_split) > 2:
							print("ERROR: sleep must take only one argument.")
						else:
							sleep_time = int(select_split[1])
							sleep(sleep_time)
					except IndexError:
						print("ERROR: sleep must take an argument. (ie: sleep 10)")
				elif str(select_split[0]) == "mkdir":
					self.commandexecuted = True
					if self.path == "/":
						if self.root:
							try:
								for x in range(len(dirs)):
									u = x-1
									if str(select_split[1]) == str(dirs[u]):
										print("ERROR: this directory have already been created.")
								if len(select_split) > 2:
									print("ERROR: spaces are not allowed.")
								else:
									dirs.append(select_split[1])
							except IndexError:
								print("ERROR: mkdir must take an argument. (ie: mkdir hello)")
						else:
							print("You must be root to create files.")
					else:
						print("ERROR: you can't create files here by the moment. (COMING SOON)")

				elif select_split[0] == "sudo":
					try:
						if select_split[1] == "rm":
							self.commandexecuted = True
							if not self.root:
								enter_passwd = getpass("Enter admin password: ")
							else:
								pass
							if enter_passwd == password or self.root:
								self.root = True
								if len(select_split) > 2:
									print("ERROR: There aren't spaces in files or directories names")
								elif self.path == "/":
										for x in range(len(dirs)):
											u = x-1
											if str(dirs[u]) == str(select_split[2]):
												dirs.pop(dirs.index(str(select_split[2])))
											else:
												pass
										for x in range(len(files)):
											u = x-1
											if str(files[u]) == str(select_split[2]):
												files.pop(files.index(str(select_split[2])))
											else:
												pass
								else:
									print("File or directory not found.")
							else:
								print("Wrong password.")
						elif select_split[1] == "mkdir":
							self.commandexecuted = True
							if not self.root:
								enter_passwd = getpass("Enter admin password: ")
							else:
								pass
							if enter_passwd == password or self.root:
								self.root = True
								for x in range(len(dirs)):
									u = x-1
									if str(select_split[1]) == str(dirs[u]):
										print("ERROR: this directory have already been created.")
								if len(select_split) > 3:
									print("ERROR: spaces are not allowed.")
								else:
									dirs.append(select_split[2])
							else:
								print("Wrong password.")
						else:
							print("Command not found.")
					except IndexError:
						print("ERROR: sudo must take two arguments. (ie: sudo rm password.txt)")
				else:
					pass
				if self.commandexecuted != True:
					if select == "ls":
						if self.path == "/":
							print("")
							for x in range(len(dirs)):
								u = x-1
								print(dirs[u], end=" ")
							print("|", end=" ")
							for x in range(len(files)):
								u = x-1
								print(files[u], end=" ")
							print("")
						else:
							print("No directories.")
					elif select == "clear":
						clear()
					elif select == "credits":
						print("\n© Daniel Falkov (Dan149 on Github) MIT License, all rights reserved.")
					elif select == "python":
						term("python")
					elif select == "python2":
						term("python2")
					elif select == "python3":
						term("python3")
					elif select == "sudo su" or select == "sudo bash" or select == "sudo zsh":
						enter_passwd = getpass("Enter admin password: ")
						if enter_passwd == password:
							self.root = True
							print("You are now root.")
						else:
							print("Wrong password.")
					elif select == "passwd":
						enter_passwd = getpass("Enter admin password: ")
						if enter_passwd == password:
							change_passwd = getpass("Enter new admin password: ")
							confirm_new_passwd = getpass("Confirm new admin password: ")
							if change_passwd == confirm_new_passwd:
								self.password = change_passwd
								password = self.password
							else:
								print("Confirmation failed.")
						else:
							print("Wrong password.")
					elif select == "help":
						self.ltehelp()
					elif select == "exit":
						quit()
					else:
						print("Command not found.")
				else:
					self.commandexecuted = False
		except KeyboardInterrupt:
			quit()

#################################
clear()
print("\nLTE | Created by Dan149, check https://github.com/Dan149/LinuxTerminalEmulator/")
Terminal()
