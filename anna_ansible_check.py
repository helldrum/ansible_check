#!/usr/bin/python
import os, sys
import yaml
import re
from optparse import OptionParser

def yaml_load(filename):
  with open(filename, 'r') as stream:
      try:
          return (yaml.load(stream))
      except yaml.YAMLError as exc:
          print(exc)

def check_args():
  parser = OptionParser()
  parser.add_option("-p", "--role_path", dest="role_path",
                  help="path to the role")
  (options, args) = parser.parse_args()

  if options.role_path is None:
    options.role_path="."

  if not os.path.exists(options.role_path):
    print "path {} not valid".format(options.role_path)
    sys.exit(2)
  else:
    return options.role_path

def main():

  role_path=check_args()
  return_code = 0
  print "Anna Say :"
  
  try:
    assert(os.path.exists(role_path + "/defaults/main.yml")), "file defaults/main.yml not found"
    assert(os.path.getsize(role_path + "/defaults/main.yml") > 0 ), "file defaults/main.yml is empty"
  except AssertionError as e:
    return_code = 2
    print e
  
  try: 
    assert(os.path.exists(role_path + "/meta")),"folder meta not found"
    assert(os.path.exists(role_path + "/meta/main.yml")), "file meta/main.yml not found"
    assert(os.path.getsize(role_path + "/meta/main.yml") > 0 ), "file meta/main.yml is empty" 
  except AssertionError as e:
    return_code = 2
    print e
  
  try:
    assert(os.path.exists(role_path + "/tasks")),"folder tasks not found"
    assert(os.path.exists(role_path + "/tasks/main.yml")), "file tasks/main.yml not found"
    assert(os.path.getsize(role_path + "/tasks/main.yml") > 0 ), "file tasks/main.yml is empty"
  except AssertionError as e:
    return_code = 2
    print e
  
  try:
    assert(os.path.exists(role_path + "/tasks/install.yml")), "file tasks/install.yml not found"
    assert(os.path.getsize(role_path + "/tasks/install.yml") > 0 ), "file tasks/install.yml is empty"
  except AssertionError as e:
    return_code = 2
    print e
  
  try: 
    meta=yaml_load(role_path + "/meta/main.yml")
    meta["galaxy_info"]["galaxy_tags"][0]
  except IOError as e:
    print "ERROR: some tests depend of galaxy_tags into meta/main.yml please create this file"

  if return_code is 0 :
    print "Everything is fine, keep the good job :)"
  else:
   print "Now i'am sad :("


if __name__ == '__main__':
  main()
  
