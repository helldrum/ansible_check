#!/usr/bin/python
#coding:utf8

import os
import sys
import yaml
import re
from optparse import OptionParser

global return_code
global role_path
global role_name

def check_args():
  global role_path

  parser = OptionParser()
  parser.add_option("-p", "--role_path", dest="role_path",
                  help="path to the role")
  (options, args) = parser.parse_args()

  if options.role_path is None:
    print "Error: parameter --role_path mandatory ..."
    sys.exit(2)

  if not os.path.exists(options.role_path):
    print "path {} not valid".format(options.role_path)
    sys.exit(2)
  else:
    role_path=options.role_path


def yaml_load(filename):
  global role_name
  with open(filename, 'r') as stream:
      try:
          return (yaml.load(stream))
      except yaml.YAMLError as exc:
          print(exc)

def _check_file_exist_not_empty(current_file):
  global role_path
  global return_code
  try:
    assert(os.path.exists(current_file)), "file {} not found".format(current_file)
    assert(os.path.getsize(current_file) > 0), "file {} is empty".format(current_file)
  except (AssertionError, OSError) as e:
    return_code = 2
    print e

def check_meta_main():
  global return_code
  global role_path
  global role_name
  global role_platform

  meta_file_path = "{}/{}".format(role_path, "meta/main.yml") 

  try:
    meta=yaml_load(meta_file_path)
    role_name=meta["galaxy_info"]["galaxy_tags"][0]
  except (IOError, KeyError) as e:
    print "ERROR: some tests depend of the property galaxy_tags into {} please create this propertie".format(meta_file_path)
    sys.exit(2)

  try:
    meta=yaml_load(meta_file_path)
    role_platform=meta["galaxy_info"]["platforms"][0]["name"]
  except (IOError, KeyError, TypeError) as e:
    print "ERROR: some tests depend of the property [\"galaxy_info\"][\"platforms\"][0][\"name\"], it's not exist into {}".format(meta_file_path)
    sys.exit(2)

  try:
    meta["galaxy_info"]["author"]
    if not meta["galaxy_info"]["author"]:
      print "the key [\"galaxy_info\"][\"author\"] is empty into {}".format(meta_file_path)
      return_code = 2
  except KeyError as e:
    print "the key [\"galaxy_info\"][\"author\"] is missing into {}".format(meta_file_path)
    return_code = 2

  try:
    meta["galaxy_info"]["description"]
    if not meta["galaxy_info"]["description"]:
      print "the key [\"galaxy_info\"][\"description\"] is empty into {}".format(meta_file_path)
      return_code = 2
  except KeyError as e:
    print "the key [\"galaxy_info\"][\"description\"] is missing into {}".format(meta_file_path)
    return_code = 2

  try:
    meta["galaxy_info"]["company"]
    if not meta["galaxy_info"]["company"]:
      print "the key [\"galaxy_info\"][\"company\"] is empty into {}".format(meta_file_path)
      return_code = 2
  except KeyError as e:
    print "the key [\"galaxy_info\"][\"company\"] is missing into {}".format(meta_file_path)
    return_code = 2

  try:
    meta["galaxy_info"]["license"]
    if not meta["galaxy_info"]["license"]:
      print "the key [\"galaxy_info\"][\"licence\"] is empty into {}".format(meta_file_path)
      return_code = 2
  except KeyError as e:
    print "the key [\"galaxy_info/\"][\"license\"] is missing into {}".format(meta_file_path)
    return_code = 2

  try:
    meta["galaxy_info"]["min_ansible_version"]
    if not meta["galaxy_info"]["min_ansible_version"]:
      print "the key [\"galaxy_info\"][\"min_ansible_version\"] is empty into {}".format(meta_file_path)
      return_code = 2
  except KeyError as e:
    print "the key [\"galaxy_info\"][\"min_ansible_version\"] is missing into {}".format(meta_file_path)
    return_code = 2

  return return_code


def check_default_files():
  global return_code
  global role_path

  _check_file_exist_not_empty("{}/{}".format(role_path, "defaults/main.yml")) 
  _check_file_exist_not_empty("{}/{}".format(role_path, "tasks/main.yml")) 
  _check_file_exist_not_empty("{}/{}".format(role_path, "meta/main.yml"))
  _check_file_exist_not_empty("{}/{}".format(role_path, "tasks/main.yml"))

