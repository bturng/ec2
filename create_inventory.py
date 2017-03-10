#!/usr/bin/python

import argparse #used to pass in arguements
import re #used for regular expressions


def exists(hostname):
    """ str -> bool
    The exists function opens the host file and checks to see if the hostname requested exists in the host file.
    It opens the host file, reads the lines, and then a for loop checks each line to see if the hostname is in it.
    If it is, True is returned. If not, False is returned.
    :param hostname:
    :return:
    """
    filename = '/usr/local/etc/ansible/hosts'
    f = open(filename, 'r')
    hostfiledata = f.readlines()
    f.close()
    for item in hostfiledata:
        if hostname in item:
            return True
    return False

def create():
    """
    The update function takes the ip address and hostname passed into the function and adds it to the host file.
    :param hostname:
    :param host_attr:
    """
    inv_file = "/usr/local/etc/ansible/inventory"

    with open(inv_file,'r') as hosts:
        for line in hosts:
            #print (line.replace(str(line).partition(' ')[0],'localhost'))
            #exit (1)
            with open('/usr/local/etc/ansible/inventory_dir/' + str(line).partition('.')[0],'w') as host_inv:
                host_inv.write(line.replace(str(line).partition(' ')[0],'localhost'))


def isValidHostname(hostname):
    """ str -> bool
    Found this on from http://stackoverflow.com/questions/2532053/validate-a-hostname-string
    First it checks to see if the hostname is too long. Next, it checks to see if the first character is a number.
    If the last character is a ".", it is removed. A list of acceptable characters is then compiled and each section
    of the host name, split by any ".", is checked for valid characters. If there everything is valid, True is returned.
    :param hostname:
    :return:
    """
    if len(hostname) > 255:
        return False
    if hostname[0].isdigit(): return False
    if hostname[-1:] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def main():

    parser = argparse.ArgumentParser(description='script to generate the inventory file for ansible')
    parser.add_argument("--add", help="Add a new host to the inventory file", required=False)
    parser.add_argument("--create", action='store_true',help="generate the inventory file", required=False)
    
    args = parser.parse_args()

    if args.add or args.create is None:
         parser.error("requires either --add or --create.")
         sys.exit(1)

    if args.create:
         create()
if __name__ == '__main__':
    main()
