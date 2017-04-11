# description 
this script is design to test ansible roles an failed if the roles don't respect skales5 best pratices
if the script success output will be
```
Anna say:
Everything is fine, keep the good job :)
```
if the script failed output will be
```
Anna say:
{some errors}
{some errors}
{some errors}
{some errors}
Now i'am sad :(
```

# usage
if you run the script without parameters the script assume that the roles you want to test in on the same directory than the script
you better use the -p parameter in order to give the path to the role you want to test

```
./anna_ansible_check.py -p path/to/your/role/folder
```
WARNING:script doesn't work now with multiples roles and in a full project structure (doesn't check group_var and env_var folder) 

# checking steps
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

load the file defaults/main.yml
  - if the file cannod be load, script will be abord with an Error
  - if the file doesn't have any entries but begin with --- the script will continue but script exit status will be failed
    - else check if all the entries respect the suffix convention (all defaults value should be prefixed with the role name)

load the file tasks/main.yml
  - if the file cannod be load, script will be abord with an Error
  - if the file doesn't have any entries but begin with --- the script will continue but script exit status will be failed
    - else check for each include entries
      - first tag is the name of the role (compared with the value of  ansible_galaxy_tags)
      - second tag is the name of the include file minus ".yml" (example: if include: install.yml, first tag need to be install)
      - third tag need to be exactly the concatenation between the first and the second tag separed with "-" (example rclone-install)

# features in progress
- check if all the template have the .j2 extention
- check if the template files have atleast one variable (unless is a plain text file and not a template)  
- check if all the template began with the string #{ansible managed}
- check if all the apt module use with item statement 
