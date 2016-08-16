# ec2
AWS example

These playbooks are configuration files that used to provision AWS instances using Ansible:

This root directory in include roles that will provision a ec2 instance and deploy a fully functional jenkin server with ldap server 

verify.py is python script I developed to verify the functionality of ldap server and creation of access-group, please cat verify.py for more comments

The following playbooks are found in  ansible galaxy and I modified to fit my need. 
ansible-aws-roles
ansible-roles-docker
ansible-aws-vpc-ha-wordpress

Here is the directory structure for my root amazon playbook

hosts
puppet-master.yml
README.md
roles
site.yml
verify.py
verify.sh


roles

├── access-group

├── java

├── jenkins

├── ldap

├── nginx

├── ntp

└── self_signed_certificate
 
