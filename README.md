#Description

To reduce the burden from the CLI, this project is created for those who
want to trigger ansible batch job on the GUI with click-mouse

##Following functions will be availiable at release V1.0

1. Simple CMDB: Groups,hosts,vars Management
2. Dynamtic Inventory: Generate preview hosts file and store into DB as well
3. Job Compose: Muti-Runjobs or roles are able to executed according to the prearranged plan
4. Review Feedback: Results of execution will be reflected on the website

##Structure of the workspace folder

/etc/ansible/
├── ansible.cfg
└── inventory
    ├── group_vars
    ├── hosts
    └── host_vars
        └── localhost.yml

