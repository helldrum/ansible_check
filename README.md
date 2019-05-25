# dependancies

python 3.x.x

pyyaml

# description 
this tool is design to test ansible roles and ansible project an failed if the project don't respect skales5 best pratices
### if the script success output will be
```
Everything is fine, keep the good job :)
```
### if the script failed output will be
```
{some errors}
{some errors}
{some errors}
{some errors}
Now i'am sad :(
```

example
```
file /path/to/my/role/meta/main.yml not found
ERROR: some tests depend of the property galaxy_tags into /path/to/my/role/meta/main.yml please create this propertie, test exit early...
Markdown
Toggle Zen Mode
Preview

Now i'am sad :(
```
# usage

### test a role
If you run the script without parameters the script assume that the roles you want to test in on the same directory than the script
you better use the -p parameter in order to give the path to the role you want to test

```
./role_check.py -p path/to/your/role/folder
```
WARNING: this script doesn't work with multiples roles and in a full project structure (doesn't check group_var and env_var folder)  use project_check.py instead

#### role checking steps
defaults/main.yml exist and not empty
tasks/main.yml exist and not empty
tasks/install.yml  exist and not empty
meta/main.yml exist and not empty
atleast one galaxy_tags exist (role name extract from this field)
  - at this point, if the galaxy tags is not found, test script is abording

check meta/main.yml properties exist and not empty
  - meta["galaxy_info"]["author"]
  -  meta["galaxy_info"]["description"]
  -  meta["galaxy_info"]["company"]
  -  meta["galaxy_info"]["license"]
  -  meta["galaxy_info"]["min_ansible_version"]
  -  meta["galaxy_info"]["platforms"]

```
---
galaxy_info:
  author: Skale 5 <skale-5@skale-5.com>
  description: rclone roles
  company: Skale-5
  license: MIT
  min_ansible_version: 2.1
  platforms:
  - name: Debian
    versions:
    - all
  galaxy_tags:
    - rclone
```
load the file defaults/main.yml
  - if the file cannod be load, script will be abord with an Error
  - if the file doesn't have any entries but begin with --- the script will continue but script exit status will be failed
    - else check if all the entries respect the suffix convention (all defaults value should be prefixed with the role name)
    - 
load the file tasks/main.yml
  - if the file cannod be load, script will be abord with an Error
  - if the file doesn't have any entries but begin with --- the script will continue but script exit status will be failed
    - else check for each include entries
      - first tag is the name of the role (compared with the value of  ansible_galaxy_tags)
      - second tag is the name of the include file minus ".yml" (example: if include: install.yml, first tag need to be install)
      - third tag need to be exactly the concatenation between the first and the second tag separed with "-" (example rclone-install)
```
- include: install.yml
  tags:
    - rclone
    - install
    - rclone-install
```
if the folder template exist
  - check if all the template have the .j2 extention
  - check if all the template began with the string # {{ ansible managed }} or // {{ ansible_managed }}

### test a project
you need to give the  / path of the project with the parameter -p
```
./project_check.py -p path/to/your/project/folder
```
this script check the project structure and call recursively ```check_role.py``` for all the roles on the folder role

```
CHECK Project Structure
file /path/to/my/project/env_vars/preprod.yml not found
file /path/to/my/project/inventories/preprod.ini not found
Project structure not good, Now i'am sad :(


CHECK ROLE: backup-mysql

file /path/to/my/project/roles/backup-mysql/meta/main.yml not found
ERROR: some tests depend of the property galaxy_tags into /path/to/my/project/roles/backup-mysql/meta/main.yml please create this propertie, test exit early...
Now i'am sad :(


CHECK ROLE: postfix

file /path/to/my/project/roles/postfix/meta/main.yml not found
ERROR: some tests depend of the property galaxy_tags into /path/to/my/project/roles/postfix/meta/main.yml please create this propertie, test exit early...
Now i'am sad :(

End of test, Now i'am sad :(
```
#### project checking steps
the script check is thoses files exist and are not empty 

ansible.cfg
env_vars/prod.yml
env_vars/preprod.yml
inventories/prod.ini
inventories/preprod.ini
inventories/prod.ini
requirements.txt
site.yml
README.md


in  folder play check is all the files are not empty

in folder env_vars
  check if file have at least one variable
  check if all variables begin with the prefix 'env_'
  
in the file site.yml
    check if all the includes files exist on the project and not empty
    
in the group_var folder
    check if all the files are not empty
    check if all the files have at least one variable
    check if all the file respect the naming convention prefix 'file_name_'
        example:
        on group_vars/www/rclone.yml all the variable begin with 'rclone_'

    
