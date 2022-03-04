#!/usr/bin/python

"""
Created by:			Simon Leung
Python version:	2.7
Version:			  2019-07-04
"""


import commands     # Module to execute Linux commands     
import json         # Module to parse JSON data
import datetime		  # Module to print date and time
import urllib       # Module to use URL 
import smtplib      # Module to send email
import time         # Module for sleep
import csv          # Module to parse csv files

# Global vars
f = open("/var/www/html/spc/events/index.html", "w")
femail = open("/home/vtools/SPCjumpserver/scripts/stadiumEvents/email.txt", "w")

sendmail = False
today = str(datetime.datetime.now().strftime('%Y-%m-%d'))

""" 
Function main
Ticket master API: https://developer.ticketmaster.com/api-explorer/v2/
"""
def main():  
       
    # Write HTML header
    f.writelines(
    """<!--  https://www.w3schools.com/w3css/tryit.asp?filename=tryw3css_templates_webpage&stacked=h -->
    <!DOCTYPE html>
    <html lang="en">
        <link rel=icon href=/spc/css/favicon.ico>
        <link rel="stylesheet" href="/spc/css/w3.css">
        <link rel="stylesheet" href="/spc/css/w3-theme-black.css"> 
        <style>
        html,body,h1,h2,h3,h4,h5,h6 {font-family: "Roboto", sans-serif;}
        .w3-sidebar {
          z-index: 3;
          width: 250px;
          top: 43px;
          bottom: 0;
          height: inherit;
        }
        </style>  
    <body>

    <!-- Navbar -->
    <div class="w3-top">
      <div class="w3-bar w3-theme w3-top w3-left-align w3-large">
        <a class="w3-bar-item w3-button w3-right w3-hide-large w3-hover-white w3-large w3-theme-l1" href="javascript:void(0)" onclick="w3_open()"><i class="fa fa-bars"></i></a>
            <a href="/spc/index.html" class="w3-bar-item w3-button w3-theme-l1">Home</a>
            <a href="/spc/vspc/index.html" class="w3-bar-item w3-button w3-theme-l1">vSPC</a>
            <a href="#" class="w3-bar-item w3-button w3-theme-l1">SPC</a>
            <a href="/spc/contact.html" class="w3-bar-item w3-button w3-hide-small w3-hover-white">Contact</a>
      </div>
    </div>

    <!-- Sidebar -->
    <nav class="w3-sidebar w3-bar-block w3-collapse w3-large w3-theme-l5 w3-animate-left" id="mySidebar">
      <a href="javascript:void(0)" onclick="w3_close()" class="w3-right w3-xlarge w3-padding-large w3-hover-black w3-hide-large" title="Close Menu">
        <i class="fa fa-remove"></i>
      </a>
      <h4 class="w3-bar-item"><b>Menu</b></h4>
      <a class="w3-bar-item w3-button w3-hover-black" href="/spc/vspc/index.html">vSPC</a>
      <a class="w3-bar-item w3-button w3-hover-black" href="/spc/spc/index.html">SPC</a>
      <a class="w3-bar-item w3-button w3-hover-black" href="/spc/events/index.html">Stadium Events</a>
      <a class="w3-bar-item w3-button w3-hover-black" href="/spc/stadiums/index.html">Stadium Info</a>      
      <a class="w3-bar-item w3-button w3-hover-black" href="/spc/subs/index.html">SPC Subscribers</a>
    </nav>

    <!-- Main content: shift it to the right by 250 pixels when the sidebar is visible -->
    <div class="w3-main" style="margin-left:250px">
    <br/><br/>
    <div class="w3-twothird w3-container">
        <h1 class="w3-text-teal">Stadium Events</h1>      
    </div>
    <br/><a href="https://developer.ticketmaster.com/api-explorer/v2/" target="_blank">Source: Ticketmaster API</a><br/>
    """       
    )     
    
    # apikey
    apikey = "12345"
    
    # Get East stadiums events
    #==========================
    easturl = "https://app.ticketmaster.com/discovery/v2/events?apikey="+ apikey +"&venueId=KovZpZAJAJAA,KovZpZAFaeIA,ZFr9jZkk1F,KovZpZA6tdnA,KovZpZA6kvlA,KovZpZAJ6kEA,KovZpaK7Ce,KovZpa3hje,KovZpakS7e,ZFr9jZ6e7A,KovZpZAdJ1vA,KovZpa2yme,Z6r9jZkeke,KovZpZAEdFeA,KovZpZAId1JA,KovZpZAFnl1A,KovZpZAEkvtA,KovZpZA7AnJA,KovZpZAdJl7A,KovZpZAdEJEA,KovZpZAEAAeA,KovZpZAF6tIA,KovZpZAa1elA&locale=*&sort=date,name,asc&size=100"
    
    print "EAST URL:\n"+easturl+"\n"
    response = urllib.urlopen(easturl)
    eastData = json.loads(response.read())
    parse_events("EAST Events", eastData)
    
    # Add sleep to avoid timeout on second API request
    time.sleep(3)
    
    # Get West stadiums events
    #==========================
    westurl = "https://app.ticketmaster.com/discovery/v2/events?apikey="+ apikey +"&venueId=Z6r9jZAFke,KovZpa4cFe,KovZpZA6t7kA,KovZpa3Wne,KovZpaFPJe,ZFr9jZe1dk,KovZpakX1e,ZFr9jZ6Fke,KovZpZAF6ttA,Z6r9jZdAae,Z6r9jZ77ae,Z6r9jZaeee,KovZpZAFdEJA,ZFr9jZdvae,ZFr9jZd6ev,ZFr9jZeAaa,KovZpZAEknnA,KovZpa3awe,KovZpa9Ybe,KovZpZA1FlkA,KovZpZA6tdtA,KovZpZAIF7aA,KovZpakSie,KovZpZAF7E1A,KovZpZAEe6AA&locale=*&sort=date,name,asc&size=100"   
    
    print "WEST URL:\n"+westurl
    response = urllib.urlopen(westurl)    
    westData = json.loads(response.read())  
    parse_events("WEST Events", westData)    
    f.close()
    
    femail.write('For more info:<br/>')
    femail.write('<a href="https://98.132.74.35/spc/events/index.html" target="_blank">https://98.132.74.35/spc/events/index.html</a></br></br>')
    femail.close()
    
    # If there are events for today send mail
    if sendmail:
        send_email()
    

