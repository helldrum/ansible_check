#!/bin/bash

echo -e "TEST:no_defaults\n"
./anna_ansible_check.py -p test/no_defaults

echo -e "\n\n\n"

echo -e "TEST:no_task\n"
./anna_ansible_check.py -p test/no_tasks

echo -e "\n\n\n"

echo -e "TEST:no_task_install\n"
./anna_ansible_check.py -p test/no_tasks_install

echo -e "\n\n\n"
