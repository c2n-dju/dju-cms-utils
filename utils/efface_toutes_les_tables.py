#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import sys
import getpass
import os

# Drop all tables from a given database

try:
    base = os.environ['DJBASE']
except KeyError:
    print("Vous avez oublié : export DJBASE=base_XXXXX_XX")    
    exit(22)

baba = input("si la base est " + base + ", tapez son nom : ")
if baba != base:
    print("Vous avez fait une faute de frappe ou bien vous ne comprenez pas les risques ! Abandon.")
    exit(22)

testVar = input("Certain d'effacer toutes les tables de la base " + base + " ? (taper OUI ou NON) ")

if testVar != "OUI":
    print("Abandon.")
    exit(22)

try:
    conn = psycopg2.connect("dbname='" + base + "'")
    conn.set_isolation_level(0)
except:
    print("Unable to connect to the database.")
    exit(22)

cur = conn.cursor()

try:
    cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
    rows = cur.fetchall()
    for row in rows:
        print("dropping table: ", row[1])   
        cur.execute("drop table " + row[1] + " cascade") 
    cur.close()
    conn.close()        
except:
    print("Error: ", sys.exc_info()[1])
