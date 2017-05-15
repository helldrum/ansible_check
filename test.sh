#!/bin/bash

echo -e "TEST:no_defaults\n"
./role_check.py -p test/no_defaults

echo -e "\n\n\nTEST:no_task\n"
./role_check.py -p test/no_tasks

echo -e "\n\n\nTEST:no_task_install\n"
./role_check.py -p test/no_tasks_install

echo -e "\n\n\nTEST:no meta"
./role_check.py -p test/no_meta

echo -e "\n\n\nTEST:meta no galaxy-tags"
./role_check.py -p test/meta_no_galaxy-tag

echo -e "\n\n\nTEST:meta galaxy-tags empty"
./role_check.py -p test/meta_no_galaxy-tag

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

echo -e "\n\n\nTEST:template file correct but no templated variable on it"
./role_check.py -p test/template_not_templated_var

