#!/bin/bash

echo -e "TEST:no_defaults\n"
./ansible_check.py -p test/no_defaults

echo -e "\n\n\nTEST:no_task\n"
./ansible_check.py -p test/no_tasks

echo -e "\n\n\nTEST:no_task_install\n"
./ansible_check.py -p test/no_tasks_install

echo -e "\n\n\nTEST:no meta"
./ansible_check.py -p test/no_meta

echo -e "\n\n\nTEST:meta no galaxy-tags"
./ansible_check.py -p test/meta_no_galaxy-tag

echo -e "\n\n\nTEST:meta galaxy-tags empty"
./ansible_check.py -p test/meta_no_galaxy-tag

echo -e "\n\n\nTEST:meta author empty"
./ansible_check.py -p test/meta_author_empty

echo -e "\n\n\nTEST:meta no author"
./ansible_check.py -p test/meta_no_author

echo -e "\n\n\nTEST:meta description empty"
./ansible_check.py -p test/meta_description_empty

echo -e "\n\n\nTEST:meta no description"
./ansible_check.py -p test/meta_no_description

echo -e "\n\n\nTEST:meta platforms empty"
./ansible_check.py -p test/meta_platforms_empty

echo -e "\n\n\nTEST:meta no platforms"
./ansible_check.py -p test/meta_no_platforms
