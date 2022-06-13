#!/usr/bin/env python3
# coding:utf8

import os
import sys
import yaml
import re
from optparse import OptionParser

global role_return_code
global role_path
global role_name

GREEN_COLOR = '\x1b[6;30;42m'
RED_COLOR = '\x1b[6;30;41m'
RESET_COLOR = '\x1b[0m'

def check_args():
    global role_path

    parser = OptionParser()
    parser.add_option("-p", "--role_path",
    dest = "role_path", help = "path to the role")
    (options, args) = parser.parse_args()

    if options.role_path is None:
        print ("ERROR: arg parameter --role_path mandatory, exiting ...")
        sys.exit(2)

    if not os.path.exists(options.role_path):
        print ("ERROR: arg role path {} not valid".format(options.role_path))
        sys.exit(2)
    else:
        role_path = options.role_path


def yaml_load(filename):
    global role_name
    with open(filename, 'r') as stream:
        try:
            return (yaml.load(stream, Loader=yaml.SafeLoader))
        except yaml.YAMLError as exc:
            print(exc)

def _check_file_exist_not_empty(current_file):
    global role_path
    global role_return_code
    try:
        assert(os.path.exists(
            current_file)), RED_COLOR + "FATAL : file {} not found".format(
            current_file) + RESET_COLOR

        # file contain at leat 1 character
        assert(os.path.getsize(
            current_file) > 1), RED_COLOR + "FATAL : file {} is empty".format(
            current_file) + RESET_COLOR
    except (AssertionError, OSError) as e:
        role_return_code = 2
        print (e)

def check_meta_main():
    global role_return_code
    global role_path
    global role_name
    global role_platform

    meta_file_path = "{}/{}".format(role_path, "meta/main.yml")

    try:
        meta = yaml_load(meta_file_path)
        role_name = meta["galaxy_info"]["galaxy_tags"][0]
        role_name = role_name.replace("-", "_")
    except (IOError, KeyError, AttributeError, TypeError, IndexError):
        print (RED_COLOR + "ERROR: some tests depend of the property galaxy_tags into {} \
        \nplease create this propertie, test exit early...".format(
            meta_file_path) + RESET_COLOR)
        print (RED_COLOR + "Now i'am sad :(" + RESET_COLOR)
        sys.exit(2)

    try:
        pattern = "[a-z0-9_]*"
        if re.match(pattern, role_name) is None or re.match(
                pattern, role_name).group() is not role_name:
            raise KeyError
    except (KeyError):
        print (RED_COLOR + "ERROR: property galaxy_tags into {} doesn't match\
pattern {} give '{}' match '{}' \
\nplease fix this propertie, test exit early...".format(
            meta_file_path, pattern, role_name,
            re.match(pattern, role_name).group()) + RESET_COLOR)
        print (RED_COLOR + "Now i'am sad :(" + RESET_COLOR)
        sys.exit(2)

    try:
        meta = yaml_load(meta_file_path)
        role_platform = meta["galaxy_info"]["platforms"][0]["name"]
    except (IOError, KeyError, TypeError):
        print (RED_COLOR + "ERROR: some tests depend of the property\
[\"galaxy_info\"][\"platforms\"][0][\"name\"], it's not exist into {} ,\
test exit early...".format(meta_file_path) + RESET_COLOR)
        print (RED_COLOR + "Now i'am sad :(" + RESET_COLOR)
        sys.exit(2)

    try:
        meta["galaxy_info"]["author"]
        if not meta["galaxy_info"]["author"]:
            print (RED_COLOR + "the key [\"galaxy_info\"][\"author\"]\
is empty into {}".format(meta_file_path) + RESET_COLOR)
            role_return_code = 2
    except KeyError:
        print (RED_COLOR + "the key [\"galaxy_info\"][\"author\"]\
is missing into {}".format(meta_file_path) + RESET_COLOR)
        role_return_code = 2

    try:
        meta["galaxy_info"]["description"]
        if not meta["galaxy_info"]["description"]:
            print (RED_COLOR + "the key [\"galaxy_info\"][\"description\"]\
is empty into {}".format(meta_file_path) + RESET_COLOR)
            role_return_code = 2
    except KeyError:
        print (RED_COLOR + "the key [\"galaxy_info\"][\"description\"]\
is missing into {}".format(meta_file_path) + RESET_COLOR)
        role_return_code = 2

    try:
        meta["galaxy_info"]["company"]
        if not meta["galaxy_info"]["company"]:
            print (RED_COLOR + "the key [\"galaxy_info\"][\"company\"]\
is empty into {}".format(meta_file_path) + RESET_COLOR)
            role_return_code = 2
    except KeyError:
        print (RED_COLOR + "the key [\"galaxy_info\"][\"company\"]\
is missing into {}".format(meta_file_path) + RESET_COLOR)
        role_return_code = 2

    try:
        meta["galaxy_info"]["license"]
        if not meta["galaxy_info"]["license"]:
            print (RED_COLOR + "the key [\"galaxy_info\"][\"licence\"]\
is empty into {}".format(meta_file_path) + RESET_COLOR)
            role_return_code = 2
    except KeyError:
        print (RED_COLOR + "the key [\"galaxy_info/\"][\"license\"]\
is missing into {}".format(meta_file_path) + RESET_COLOR)
        role_return_code = 2

    try:
        meta["galaxy_info"]["min_ansible_version"]
        if not meta["galaxy_info"]["min_ansible_version"]:
            print (RED_COLOR + "the key [\"galaxy_info\"][\"min_ansible_version\"]\
is empty into {}".format(meta_file_path) + RESET_COLOR)
            role_return_code = 2
    except KeyError:
        print (RED_COLOR + "the key [\"galaxy_info\"][\"min_ansible_version\"]\
is missing into {}".format(meta_file_path) + RESET_COLOR)
        role_return_code = 2

    return role_return_code


