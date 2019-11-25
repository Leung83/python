#!/usr/bin/python

"""
Created by:			Simon Leung
Email:  			simonleung83@gmail.com
Python version:		2.7
Date:				2018-08-31
"""


from ciscoconfparse import CiscoConfParse   # Module to parse Cisco conf files, "pip install --upgrade ciscoconfparse" or "easy_install -U ciscoconfparse"
import sys			                        # Module to parse CLI arguments

""" 
Function main
"""
def main():

    if len(sys.argv) != 4:
        print "\nSyntax: "
        print "python ciscoconfparser.py <cfg_file> <parent> <child>"
        print "python ciscoconfparser.py <cfg_file> vlan name \t\t\t - Shows vlan and network names"
        print "python ciscoconfparser.py <cfg_file> fex description \t\t - Shows fex and description"
        print "python ciscoconfparser.py <cfg_file> interface description \t - Shows interface and description"
        print "python ciscoconfparser.py <cfg_file> interface vlan \t\t - Shows interface and vlan"        
        print ""
    
    else:     
        
        try:
            filename = sys.argv[1]
            parent = sys.argv[2]
            child = sys.argv[3]
            
            # Open config file
            file = CiscoConfParse(filename)
            # Search parent and child string
            list = file.find_objects_w_child("^"+parent, child)
            
            for obj in list:

                for ch in obj.children:          
                    if ch.text.find(child) != -1:                 
                         print obj.text + "\t",
                         # Remove child text from printout
                         split = ch.text.split(child)
                         print split[1]
                         
        except Exception as e:  
            print "Error: ", e
        
main()
