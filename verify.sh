#/bin/bash

##This is a program to verify the following items
## 1. verify correctness of the LDAP server
## 2. verify configuration group named “techops_dba” to /etc/security/access.conf and /etc/sudoers
## 3. verify the NTP server
## 4. verify the security restrictions so that clients are only able to access the first host from the second host.


##First verification
echo "STARTING TO VERFIY LDAP SERVER....."
ansible -i /etc/ansible/ec2/hosts ldapserver -u ec2-user -m shell -a 'netstat -plan | egrep 389 | egrep "LISTEN|ESTABLISHED'
ansible -i /etc/ansible/ec2/hosts ldapserver -u ec2-user -m shell -a 'echo exit | telnet 0 389'
echo "LDAP SERVER VERIFICATION DONE...."
echo "--------------------------------"

##Second verification
echo "STARTING TO VERFIY GROUP NAME....."
ansible -i /etc/ansible/ec2/hosts ldapserver -u ec2-user -m shell -a 'egrep -r techops_dba /etc/security/access.conf'
ansible -i /etc/ansible/ec2/hosts ldapserver -u ec2-user -m shell -a 'egrep -r techops_dba /etc/sudoers'
echo "GROUPNAME VERIFICATION DONE...."
echo "--------------------------------"

##Third verification
echo "STARTING TO VERFIY NTP SERVER....."
ansible -i /etc/ansible/ec2/hosts ldapserver -u ec2-user -m shell -a '/usr/sbin/ntpq -p'
echo "NTP SERVER VERIFICATION DONE...."
echo "--------------------------------"

##Fourth verification
echo "STARTING TO VERFIY SSH CONNECTION....."
LDAP_PRIVATE_ADDR=`ansible  -i /etc/ansible/ec2/hosts ldapserver -u ec2-user -m setup -a 'filter=ansible_eth0' | egrep -A 1 ipv4 | egrep address | awk -F'\"' {'print $4'}`

ansible -i /etc/ansible/ec2/hosts management -u ec2-user -m shell -a "nmap -p 22 -Pn $LDAP_PRIVATE_ADDR"

LDAP_PUBLIC_ADDR=`cat /etc/ansible/ec2/hosts | egrep -A 1 ldapserver | egrep ansible | awk {'print $1'}`

ansible -i /etc/ansible/ec2/hosts management -u ec2-user -m shell -a "nmap -p 22 -Pn $LDAP_PUBLIC_ADDR"
echo "SSH CONNECTION VERIFICATION DONE...."
echo "--------------------------------"

