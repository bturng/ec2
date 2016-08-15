# ec2
AWS example

This are configuration files that used to provision instances using Ansible:

This root directory in include roles that will provision a ec2 instance and deploy a fully functional jenkin server and ldap server 

verify.py is python script I developed to verify the functionality of ldap server and creation of access-group, please cat virify for more comments

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
 
