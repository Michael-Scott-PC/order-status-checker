# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 21:37:02 2019

@author: mseno
"""

import pymysql

# Connect to database
db = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='', db='ordertrackerdb')

# Pepare a cursor object using curser() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("USE ordertrackerdb;")
cursor.execute("SHOW tables;")

# Fetch a single row using fetchone() method.
row = cursor.fetchall()

print(row)
    
# Disconnect from server
db.close()