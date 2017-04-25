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

def check_env_vars():
  global project_path
  
  for filename in os.listdir("{}/env_vars".format(project_path)):
    current_env_file = "{}/env_vars/{}".format(project_path, filename)
    try:
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

    except (IOError, KeyError) as e:
      print "Error: unexpected error when open the file {}.".filename
      sys.exit(2)
    

def main():
  global return_code
  return_code = 0

  check_args()
  print "Heather Say :"
  check_env_vars()

if __name__ == '__main__':
  main()
 

