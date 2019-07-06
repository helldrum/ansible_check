# description 

this tool is design to check skale5 best pratice on ansible and project.
the goal is to trigger errors when the role or project doesn't respect convention.
Skale5 best pratice and convention will be detailled following below. 

# dependencies

python 3.x.x

pyyaml

# usage

##  role_check.py

the script role\_check.py is used to check a single ansible roles and need a mandatory parameter `-p` or  `--role_path`.

you need to use the project script is you want to test the full structure 

(project script check project structure and call the role\_check.py script for each roles found)

example:

```
./role_check.py -p path/to/your/role/folder
or ./role_check.py --role_path path/to/your/role/folder
```

## project\_check.py

project\_check.py check the full ansible project and call role\_check.py for each roles found.

this script need a mandatory parameter "-p" or "--project\_path".


## test.sh

this script is used to test all the possible errors supported by  project and role check script.

you can call this script as is

```
./test.sh
```

tests run the checking scripts on various missformed roles and project, in order to display error messages.

expected behaviour is to have ERROR messages in red and the message "Everything is fine, keep the good job :)" in green  

on project and role who respect the conventions.

please report if uncontrolled python stack message appear.


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

# role checking steps

## empty mandatory files 

defaults/main.yml exist and not empty
tasks/main.yml exist and not empty
tasks/install.yml  exist and not empty
meta/main.yml exist and not empty

## meta/main.yaml

check meta/main.yml properties exist and not empty

```
meta["galaxy_info"]["author"]
meta["galaxy_info"]["description"]
meta["galaxy_info"]["company"]
meta["galaxy_info"]["license"]
meta["galaxy_info"]["min_ansible_version"]
meta["galaxy_info"]["platforms"]
```

/!\ you need at least one existing galaxy tag

role name extract from this field at this point, if the galaxy tags is not found,

check script is abording, you should add a tag and run the script again

example of normalize meta:

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

## defaults/main.yml

  - if the file cannot be load, script will be abord with an Error
  - if the file doesn't have any entries but begin with --- the script will continue but you will have an error empty file
    - else check if all the entries respect the suffix convention (all defaults value should be prefixed with the role name)

## tasks/main.yml

  - if the file cannod be load, script will be abord with an Error
  - if the file doesn't have any entries but begin with --- the script will continue but you will have an error empty file
    - else check for each include entries
      - first tag is the name of the role (compared with the value of  ansible_galaxy_tags)
      - second tag is the name of the include file minus ".yml" (example: if include: install.yml, first tag need to be install)
      - third tag need to be exactly the concatenation between the first and the second tag separed with "-" (example rclone-install)


example or normalize main.yml

```
- include: install.yml
  tags:
    - rclone
    - install
    - rclone-install
```

## folder template exist

  - check if all the template have the .j2 extension (you should probably use a file folder if the file is not a template)
  - check if all the template began with the string # {{ ansible managed }} or // {{ ansible_managed }}

# project checking steps

## required root project files

the script check if thoses files exist and are not empty 

- we are expecting at least 2 envs prod and preprod
- basic ansible.cfg file
- requirements.txt should have the ansible version and dependancies use for this project  
- README.md in order to give project context
- site.yml (the main ansible file with all playbooks includes)

```
ansible.cfg
env_vars/prod.yml
env_vars/preprod.yml
inventories/prod.ini
inventories/preprod.ini
inventories/prod.ini
requirements.txt
site.yml
README.md
```

## folder play

check is all the files are not empty
whe don't want empty playbook file

## folder env_vars

in order to use variable precedence in an organise way
- check if file have at least one variable
- check if all variables begin with the prefix 'env_'
  
## file site.yml

- check if all the includes files exist on the project and not empty

## group var folder

- check if all the files are not empty
- check if all the files have at least one variable
- check if all the file respect the naming convention prefix 'file_name_'

example:

```
on group_vars/www/rclone.yml all the variable begin with 'rclone_'
```
