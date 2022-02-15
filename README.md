# LinuxTerminalEmulator
### LTE is a python script which mimics the operation of a linux terminal, useful for beginners wishing to learn basic linux commands.

<a href="https://github.com/Dan149/LinuxTerminalEmulator/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg?label=License&style=flat" /></a>
[![Python 3.7](https://img.shields.io/badge/Python-3.9-blue.svg)](http://www.python.org/download/)
[![OS](https://img.shields.io/badge/Tested%20on:-Windows%20|%20Linux-purple.svg)](https://www.linux.com/what-is-linux/)
<a href="https://twitter.com/daniel_fkv"><img src="https://img.shields.io/twitter/follow/daniel_fkv?label=Follow&style=social"/></a>

For everyone who wish to learn to use the linux terminal without impacting the operation of their computer or having to install a virtual machine to test their skills.

available commands:
  - cd
  - ls
  - cat
  - mkdir
  - rm
  - sudo su / sudo bash / sudo zsh
  - passwd
  - clear
  - exit
  - python
  - python2 (if installed on the computer)
  - python3
  - credits (not a real linux command)
  - help
  - sleep
  - reboot
  - init1

## Requirements

  - <a href="https://www.python.org">Python3.9</a> (tutorials for installation: <a href="https://www.youtube.com/watch?v=uDbDIhR76H4">Windows 10</a> | <a href="https://www.youtube.com/watch?v=0rg6nyanX5Y">Mac OS</a>).

## Installation & Launch

1- open the cmd or the terminal an type: `git clone https://github.com/Dan149/LinuxTerminalEmulator`

2- type: `cd LinuxTerminalEmulator`

3- to launch, type: `python3 script.py`

WARNING: On Windows, don't lauch the script by double-clicking on it, it can generate errors.

---------------------------------------------------------------------------------------------------
## What's new in version 0.1a ?

New feature: logging:

  In the /tmp root directory, there is a file called `log.txt`, using the root user, you can acces LTE logs by using the command `cat log.txt`.


Root user specs:

  In order to get root access of the system, you need to find the password of the root user, the password is stored in a textfile somewhere in the /home/{user} directory, good luck !
  
---------------------------------------------------------------------------------------------------
# Unsupported basic commands:
  - `cd home/Desktop` | you need to type: `cd home`, `cd Desktop`. Same process for all folders.
  - `cd /home` or others | you need to be in the root directory and type: `cd home`, and not `cd /home`, however, the `cd /`, `cd \`, `cd ~` and `cd ..` commands are working.

# // TO DO:

  - mv command
  - cp command
  - touch command
  - nano command
  - make the cd command accept multiple directory input: cd dir/dir1/
