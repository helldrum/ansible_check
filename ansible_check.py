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


def check_meta_main():
  global return_code
  global role_path
  global role_name
  global role_platform

  try: 
    meta=yaml_load(role_path + "/meta/main.yml")
    role_name=meta["galaxy_info"]["galaxy_tags"][0]
  except (IOError, KeyError) as e:
    print "ERROR: some tests depend of the property galaxy_tags into meta/main.yml please create this propertie"
    print "Now i'am sad :("
    sys.exit(2)

  try:
    meta=yaml_load(role_path + "/meta/main.yml")
    role_platform=meta["galaxy_info"]["platforms"][0]["name"]
  except (IOError, KeyError, TypeError) as e:
    print "ERROR: some tests depend of the property [\"galaxy_info\"][\"platforms\"][0][\"name\"] into meta/main.yml please create this propertie"
    print "Now i'am sad :("
    sys.exit(2)

  try:
    meta["galaxy_info"]["author"]
    if not meta["galaxy_info"]["author"]:
      print "the key [\"galaxy_info\"][\"author\"] is empty into meta/main.yml"
      return_code = 2
  except KeyError as e:
    print "the key [\"galaxy_info\"][\"author\"] is missing into meta/main.yml"
    return_code = 2

  try:
    meta["galaxy_info"]["description"]
    if not meta["galaxy_info"]["description"]:
      print "the key [\"galaxy_info\"][\"description\"] is empty into meta/main.yml"
      return_code = 2
  except KeyError as e:
    print "the key [\"galaxy_info\"][\"description\"] is missing into meta/main.yml"
    return_code = 2

  try:
    meta["galaxy_info"]["company"]
    if not meta["galaxy_info"]["company"]:
      print "the key [\"galaxy_info\"][\"company\"] is empty into meta/main.yml"
      return_code = 2
  except KeyError as e:
    print "the key [\"galaxy_info\"][\"company\"] is missing into meta/main.yml"
    return_code = 2

  try:
    meta["galaxy_info"]["license"]
    if not meta["galaxy_info"]["license"]:
      print "the key [\"galaxy_info\"][\"licence\"] is empty into meta/main.yml"
      return_code = 2
  except KeyError as e:
    print "the key [\"galaxy_info/\"][\"license\"] is missing into meta/main.yml"
    return_code = 2

  try:
    meta["galaxy_info"]["min_ansible_version"]
    if not meta["galaxy_info"]["min_ansible_version"]:
      print "the key [\"galaxy_info\"][\"min_ansible_version\"] is empty into meta/main.yml"
      return_code = 2
  except KeyError as e:
    print "the key [\"galaxy_info\"][\"min_ansible_version\"] is missing into meta/main.yml"
    return_code = 2

  return return_code


def check_default_files():
  global return_code
  global role_path
 
  try:
    assert(os.path.exists(role_path + "/defaults/main.yml")), "file defaults/main.yml not found"
    assert(os.path.getsize(role_path + "/defaults/main.yml") > 0 ), "file defaults/main.yml is empty"
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
    assert(os.path.exists(role_path + "/meta")),"folder meta not found"
    assert(os.path.exists(role_path + "/meta/main.yml")), "file meta/main.yml not found"
    assert(os.path.getsize(role_path + "/meta/main.yml") > 0 ), "file meta/main.yml is empty"
  except AssertionError as e:
    return_code = 2
    print e


def check_defaults_main():
  global return_code
  global role_path
  global role_name

  try:
    default_main=yaml_load("{}/defaults/main.yml".format(role_path))    
  except IOError as e:
    print "FATAL: can't open the file {}/defaults/main.yml , this file is required for playbook run.".format(role_path)
    print "test end  before the end"
    print "Now, i'am sad :("
    sys.exit(2)

  # default/main.yml  check naming convention
  if default_main is None:
    print "file {}/defaults/main.yml doesn't have any variables".format(role_path)
    return_code = 2
  else:
    for var_name in default_main:
     if re.match("^{}.*".format(role_name), var_name) is None:
       print "{} propertie dont respect the naming convention prefix {}_ into {}/defaults/main.yml".format(
         var_name, 
         role_name, 
         role_path
       ) 
       return_code =2


def check_tasks_main():

  global return_code
  global role_path
  global role_name

  #tasks/main.yml check tags convention
  try:
    tasks_main=yaml_load("{}/tasks/main.yml".format(role_path))
  except IOError as e:
    print "FATAL: can't open the file {}/tasks/main.yml, this file is required for playbook run.".format(role_path)
    print "test end  before the end"
    print "Now, i'am sad :("
    sys.exit(2)
  
  if tasks_main is None:
    print "file {}/tasks/main.yml doesn't have any entries".format(role_path)
    return_code = 2
  else:
    for entrie in tasks_main:
      include_name=entrie["include"].split(".yml", 1)[0]

      try:
        if entrie["tags"][0] != role_name :
          print "first tag for include {} should be {}, get {} instead into task/main.yml".format(
            include_name,
            role_name,
            entrie["tags"][0])
      except IndexError as e:
        print  "tag {} is missing on include {} into task/main.yml".format(role_name,include_name)

      try:
        if entrie["tags"][1] != include_name :
          print "second tag for include {} should be {}, get {} instead into task/main.yml".format(
            include_name,
            include_name,
            entrie["tags"][1])
      except IndexError as e:
        print  "tag {} is missing on include {} into task/main.yml".format(include_name,include_name)

      try:
        tag3= "{}-{}".format(role_name,include_name)
        if entrie["tags"][2] != tag3 :
          print "third tag for include {} should be {}, get {} instead into task/main.yml".format(
            include_name,
            tag3,
            entrie["tags"][2])

      except IndexError as e:
        print  "tag {} is missing on include {} into task/main.yml".format(include_name,include_name)
        return_code = 2


def check_templates():
  global return_code
  global role_path

  try:
     for template_filename in os.listdir(role_path+"/templates/"):
       full_template_path="{}/templates/{}".format(role_path, template_filename)

       if not template_filename.endswith(".j2"):
         print "file {} in folder template doesn't have the extension j2".format(template_filename)
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
         print "file {} doesn't have any templated variables so it's a static file and not a template.".format(full_template_path)
         return_code = 2
  except OSError:
    pass # no templates folder (not required)



def main():
  global return_code
  return_code = 0
  
  check_args()
  print "Heather Say :"

  check_default_files()
  check_meta_main()
  check_defaults_main()
  check_tasks_main()
  check_templates()

  if return_code is 0 :
    print "Everything is fine, keep the good job :)"
  else:
   print "Now i'am sad :("

  sys.exit(return_code)


if __name__ == '__main__':
  main()
  