def check_default_files():
    global role_return_code
    global role_path

    _check_file_exist_not_empty("{}/{}".format(role_path, "tasks/main.yml"))
    _check_file_exist_not_empty("{}/{}".format(role_path, "meta/main.yml"))
    _check_file_exist_not_empty("{}/{}".format(role_path, "tasks/install.yml"))


def check_defaults_main():
    global role_return_code
    global role_path
    global role_name

    default_main_path = "{}/defaults/main.yml".format(role_path)
    try:
        default_main = yaml_load(default_main_path)
    except IOError:
        print (RED_COLOR + "FATAL: can't open the file {} ,\
role doesn't have default values.".format(default_main_path) + RESET_COLOR)
        print (RED_COLOR + "test end  before the end" + RESET_COLOR)
        print (RED_COLOR + "Now, i'am sad :(" + RESET_COLOR)

        sys.exit(2)

    # default/main.yml  check naming convention
    if default_main is None:
        print (RED_COLOR + "file {} doesn't have any default value.".format(
            default_main_path) + RESET_COLOR)
        role_return_code = 2
    else:
        for var_name in default_main:
            if re.match("^{}.*".format(role_name), var_name) is None:
                print (RED_COLOR + "{} propertie dont respect the naming \
convention prefix {}_ into {}.".format(
                  var_name,
                  role_name,
                  default_main_path
                ) + RESET_COLOR)
                role_return_code = 2


def _resolve_includes_name(dict_to_resolve):
    try:
        if dict_to_resolve["include"]:
            return "include"
    except(KeyError, TypeError):
        pass

    try:
        if dict_to_resolve["import_tasks"]:
            return "import_tasks"
    except(KeyError, TypeError):
        pass

    try:
        if dict_to_resolve["include_tasks"]:
            return "include_tasks"
    except(KeyError, TypeError):
        pass


