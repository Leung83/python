#!/usr/bin/python

"""
Created by:			  Simon Leung
Python version:		2.7
Version:			    2020-03-15
"""

  
import json         # Module to parse JSON data
import datetime		  # Module to print date and time
import urllib       # Module to use URL 
import time         # Module for time functions
import bs4 as bs    # Module Beautifulsoup to parse HTML

# Global vars
f = open("/var/www/html/spc/stadiums/index.html", "w")
capacity = "-"
league = "-"
teams = "-"


""" 
Function main parses stadium capacity info from Wikipedia pages
Ticket master API: https://developer.ticketmaster.com/api-explorer/v2/
MLB: https://en.m.wikipedia.org/wiki/List_of_U.S._baseball_stadiums_by_capacity
NFL: https://en.m.wikipedia.org/wiki/List_of_current_National_Football_League_stadiums
NBA: https://en.m.wikipedia.org/wiki/List_of_National_Basketball_Association_arenas
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
        <h1 class="w3-text-teal">Stadium Info</h1>      
    </div>
    <br/><a href="https://developer.ticketmaster.com/api-explorer/v2/" target="_blank">Source: Ticketmaster API and Wikipedia</a><br/>
    <a href="/spc/stadiums/west_venues.csv">west_venues.csv</a><br/>
    <a href="/spc/stadiums/east_venues.csv">east_venues.csv</a><br/>
    """       
    ) 
    
    apikey = "12345"
      
    eastVenues = ["KovZpZAJAJAA","KovZpZAFaeIA","ZFr9jZkk1F","KovZpZA6tdnA","KovZpZA6kvlA","KovZpZAJ6kEA","KovZpaK7Ce","KovZpa3hje","KovZpakS7e","ZFr9jZ6e7A","KovZpZAdJ1vA","KovZpa2yme","Z6r9jZkeke","KovZpZAEdFeA","KovZpZAId1JA","KovZpZAFnl1A","KovZpZAEkvtA","KovZpZA7AnJA","KovZpZAdJl7A","KovZpZAdEJEA","KovZpZAEAAeA","KovZpZAF6tIA","KovZpZAa1elA"]
    
    westVenues = ["Z6r9jZAFke","KovZpa4cFe","KovZpZA6t7kA","KovZpa3Wne","KovZpaFPJe","ZFr9jZe1dk","KovZpakX1e","ZFr9jZ6Fke","KovZpZAF6ttA","Z6r9jZdAae","Z6r9jZ77ae","Z6r9jZaeee","KovZpZAFdEJA","ZFr9jZdvae","ZFr9jZd6ev","ZFr9jZeAaa","KovZpZAEknnA","KovZpa3awe","KovZpa9Ybe","KovZpZA1FlkA","KovZpZA6tdtA","KovZpZAIF7aA","KovZpakSie","KovZpZAF7E1A","KovZpZAEe6AA"]
    
    date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    
     # Write html table     
    f.write('\n<table class="w3-table-all">\n')
    f.write('<tr><th colspan="7">updated: '+date+" EST | Updates quartily</th></tr>")
    f.write('<tr><th>EAST Venues</th><th>Timezone</th><th>City</th><th>Capacity</th><th>League</th><th>Home Team</th><th>Lat/Long</th></tr>\n')  
    
    for id in eastVenues:
        url = "https://app.ticketmaster.com/discovery/v2/venues/"+id+"?apikey="+ apikey +"&locale=en"
        print(url)
        response = urllib.urlopen(url)
        venueData = json.loads(response.read())
        # function to parse json data
        parse_venue(venueData)
        # Add timer to avoid API rate limit
        time.sleep(0.1)
    
    f.write('</table></br></br>\n')
    
     # Write html table     
    f.write('\n<table class="w3-table-all">\n')
    f.write('<tr><th colspan="7">updated: '+date+" EST | Updates quartily</th></tr>")
    f.write('<tr><th>WEST Venues</th><th>Timezone</th><th>City</th><th>Capacity</th><th>League</th><th>Home Team</th><th>Lat/Long</th></tr>\n')
    
    for id in westVenues:
        url = "https://app.ticketmaster.com/discovery/v2/venues/"+id+"?apikey="+ apikey +"&locale=en"
        print(url)
        response = urllib.urlopen(url)
        venueData = json.loads(response.read())
        # function to parse json data
        parse_venue(venueData)
        # Add timer to avoid API rate limit
        time.sleep(0.1)        
    
    f.write('</table></br></br>\n')
    f.close()
    