"""
Function to parse json data and save to html table
"""
def parse_events(tableName, loaded_json):
    date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    
    events = loaded_json["_embedded"]["events"]
    global sendmail     # Need to define global otherwise local variable
    
    # Write html table     
    f.write('\n<table class="w3-table-all">\n')
    f.write('<tr><th colspan="7">updated: '+date+" EST | Updates daily | Shows max 100 events</th></tr>")
    f.write('<tr><th>'+tableName+'</th><th>Date</th><th>Local Time</th><th>UTC Time</th><th>Event Type</th><th>Stadium</th><th>City</th><th>Capacity</th></tr>\n')    
    
    femail.write('<table>\n')
    femail.write('<tr><th>'+tableName+'</th><th>Date</th><th>Local Time</th><th>UTC Time</th><th>Event Type</th><th>Stadium</th><th>City</th><th>Capacity</th></tr>\n')

    
    for event in events:
        # Ignore events that has no genre       
        if "genre" in event["classifications"][0]:
            
            # Ignore events = Undefined 
            if  "Undefined" not in event["classifications"][0]["genre"]["name"]:
            
                # Ignore "tours" in event name 
                if "tours" not in event["name"].encode("utf-8").lower():
                    # Have to use encode with characters non-alphanumeric (accent)                    
                    eventName   = event["name"].encode("utf-8")
                    # Remove part of venue name to get better match
                    url         = event['url'].encode("utf-8")
                    date        = event["dates"]["start"]["localDate"]            
                    type        = event["classifications"][0]["genre"]["name"]                    
                    venue       = event["_embedded"]["venues"][0]["name"]
                    # Remove part of venue name to get better match
                    venue       = venue.replace(' | Park at the Park','').replace('Ballpark','Ball Park').replace(', Home of the Cleveland Browns','').replace('GEHA Field at ','')
                    city        = event["_embedded"]["venues"][0]["city"]["name"]
                    state       = event["_embedded"]["venues"][0]["state"]["stateCode"]
                    capacity    = "-"
                    
                    # Check if localTime key exists else print dash
                    if "localTime" in event["dates"]["start"]:
                        localTime = event["dates"]["start"]["localTime"]                
                    else:
                        localTime = "-"
                        
                    # Check if dateTime key exists else print dash
                    if "dateTime" in event["dates"]["start"]:
                        dateTime = event["dates"]["start"]["dateTime"]
                    else:
                        dateTime = "-"   

                
                    # Print to terminal
                    #====================
                    print "Event Name: "+eventName
                    print "Date: "+date
                    
                    #Check if localTime key exists
                    if "localTime" in localTime:
                        print "Local Time: "+localTime
                    else:
                        print "Local Time: -"
                    
                    # Check if dateTime key exists
                    if "dateTime" in dateTime:
                        print "UTC Time: "+dateTime
                    else:
                        print "UTC Time: -"            
                        
                    print "Event Type: "+type
                    print "Stadium: "+venue
                    print "City: "+city +", "+ state

                    # Find capacity in csv file
                    if "EAST" in tableName:
                        csvfile = open('/home/vtools/SPCjumpserver/scripts/stadiums/east_venues.csv', 'rb')
                    else:
                        csvfile = open('/home/vtools/SPCjumpserver/scripts/stadiums/west_venues.csv', 'rb')                        
                    
                    reader = csv.reader(csvfile, delimiter=',')
                    for row in reader:
                        # Convert search string lower case and remove whitespaces
                        if venue.lower().replace(" ", "") in row[1].lower().replace(" ", ""):
                            # Check contains number and not "-"
                            if "-" not in row[4]:                       
                                # add comma thousands separator
                                capacity = ('{:,}'.format(int(row[4])))                                
                                break
                    print "Capacity: "+capacity                                
                    csvfile.close() 

                    print "\n"
                    
                    # Save to html file
                    #====================
                    f.write('<tr>')
                    # Have to use encode with characters not alphanumeric
                    f.write('<td><a href="'+url+'" target="_blank">'+eventName+'</a></td>')
                    f.write('<td>'+date+'</td>')  
                    f.write('<td>'+localTime+'</td>')
                    f.write('<td>'+dateTime+'</td>')  
                    f.write('<td>'+type+'</td>')
                    f.write('<td>'+venue+'</td>')
                    f.write('<td>'+city +', '+ state+'</td>')
                    f.write('<td>'+capacity+'</td>')
                    f.write('</tr>\n')
                    
                    # Write events of today to email file 
                    # example if "2019-07-05" in date:            
                    if today in date:            
                        sendmail = True                
                        femail.write('<tr>')         
                        femail.write('<td><a href="'+url+'" target="_blank">'+eventName+'</a></td>')
                        femail.write('<td>'+date+'</td>')
                        femail.write('<td>'+localTime+'</td>')
                        femail.write('<td>'+dateTime+'</td>')  
                        femail.write('<td>'+type+'</td>')
                        femail.write('<td>'+venue+'</td>')
                        femail.write('<td>'+city +', '+ state+'</td>')
                        femail.write('<td>'+capacity+'</td>')
                        femail.write('</tr>\n')                    
            
    f.write('</table></br></br>\n')
    femail.write('</table></br></br>')


""" 
Function to send email
""" 
def send_email():
    
    vcpmail = open ("/home/vtools/SPCjumpserver/scripts/stadiumEvents/email.txt", 'r')
    recipients = [recipients@mail.com]
    message =""
    message += "Subject: INFO | Stadium Events | "+today+"\n"
    message += "To:"
    message += ", ".join(recipients) + "\n"
    message += "MIME-Version: 1.0:\n"
    message += "Content-type: text/html\n"
    message += "Content-Disposition: inline\n\n"

    for line in vcpmail.readlines():
        message += line + "<br>"

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail('vtools@mail.com',recipients, message)         
        print("\nSuccessfully sent email")
    except:
        print("Error: unable to send email")
        raise   

main()
