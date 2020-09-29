import mysql.connector
import requests
import datetime



#query = ("Select ID, Navn FROM Selskap")
def fill_db(*args):
    connect = mysql.connector.connect (user='root', password='', host='127.0.0.1', database='testdb')
    cursor = connect.cursor()

    cursor.execute("DROP TABLE short_register")
    cursor.execute("INSERT INTO short_register " 
                    "(Navn, Shortsum, Shortpercent)" 
                    "Values(company_name, shorted_sum, short_percent)")
    
    cursor.close()
    connect.close()