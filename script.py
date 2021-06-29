# -*- coding: utf-8 -*-
# COPYRIGHT Daniel Falkov, MIT License, all rights reserved. (check https://github.com/Dan149/LinuxTerminalEmulator)
from os import system as term
import os

def clear():
	if os.name == "nt":
		term("cls")
	else:
		term("clear")

class Terminal:
	launched = True
	cdexecuted = False
	dirs = ["sys", "lib", "var", "usr", "home"]
	path = "/"
	def __init__(self):
		self.main()
	def help(self):
		print("""
	cd: enter in a directory (use: cd [dir_name])
	ls: list directories in the current directory (use: ls)
	clear: clear the terminal (use: clear)
	exit: exit LTE (use: exit)
	python: launch your default python env in the terminal (use: python)
	python2: launch python2, if installed on the computer (use: python2)
	python3: launch python3 (use: python3)
	credits: display LTE credits
	help: display this message
""")
	def main(self):
		try:
			while self.launched:
				dirs = self.dirs
				select = input(f"\n{self.path}> ")
				select_split = select.split(" ")
				# print(select_split)
				if select_split[0] == "cd":
					self.cdexecuted = True
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
				else:
					pass
				if not self.cdexecuted:
					if select == "ls":
						for x in range(len(dirs)):
							u = x-1
							print(dirs[u], end=" ")
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
					elif select == "exit":
						quit()
					else:
						print("Command not found.")
				else:
					self.cdexecuted = False
		except KeyboardInterrupt:
			quit()

#################################
print("LTE | Created by Dan149, check https://github.com/Dan149/LinuxTerminalEmulator/")
Terminal()
