#!/usr/bin/env python
import platform
import os
import subprocess

def host_platform():
  ret = platform.system().lower()
  if (ret == "darwin"):
    return "mac"
  return ret

def get_script_dir(file=""):
  test_file = file
  if ("" == file):
    test_file = __file__
  scriptPath = os.path.realpath(test_file)
  scriptDir = os.path.dirname(scriptPath)
  return scriptDir

def get_path(path):
  if "windows" == host_platform():
    return path.replace("/", "\\")
  return path

def is_dir(path):
  return os.path.isdir(get_path(path))

def cmd(prog, args=[], is_no_errors=False):  
  ret = 0
  if ("windows" == host_platform()):
    sub_args = args[:]
    sub_args.insert(0, get_path(prog))
    ret = subprocess.call(sub_args, stderr=subprocess.STDOUT, shell=True)
  else:
    command = prog
    for arg in args:
      command += (" \"" + arg + "\"")
    ret = subprocess.call(command, stderr=subprocess.STDOUT, shell=True)
  if ret != 0 and True != is_no_errors:
    sys.exit("Error (" + prog + "): " + str(ret))
  return ret

def git_update(repo, is_no_errors=False, is_current_dir=False):
  print("[git] update: " + repo)
  url = "https://github.com/trofim24/test2.git"
  folder = get_script_dir() + "/../" + repo
  is_not_exit = False
  if not is_dir(folder):
    retClone = cmd("git", ["clone", url, folder], is_no_errors)
    if retClone != 0:
      return
    is_not_exit = True
  old_cur = os.getcwd()
  os.chdir(folder)
  cmd("git", ["fetch"], False)
  cmd("git", ["pull"], False)
  
  os.chdir(old_cur)
  return

git_update("test2")