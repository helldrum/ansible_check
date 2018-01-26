#!/bin/bash

echo -e "TEST:project doesn't have required files"
./project_check.py -p test/project/missing_required_files

echo -e "TEST:project required files are empty"
./project_check.py -p test/project/empty_required_files

echo -e "\n\nTEST:project site includes missformed"
./project_check.py -p test/project/missformed_site_file/

echo -e "\n\nTEST:project env not respect naming convention"
./project_check.py -p test/project/env_var_naming_convention

echo -e "\n\nTEST:project doesn't have group_vars folder"
./project_check.py -p test/project/missing_group_var_folder

echo -e "\n\nTEST:project group_vars doesn't respect the naming convention"
./project_check.py -p test/project/group_vars_missformed

echo -e "\n\nTEST: role doesn't have defaults folder"
./role_check.py -p test/no_default_folder

echo -e "\n\n\nTEST: role doesn't have task folder"
./role_check.py -p test/no_tasks

echo -e "\n\n\nTEST:role doesn't have the task install"
./role_check.py -p test/no_tasks_install

echo -e "\n\n\nTEST:role doesn't have meta folder"
./role_check.py -p test/no_meta

echo -e "\n\n\nTEST:role meta file doesn't have a galaxy tags"
./role_check.py -p test/meta_no_galaxy-tag

echo -e "\n\n\nTEST:role meta file have the var galaxy-tag empty"
./role_check.py -p test/meta_galaxy-tag_empty

echo -e "\n\n\nTEST:role meta file doesn't have the var author"
./role_check.py -p test/meta_no_author

echo -e "\n\n\nTEST:role meta file have the var author empty"
./role_check.py -p test/meta_author_empty

echo -e "\n\n\nTEST:role meta file have the var description empty"
./role_check.py -p test/meta_description_empty

echo -e "\n\n\nTEST:role meta file doesn't have the var description"
./role_check.py -p test/meta_no_description

echo -e "\n\n\nTEST:role meta file have the var platforms empty"
./role_check.py -p test/meta_platforms_empty

echo -e "\n\n\nTEST:role meta file doesn't have the var platforms"
./role_check.py -p test/meta_no_platforms

echo -e "\n\n\nTEST:role have a template file empty"
./role_check.py -p test/template_empty

echo -e "\n\n\nTEST:role have one template file with no j2 extension"
./role_check.py -p test/template_not_j2

echo -e "\n\n\nTEST:role file task/main.yml doesn't have any includes"
 ./role_check.py -p test/no_includes

echo -e "\n\n\nTEST:role can use keywords import_tasks or include_tasks or include"
./role_check.py -p test/include_import_tasks_include_tasks
