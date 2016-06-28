#!/usr/bin/python

import sys
import subprocess
import argparse
import getpass
import re
import socket
import time
from time import gmtime, strftime
import paramiko

def connect_verify():

    
    parser = argparse.ArgumentParser(description='verification code for Comcast')
    parser.add_argument("--host", help="Enter the public HostName for a LDAP server", required=True)
    parser.add_argument("--user", help="Enter the UserName", required=True)
    parser.add_argument("--prikey", help="Enter the Path to the user's private Key", required=True)
    args = parser.parse_args()    
    
    ## This part runs three task
    ## 1. verify correctness of the LDAP server
    ## 2. verify configuration group named techops_dba to /etc/security/access.conf and /etc/sudoers
    ## 3. verify the NTP server

	
    k = paramiko.RSAKey.from_private_key_file(args.prikey)
    u = args.user
    h = args.host

    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print "connecting"
    c.connect( hostname = h, username = u, pkey = k ) 
    print "Connected to %s" % h

    # Send the command
    commands = [ "netstat -plan | egrep 389 | egrep 'LISTEN|ESTABLISHED'", "egrep -r techops_dba /etc/security/access.conf;egrep -r techops_dba /etc/sudoers",
                 "/usr/sbin/ntpq -p"]
    j = 1

    for command in commands:
        print "=============================================================================="
        print "Starting task %d" % j
        print "Executing {}".format( command )
        stdin , stdout, stderr = c.exec_command(command)
        print stdout.read()
        print( "Errors")
        print stderr.read()
        j += 1
    c.close()
    
    ## This is part 4  of the verification step
    ## 4. verify the security restrictions so that clients are only able to access the first host from the second host.    

    ##This test the private ip ssh connection
    ldap_private_ip = socket.gethostbyname(args.host)
    j -= 1 
    i = 1
    j += 1

    print "=============================================================================="
    print "starting task %da" %j    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print "testing ssh connection to private ip address of an Ldap server: %s" % ldap_private_ip
        ssh.connect( hostname = ldap_private_ip, username = u, pkey = k )
        print "Connected to %s" % ldap_private_ip
        print "This shows that only managment host should be only be able to connect to the ldap server"
        ssh.close
    except paramiko.AuthenticationException:
        print "Authentication failed when connecting to %s" % ldap_private_ip
        sys.exit(1)
    except:
        print "Could not SSH to %s, tring to ssh again" % ldap_private_ip
        i += 1
        time.sleep(2)

    # If we could not connect within time limit
    if i == 30:
        print "Could not connect to %s. Giving up" % host
        sys.exit(1)


    ##This parts finds the public ip address for the ldap server and tries to ssh to it
    
    i = 1

    print "=============================================================================="
    print "starting task %db" %j

    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect( hostname = ldap_private_ip, username = u, pkey = k )
    
   # Send the command
    curl_cm = "curl ipecho.net/plain ; echo"
    print "Executing {}".format(curl_cm)
    stdin , stdout, stderr = c.exec_command(curl_cm)
    ldap_public_ip = stdout.read()
    print( "Errors")
    print stderr.read()
    c.close()
    
    print "The public ip address for the ldap server is  %s" %ldap_public_ip
    while True:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print "testing ssh connection to public ip address of the Ldap server: %s" % ldap_public_ip
            ssh.connect( hostname = ldap_public_ip, username = u, pkey = k, timeout=10)
            print "Connected to %s" % ldap_public_ip
            print "The AWS security group is setup incorrectly on %s Please check the settings!" % ldap_public_ip
            break
        except paramiko.AuthenticationException:
            print "Authentication failed when connecting to %s" % ldap_public_ip
            sys.exit(1)
        except:
            print "Could not SSH to %s, tring to connection again" % ldap_public_ip
            i += 1
            time.sleep(2)

        # If we could not connect within time limit
        if i == 3:
            print "Could not connect to %s. Giving up. This shows that the public ip ldap server can not be reached" % ldap_public_ip
            sys.exit(1)

if __name__ == '__main__':
    
    connect_verify()

