#!/usr/bin/python

"""
Created by:			Simon Leung
Email:  			simonleung83@gmail.com
Python version:		2.7
Date:				2017-12-13
"""


import sys			# Module to get CLI arguments
import paramiko		# Module to SSH
import sys			# Module to parse CLI arguments

""" 
Function main
"""

def send_cmd(command):
        stdin, stdout, stderr = ssh.exec_command(command) 
        # Blocks until stdout ready
        stdout.channel.recv_exit_status()
        print(stdout.read())

def main():

    if len(sys.argv) != 5:
        print "\nSyntax:"
        print 'python ssh.py <IP> <user> <password> "<command>"'
        print "Example:"
        print 'python ssh.py 1.1.1.1 user pass "ls -la"\n'

    else:
        global ssh
        ip      = sys.argv[1]
        user    = sys.argv[2]
        pw      = sys.argv[3]
        cmd     = sys.argv[4]
     
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip,username=user, password=pw, timeout=30)
            print "Connected to "+user+"@"+ ip 
            send_cmd(cmd)

                   
        except Exception as e:  
            print "Connection error: ", e
        
        ssh.close()
main()