def check_tasks_main():

    global role_return_code
    global role_path
    global role_name

    file_task_main_path = "{}/tasks/main.yml".format(role_path)
    try:
        tasks_main = yaml_load(file_task_main_path)
    except IOError:
        print (RED_COLOR + "FATAL: can't open the file {},\
this file is required for playbook run.".format(
            file_task_main_path) + RESET_COLOR)
        print (RED_COLOR + "test end  before the end" + RESET_COLOR)
        print (RED_COLOR + "Now, i'am sad :(" + RESET_COLOR)
        sys.exit(2)

    if tasks_main is None:
        print (RED_COLOR + "file {} doesn't have any entries".format(
            file_task_main_path) + RESET_COLOR)
        role_return_code = 2

    else:
        for entrie in tasks_main:
            try:
                include_name = entrie[_resolve_includes_name(
                    entrie)].split(".yml", 1)[0]
            except (KeyError, TypeError):
                print (RED_COLOR + "ERROR:\
some tests depend of the includes files and tags,\
it's not exist into {} , test exit early...".format(
                    file_task_main_path) + RESET_COLOR)
                print (RED_COLOR + "possible dict values are include,\
include_tasks, import_tasks" + RESET_COLOR)
                print (RED_COLOR + "Now i'am sad :(" + RESET_COLOR)
                sys.exit(2)

            try:
                if entrie["tags"][0] != role_name:
                    print (RED_COLOR + "first tag for include '{}' should be '{}',\
get '{}' instead into {}".format(
                        include_name, role_name,
                        entrie["tags"][0], file_task_main_path
                    ) + RESET_COLOR)
                    role_return_code = 2

            except (IndexError, KeyError):
                print (RED_COLOR + "tag '{}' is missing on include\
 '{}' \into {}".format(
                    role_name, include_name,
                    file_task_main_path
                ) + RESET_COLOR)
                role_return_code = 2

            try:
                if entrie["tags"][1] != include_name:
                    print (RED_COLOR + "second tag for include '{}' should be '{}', \
 get '{}' instead into {}".format(
                        include_name, include_name,
                        entrie["tags"][1], file_task_main_path
                    ) + RESET_COLOR)
                    role_return_code = 2

            except (IndexError, KeyError):
                print (RED_COLOR + "tag '{}' is missing on include '{}' \
into {}".format(
                    include_name, include_name,
                    file_task_main_path) + RESET_COLOR)
                role_return_code = 2

            try:
                tag3 = "{}-{}".format(role_name, include_name)
                if entrie["tags"][2] != tag3:
                    print (RED_COLOR + "third tag rolename-includename \
for include '{}' should be '{}', get {} instead into {}.".format(
                        include_name, tag3,
                        entrie["tags"][2], file_task_main_path) + RESET_COLOR)
                    role_return_code = 2

            except (IndexError, KeyError):
                print (RED_COLOR + "tag rolename-includename is missing on include {} \
into {}.".format(
                    include_name, file_task_main_path) + RESET_COLOR)
                role_return_code = 2


def check_templates():
    global role_return_code
    global role_path

    try:
        for template_filename in os.listdir(role_path+"/templates/"):
            full_template_path = "{}/templates/{}".format(
                role_path, template_filename)

        if not template_filename.endswith(".j2"):
            print (RED_COLOR + "file {} in folder template doesn't \
have the extension j2".format(full_template_path) + RESET_COLOR)
            role_return_code = 2

        try:
            assert(os.path.getsize(full_template_path) > 0), RED_COLOR + "file {} \
is empty".format(full_template_path) + RESET_COLOR
        except AssertionError as e:
            role_return_code = 2
            print (e)

        with open(full_template_path, "r") as f:
            template_content = f.read()
            if not template_filename.endswith(".json.j2"):
                if "{{ ansible_managed }}" not in template_content:
                    role_return_code = 2
                    print (RED_COLOR + "template file {} need to have \
the variable {{{{ ansible_managed }}}}".format(
                        full_template_path
                    ) + RESET_COLOR)

    except OSError:
        pass  # no templates folder (not required)


def main():
    global role_return_code
    role_return_code = 0
    check_args()
    check_default_files()
    check_meta_main()
    check_defaults_main()
    check_tasks_main()
    check_templates()


    if role_return_code == 0:
        print (GREEN_COLOR + "Everything is fine, \
keep the good job :)" + RESET_COLOR)
    else:
        print (RED_COLOR + "Now i'am sad :(" + RESET_COLOR)

    sys.exit(role_return_code)


if __name__ == '__main__':
    main()
