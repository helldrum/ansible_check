#!/usr/bin/python
#coding:utf8

import os
import sys
import yaml
import re
from optparse import OptionParser

global return_code
global project_path

def check_args():
  global project_path

  parser = OptionParser()
  parser.add_option("-p", "--project_path", dest="project_path",
                  help="path to the project")
  (options, args) = parser.parse_args()

  if options.project_path is None:
    print "property project_path is mandatory, exiting ..."
    sys.exit(2)

  if not os.path.exists(options.project_path):
    print "path {} not valid".format(options.project_path)
    sys.exit(2)
  else:
    project_path=options.project_path

def yaml_load(filename):
  with open(filename, 'r') as stream:
      try:
          return (yaml.load(stream))
      except yaml.YAMLError as exc:
          print(exc)

def _check_file_exist_not_empty(current_file):
  global project_path
  global return_code
  try:
    assert(os.path.exists(current_file)), "file {} not found".format(current_file)
    assert(os.path.getsize(current_file) > 0), "file {} is empty".format(current_file)
  except (AssertionError, OSError) as e:
    return_code = 2
    print e

def check_default_files():
  global project_path

  _check_file_exist_not_empty("{}/{}".format(project_path , "ansible.cfg"))
  _check_file_exist_not_empty("{}/{}".format(project_path , "env_vars/prod.yml"))
  _check_file_exist_not_empty("{}/{}".format(project_path , "env_vars/preprod.yml"))
  _check_file_exist_not_empty("{}/{}".format(project_path , "inventories/prod.ini"))
  _check_file_exist_not_empty("{}/{}".format(project_path , "inventories/preprod.ini"))
  _check_file_exist_not_empty("{}/{}".format(project_path , "inventories/prod.ini"))
  _check_file_exist_not_empty("{}/{}".format(project_path , "requirements.txt"))
  _check_file_exist_not_empty("{}/{}".format(project_path , "site.yml"))
  _check_file_exist_not_empty("{}/{}".format(project_path , "README.md"))

  try:
    for filename in os.listdir("{}/plays".format(project_path)):
      _check_file_exist_not_empty("{}/plays/{}".format(project_path , filename))

  except (AssertionError, OSError) as e:
    code_return = 2
    print e

def check_env_vars():
  global project_path
 
  try:
    for filename in os.listdir("{}/env_vars".format(project_path)):
      current_env_file = "{}/env_vars/{}".format(project_path, filename)
      env_vars = yaml_load(current_env_file)

      if env_vars is None:
        print "file {} doesn't have any variables".format(current_env_file)
        return_code = 2
      else:
        for var_name in env_vars:
          if re.match("^env_.*", var_name) is None:
            print "{} propertie dont respect the naming convention prefix env_ into {}".format(
            var_name, 
            current_env_file
            )
            return_code = 2
  except (IOError, KeyError, OSError) as e:
    print "Error: folder {}/env_vars is empty .".format(project_path)
    return_code = 2


def check_group_vars():
  global project_path

  try:
    for group_folder in os.listdir("{}/group_vars".format(project_path)):
      try:
        for group_file in os.listdir("{}/group_vars/{}".format(project_path, group_folder)):
          _check_file_exist_not_empty("{}/group_vars/{}".format(project_path, group_folder))

      except (IOError, KeyError, OSError) as e:
        print "Error: folder {}/group_vars is empty .".format(project_path)
        return_code = 2

  except (IOError, KeyError, OSError) as e:
    print "Error: folder {}/group_vars is empty .".format(project_path)
    return_code = 2

def main():
  global return_code
  return_code = 0

  check_args()
  print "Heather Say :"
  check_default_files()
  check_env_vars()
  check_group_vars()
  if return_code is 0 :
    print "Everything is fine, keep the good job :)"
  else:
   print "Now i'am sad :("

  sys.exit(return_code)

if __name__ == '__main__':
  main()
 

