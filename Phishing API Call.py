# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 09:59:43 2019

Author: Jason Richmond
Purpose: Open API connection to CoFense website using the users CoFense token in order to download Phishing Data to CSV or TXT
file.

"""
from urllib.request import Request, urlopen
import json
import urllib.request
import re
import string
import time
from schema import Schema, And, Use, Optional, SchemaError
import os




#######################################################
#######################################################
###############   API Call to CoFense #################
#######################################################
#######################################################
def API_Call():

    # Uses users' token generated on CoFense site to open JSON list of URLs containing Phishing Data
    token = ("Token token=%r" % (APItoken))
    token = token.replace("'",'"')
    
    url = "https://login.phishme.com/api/v1/scenarios.json"
    request = urllib.request.Request(url)
    request.add_header('Authorization', token)
    response = urllib.request.urlopen(request)
    html = response.read()
    
    
    # uncomment the below if you wish to see the list of files/URLs in the JSON request
    #print(html)
    #url_check(Schema, html)
 

    # Parses the JSON response to get most current URL for CSV
    y = json.loads(html)
    x = y[0]  #[0] will return the top row
    
    
    # Validates headers and data types recevied using Schema below.  Will escape to error handler if not validated
    Schema.validate(x)
    #validated = Schema.validate(x)
    #print(validated)
    
    # Uncomment to show URL being passed to pull data
    #print(x["full_csv_url"])
      
    
    response.close()
    title = x["title"]
    recipients = x["recipients"]
    date = x["date_started"]
    date = date[0:10]


    # Takes the URL for the most current file and opens connection and exports data
    site= str(x["full_csv_url"])
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    req.add_header('Authorization', token)

    with urlopen(req) as x:
        data = x.read().decode('utf-8')

    # Export data to CSV file names 
    print("Connection established.  Downloading Phishing data now.")
    
    # Strip out trailing new line and all non-printable chars from dataset
    csv_data = data.rstrip()
    csv_data = re.sub(r'[^{0}\n]'.format(string.printable), '', csv_data)
    
    
    col_headers = data.partition('\n')[0]
    col_headers_nbr = col_headers.count(",") + 1
    split_data = col_headers.split(",")
    
   
    if test_CSV(split_data,col_headers_nbr) == True:
        
        filename = "Phishing Data - " + title + ".csv"
        outputfilename = os.path.join(filePath, filename)
        
        print(csv_data, file=open(outputfilename,"w+", newline=""))
        #print("File Exported: " & outputfilename & "; Test Date: " + date + "; Responses: " + str(recipients))
        print("File Exported: %r; Test Date: %r; Responses: %r" % (outputfilename, date, str(recipients)))
        
    else:
        print("\nProcess halted.  \nErrors found in CSV headers, either extra fields or missing fields.  \nSee error message for details.\n")
       
    
    

#######################################################
#######################################################
###############   CSV Test Function ###################
#######################################################
#######################################################
def test_CSV(split_data,col_headers_nbr):
    
    # list of expected headers for CSV file.  Will be compared to ensure we do not
    #  receive extra headers or there are no missing headers
    csv_headers = 'Email,Recipient Name,Recipient Group,Department,Location,Opened Email?,Opened Email Timestamp,Clicked Link?,Clicked Link Timestamp,Submitted Form,Username,Entered Password?,Submitted Form Timestamp,Reported Phish?,New/Repeat Reporter,Reported Phish Timestamp,Time to Report (in seconds),Remote IP,GeoIP Country,GeoIP City,GeoIP ISP,Last DSN,Last Email Status,Last Email Status Timestamp,Language,Browser,User-Agent,Mobile?,Seconds Spent on Education Page,SUPERVISOR,DIVISION,EXECUTIVE,MISC.,Location State,Employee Number,Job Name,Supervisor Email Address,1 Down From Executive,Employment Category,Date Of Hire,Length Of Service,Work At Home,HR Admin Email Address,Submitted Data'
    split_cvs_hdr = csv_headers.split(",") 
    a = 0   # Loop variable to count the number of errors
    
    try:
        for x in range(0, col_headers_nbr):
            yy = str(split_data[x].strip().lower())
            zz = str(split_cvs_hdr[x].strip().lower())
            
            if yy == zz:
                a +=0
            else:
                a += 1
        
        print('Number of errors in CSV file header:', a)
        
        if a == 0:
            return True
        else:
            return False
            
        
    except:        
        pass # Catch exception but pass it so all errors can be captured and logged





    
#######################################################
#######################################################
##################   MAIN PROGRAM #####################
#######################################################
#######################################################

# initialize global variables 
# used in error handling HTTPError loop        
int = 1
# Get token code from profile page on CoFense website.  Is specific to login user
APItoken=input("Enter API Token:")
filePath = "YOUR PATH HERE"

change = input("The Default file path is: YOUR PATH HERE \nDo you wish to export to a different location? (Yes/No) ")
validInput = False

while validInput == False:
    if change.lower() == "no":
        validInput = True
    elif change.lower() == "yes":
        filePath = input("Enter the new filepath here: ")
        print("You entered: %r" %(filePath))
        validInput = True
    else:
        change = input("Enter either Yes or No only. ")
        validInput = False
    

    

# used in field validation in API call.  Will compare the list below to list of fields found in API call
Schema = Schema({
             'id': And(str), 
             'title': And(str), 
             'scenario_type': And(str), 
             'date_started': And(str), 
             'date_finished':  And(str), 
             'responses': And(Use(float)), 
             'full_csv_url':  And(str), 
             'recipients': And(Use(float)),  
             'notes': And(str)
             })

try:
    print("Attempting to login into CoFense and pull most current data.")
    API_Call()
    
    
    
# So far all exceptions are due to the "cooldown" time required between connections with CoFense.  
# Process will loop 3 times and wait 30 seconds between attempts between failures.
except urllib.error.HTTPError as e:
    print("Process Failed with error: ")
    print(e)
    int +=1
    if int < 3:
        print("Waiting 30 seconds and will try again")
        time.sleep(30)
        print("Processing attempt #" + str(int))
        API_Call()
    else:
        print("Process already attempted twice.  Please try again later.")


except SchemaError as se:
    print(se)
        

except Exception as err:    
    print(err)
