#!/usr/bin/env python
import os
import subprocess

def get_script_dir(file=""):
  test_file = file
  if ("" == file):
    test_file = __file__
  scriptPath = os.path.realpath(test_file)
  scriptDir = os.path.dirname(scriptPath)
  return scriptDir

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
  cmd("git", ["fetch"], False if ("1" != config.option("update-light")) else True)
  if is_not_exit or ("1" != config.option("update-light")):
    retCheckout = cmd("git", ["checkout", "-f", config.option("branch")], True)
    if (retCheckout != 0):
      print("branch does not exist...")
      print("switching to master...")
      cmd("git", ["checkout", "-f", "master"])
    cmd("git", ["submodule", "update", "--init", "--recursive"], True)
  if (0 != config.option("branch").find("tags/")):
    cmd("git", ["pull"], False if ("1" != config.option("update-light")) else True)
    cmd("git", ["submodule", "update", "--recursive", "--remote"], True)
  os.chdir(old_cur)
  return

git_update("test2")