"""
Function to parse json data and save to html table
"""
def parse_venue(json):
    global capacity,league,teams
    date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
       
    # Have to use encode with characters non-alphanumeric (accent)
    name        = json["name"].encode("utf-8")
    timezone    = json['timezone']
    city        = json["city"]["name"]
    state       = json["state"]["stateCode"] 
    long        = json["location"]["longitude"]
    lat         = json["location"]["latitude"]

    # Remove part of venue name to get better match
    filtername = name.replace(' | Park at the Park','').replace('Ballpark','Ball Park').replace(', Home of the Cleveland Browns','').replace('GEHA Field at ','')
    find_capacity(filtername)

    # Save to html file
    f.write('<tr>')
    #f.write('<td><a href="'+url+'" target="_blank">'+name+'</a></td>')
    f.write('<td>'+filtername+'</td>')
    f.write('<td>'+timezone+'</td>')  
    f.write('<td>'+city+', '+state+'</td>')
    f.write('<td>'+capacity+'</td>')
    f.write('<td>'+league+'</td>')
    f.write('<td>'+teams+'</td>')   
    f.write('<td><a href="https://maps.google.com/?q='+lat+','+long+'" target="_blank">'+lat+'<br/>'+long+'</a></td>')
    f.write('</tr>\n')  
        

def find_capacity(name):
    global capacity,league,teams
    capacity = "-"
    league = "-"
    teams = "-"  
    
    path = "/home/vtools/SPCjumpserver/scripts/stadiums/"
   
 
    # Search NFL Stadiums
    with open(path+"nfl_stadiums.json") as json_file:  
        loaded_json = json.loads(json_file.read())
        for key, value in loaded_json["Name"].items():
            # Convert search string lower case and remove whitespaces
            if name.lower().replace(" ", "") in value.lower().replace(" ", ""):
                #print key, value
                teams = loaded_json["Team(s)"][key]
                league = "NFL"
                # Remove text after left square bracket
                num = str(loaded_json["Capacity"][key]).split('[', 1)[0]
                # add comma thousands separator
                capacity = ('{:,}'.format(int(num)))
                return 
                
    # Search NBA Stadiums
    with open(path+"nba_stadiums.json") as json_file:  
        loaded_json = json.loads(json_file.read())
        for key, value in loaded_json["Arena"].items():
            # Convert search string lower case and remove whitespaces
            if name.lower().replace(" ", "") in value.lower().replace(" ", ""):
                #print key, value
                teams = loaded_json["Team(s)"][key]
                league = "NBA"
                # Remove text after left square bracket
                num = str(loaded_json["Capacity"][key]).split('[', 1)[0]
                # add comma thousands separator
                capacity = ('{:,}'.format(int(num)))
                return                
                
    # Search MLB Stadiums
    with open(path+"mlb_stadiums.json") as json_file:  
        loaded_json = json.loads(json_file.read())
        for key, value in loaded_json["Stadium"].items():
            # Convert search string lower case and remove whitespaces
            if name.lower().replace(" ", "") in value.lower().replace(" ", ""):
                #print key, value
                teams = loaded_json["Home Team(s)"][key]
                league = "MLB"
                # Remove text after left square bracket and remove comma
                num = str(loaded_json["Capacity"][key]).split('[', 1)[0].replace(',','')
                # add comma thousands separator
                capacity = ('{:,}'.format(int(num))) 
                return                

    # Search Other venues
    with open(path+"other_venues.json") as json_file:  
        loaded_json = json.loads(json_file.read())
        for key, value in loaded_json["Venue"].items():
            # Convert search string lower case and remove whitespaces
            if name.lower().replace(" ", "") in value.lower().replace(" ", ""):
                #print key, value
                teams = loaded_json["Team(s)"][key]
                league = loaded_json["League"][key]
                # Remove text after left square bracket and remove comma
                num = str(loaded_json["Capacity"][key]).split('[', 1)[0].replace(',','')
                # add comma thousands separator
                capacity = ('{:,}'.format(int(num)))
                return                  
main()
