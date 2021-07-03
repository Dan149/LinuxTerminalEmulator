# LinuxTerminalEmulator
### LTE is a python script which mimics the operation of a linux terminal, useful for beginners wishing to learn basic linux commands.

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

## Requirements

  - Python3.9 (tutorials: <a href="https://www.youtube.com/watch?v=uDbDIhR76H4">Windows 10</a> | <a href="https://www.youtube.com/watch?v=0rg6nyanX5Y">Mac OS</a>)

## Installation & Launch

1- open the cmd or the terminal an type: `git clone https://github.com/Dan149/LinuxTerminalEmulator`

2- type: `cd LinuxTerminalEmulator`

3- to launch, type: `python3 script.py`

WARNING: On Windows, don't lauch the script by double-clicking on it, it can generate errors.

---------------------------------------------------------------------------------------------------

# Which basic things you can't do:
  - `cd home/Desktop` | you need to type: `cd home`, `cd Desktop`. Same process for all folders.
  - `cd /home` or others | you need to be in the root directory and type: `cd home`, and not `cd /home`, however, the `cd /`, `cd \`, `cd ~` and `cd ..` commands are working.

# TO DO:

  - mv command
  - cp command
  - touch command
  - nano command
  - fake init1 command
  - fake reboot command
  - fake shutdown command
  - make the cd command accept multiple directory input: cd dir/dir1/
