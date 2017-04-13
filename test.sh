#!/bin/bash

echo -e "TEST:no_defaults\n"
./anna_ansible_check.py -p test/no_defaults

echo -e "\n\n\nTEST:no_task\n"
./anna_ansible_check.py -p test/no_tasks

echo -e "\n\n\nTEST:no_task_install\n"
./anna_ansible_check.py -p test/no_tasks_install

echo -e "\n\n\nTEST:no meta"
./anna_ansible_check.py -p test/no_meta

echo -e "\n\n\nTEST:meta no galaxy-tags"
./anna_ansible_check.py -p test/meta_no_galaxy-tag

echo -e "\n\n\nTEST:meta galaxy-tags empty"
./anna_ansible_check.py -p test/meta_no_galaxy-tag

echo -e "\n\n\nTEST:meta author empty"
./anna_ansible_check.py -p test/meta_author_empty

echo -e "\n\n\nTEST:meta no author"
./anna_ansible_check.py -p test/meta_no_author

echo -e "\n\n\nTEST:meta description empty"
./anna_ansible_check.py -p test/meta_description_empty

echo -e "\n\n\nTEST:meta no description"
./anna_ansible_check.py -p test/meta_no_description

echo -e "\n\n\nTEST:meta platforms empty"
./anna_ansible_check.py -p test/meta_platforms_empty

echo -e "\n\n\nTEST:meta no platforms"
./anna_ansible_check.py -p test/meta_no_platforms
