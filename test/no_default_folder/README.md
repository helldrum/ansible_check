# SKALE-5 Ansible role: Rclone

## Description

Rclone is a command line program to sync files and directories to and from

- Google Drive
- Amazon S3
- Openstack Swift / Rackspace cloud files / Memset Memstore
- Dropbox
- Google Cloud Storage
- Amazon Drive
- Microsoft One Drive
- Hubic
- Backblaze B2
- Yandex Disk
- The local filesystem

## Install

	git remote add remote_role_rclone git@git.sk5.io:roles/rclone.git 
	git subtree add --prefix roles/rclone remote_role_rclone master

See `defaults/main.yml` for usage.

## Links

- [rclone docs](http://rclone.org/)
- [rclone official repo](https://github.com/stefangweichinger/ansible-rclone)