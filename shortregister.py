# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 06:45:19 2018

@author: erikm
"""

import mysql.connector
import requests
import datetime

# Store URL, make request and print status code
url = 'https://ssr.finanstilsynet.no/api/Issuers?extension=json'
r = requests.get(url)
print("Status code:", str(r.status_code) + "\n")

# Connect to DB
connect = mysql.connector.connect (user='root', password='', host='127.0.0.1', database='testdb')
cursor = connect.cursor()

# Store API response in a variable
response_dict = r.json()

# Flip the format of date from YYYY-MM-DD to DD-MM-YYYY
def date_flip():
    a = response_dict['LastChange'][0:4]    # Year
    b = response_dict['LastChange'][5:7]    # Month
    c = response_dict['LastChange'][8:10]   # Day
    print("Last change: " + c + "-" + b + "-" + a)

def fill_db(*args):
    connect = mysql.connector.connect (user='root', password='', host='127.0.0.1', database='testdb')
    cursor = connect.cursor()
    
    # Identify last row
    id = cursor.lastrowid

    # Create insert into command for adding to DB
    add_company = ("INSERT INTO short_register "
                    "(id, navn, shortsum, shortpercent, last_changed) "
                    "Values (%s, %s, %s, %s, %s)")

    # Define company data to add
    company_data = (id, str(response_dict['Name']), int(response_dict['ShortedSum']), float(response_dict['ShortPercent']), str(response_dict['LastChange']))
    # Execute to DB
    cursor.execute(add_company, company_data)
    # Confirm addition to DB
    print("<-- Added to DB --> \n")
    # Commit to database
    connect.commit()
    # Close connection
    cursor.close()
    connect.close()

# Loop through response, store in variables and print variables if criterias are met
for response_dict in response_dict:
    # Assign temporary variables
    company_name = response_dict['Name']
    short_percent = response_dict['ShortPercent']
    shorted_sum = response_dict['ShortedSum']
    last_change = response_dict['LastChange']

    # Removes inactive positions (>0.5 % of outstanding share count) from the list
    #if short_percent == 0.0 and shorted_sum == 0.0:
    #    pass
    #else:
    print(company_name)
    print("Short percent: " + str(short_percent))
    print("Short amount: " + str(shorted_sum))
    # Date flip function
    str(date_flip())
    # Run database function
    fill_db()