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
<ul>
<li>hosts</li>
<li>puppet-master.yml</li>
<li>Create 1 x security group for each(Webservers,RDS and ELB)</li>
<li>Provision 2 x EC2 instances(Ubuntu 14.04 LTS) in 2 different AZ</li>
<li>Provision 1 x RDS instance in private subnet</li>
<li>Launch and configure public facing VPC ELB (cross_az_load_balancing) and attach VPC subnets</li>
<li>Register EC2 instances on ELB</li>
<li>Install essential and webservers role on both instances</li>
<li>Take the ELB dnsname and register/create dns entry in Route53</li>
</ul>

<p>roles
├── access-group
│   ├── tasks
│   ├── templates
│   └── vars
├── java
│   ├── defaults
│   ├── meta
│   ├── README.md
│   ├── tasks
│   ├── tests
│   └── vars
├── jenkins
│   ├── defaults
│   ├── handlers
│   ├── meta
│   ├── README.md
│   ├── tasks
│   ├── templates
│   ├── tests
│   └── vars
├── ldap
│   ├── handlers
│   ├── site.yml
│   ├── tasks
│   ├── templates
│   └── vars
├── nginx
│   ├── handlers
│   ├── meta
│   ├── tasks
│   └── templates
├── ntp
└── self_signed_certificate
    ├── tasks
    └── vars
 </p>