def check_defaults_main():
  global return_code
  global role_path
  global role_name
 
  default_main_path = "{}/defaults/main.yml".format(role_path) 
  try:
    default_main=yaml_load(default_main_path)    
  except IOError as e:
    print "FATAL: can't open the file , this file is required for playbook run.".format(default_main_path)
    print "test end  before the end"
    sys.exit(2)

  # default/main.yml  check naming convention
  if default_main is None:
    print "file {} doesn't have any variables".format(default_main_path)
    return_code = 2
  else:
    for var_name in default_main:
     if re.match("^{}.*".format(role_name), var_name) is None:
       print "{} propertie dont respect the naming convention prefix {}_ into {}.".format(
         var_name, 
         role_name, 
         default_main_path
       ) 
       return_code =2


def check_tasks_main():

  global return_code
  global role_path
  global role_name

  file_task_main_path = "{}/tasks/main.yml".format(role_path)
  try:
    tasks_main=yaml_load(file_task_main_path)
  except IOError as e:
    print "FATAL: can't open the file {}, this file is required for playbook run.".format(file_task_main_path)
    print "test end  before the end"
    print "Now, i'am sad :("
    sys.exit(2)
  
  if tasks_main is None:
    print "file {} doesn't have any entries".format(file_task_main_path)
    return_code = 2
  else:
    for entrie in tasks_main:
      include_name=entrie["include"].split(".yml", 1)[0]

      try:
        if entrie["tags"][0] != role_name :
          print "first tag for include {} should be {}, get {} instead into {}".format(
            include_name,
            role_name,
            entrie["tags"][0],
            file_task_main_path
          )
      except IndexError as e:
        print  "tag {} is missing on include {} into {}".format(role_name, include_name, file_task_main_path)

      try:
        if entrie["tags"][1] != include_name :
          print "second tag for include {} should be {}, get {} instead into {}".format(
            include_name,
            include_name,
            entrie["tags"][1],
            file_task_main_path
          )
      except IndexError as e:
        print  "tag {} is missing on include {} into {}".format(include_name, include_name, file_task_main_path)

      try:
        tag3= "{}-{}".format(role_name,include_name)
        if entrie["tags"][2] != tag3 :
          print "third tag for include {} should be {}, get {} instead into {}.".format(
            include_name,
            tag3,
            entrie["tags"][2],
            file_task_main_path
          )

      except IndexError as e:
        print  "tag {} is missing on include {} into {}.".format(include_name, include_name, file_task_main_path)
        return_code = 2


def check_templates():
  global return_code
  global role_path

  try:
     for template_filename in os.listdir(role_path+"/templates/"):
       full_template_path="{}/templates/{}".format(role_path, template_filename)

       if not template_filename.endswith(".j2"):
         print "file {} in folder template doesn't have the extension j2".format(full_template_path)
         return_code = 2

       try:
         assert(os.path.getsize(full_template_path) > 0 ), "file {} is empty".format(full_template_path)
       except AssertionError as e:
         return_code = 2
         print e

       with open(full_template_path ,"r") as f:
         firstline = f.readline()

         if not template_filename.endswith(".json.j2"):
           if ("# {{ ansible_managed }}" not in  firstline) and ("// {{ ansible_managed }}" not in  firstline):
              return_code = 2
              print "first line of template file {} need to be # {{{{ ansible_managed }}}} or {{{{ ansible_managed }}}}".format(full_template_path)
              

       flag=False
       with open(full_template_path ,"r") as f:
         lines=f.readlines()
       
       for line in lines:
         if "{{" in line:
           if "ansible_managed" not in line:
             flag=True

       if not flag:
         print "file {} doesn't have any templated variables".format(full_template_path)
         return_code = 2
  except OSError:
    pass # no templates folder (not required)



def main():
  global return_code
  return_code = 0
  check_args()
  check_default_files()
  check_meta_main()
  check_defaults_main()
  check_tasks_main()
  check_templates()

if __name__ == '__main__':
  main()
  
