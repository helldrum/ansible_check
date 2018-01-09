#!/bin/bash

echo -e "TEST:project doesn't have required files"
./project_check.py -p test/project/missing_required_files

echo -e "\n\nTEST:project site includes missformed"
./project_check.py -p test/project/missformed_site_file/

echo -e "\n\nTEST:project env not respect naming convention"
./project_check.py -p test/project/env_var_naming_convention

echo -e "\n\nTEST:project doesn't have group_vars folder"
./project_check.py -p test/project/missing_group_var_folder

echo -e "\n\nTEST: role doesn't have defaults folder"
./role_check.py -p test/no_default_folder

echo -e "\n\n\nTEST:no_task"
./role_check.py -p test/no_tasks

echo -e "\n\n\nTEST:no_task_install"
./role_check.py -p test/no_tasks_install

echo -e "\n\n\nTEST:no meta"
./role_check.py -p test/no_meta

echo -e "\n\n\nTEST:meta no galaxy-tags"
./role_check.py -p test/meta_no_galaxy-tag

echo -e "\n\n\nTEST:meta no galaxy-tags"
./role_check.py -p test/meta_no_galaxy-tag

echo -e "\n\n\nTEST:meta galaxy-tag empty"
./role_check.py -p test/meta_galaxy-tag_empty

echo -e "\n\n\nTEST:meta author empty"
./role_check.py -p test/meta_author_empty

echo -e "\n\n\nTEST:meta no author"
./role_check.py -p test/meta_no_author

echo -e "\n\n\nTEST:meta description empty"
./role_check.py -p test/meta_description_empty

echo -e "\n\n\nTEST:meta no description"
./role_check.py -p test/meta_no_description

echo -e "\n\n\nTEST:meta platforms empty"
./role_check.py -p test/meta_platforms_empty

echo -e "\n\n\nTEST:meta no platforms"
./role_check.py -p test/meta_no_platforms

echo -e "\n\n\nTEST:template file empty"
./role_check.py -p test/template_empty

echo -e "\n\n\nTEST:template file correct but no j2 extension"
./role_check.py -p test/template_not_j2

echo -e "\n\n\nTEST: task/main.yml doesn't have any include"
 ./role_check.py -p test/no_includes
