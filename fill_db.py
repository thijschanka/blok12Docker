# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:33:41 2019

@author: thijs
import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.99.101",
  port="3306",
  user="user",
  passwd="pass",
  database="mydb"
)


print(mydb)


mycursor = mydb.cursor()

sql = "INSERT INTO Chromosome (ID, Name) VALUES (%s, %s)"
val = (23, "y")
mycursor.execute(sql, val)

sql = "INSERT INTO Position (ID_position, Chromosome_ID) VALUES (%s, %s)"
val = (200, 23)
mycursor.execute(sql, val)

sql = "INSERT INTO Stats (ID_stats, REF, ALT, Position_ID_position) VALUES (%s, %s, %s, %s)"
val = (238692, 'A', 'F', 200)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
"""
import pandas as pd
import mysql.connector
def convertFile():
    file = open("gnomad.exomes.r2.1.1.sites.Y.vcf")
    lines = ''.join(file.readlines())
    file.close()
    file= open("gnomad.exomes.r2.1.1.sites.Y.tsv", 'w+')
    file.write(lines)
    file.close

def convertChrom(x):
    if x in ['y', 'Y']:
        x = 23
    if x in ['x', 'X']:
        x = 24
    return int(x)

def convertID(x):
    x = x[2:]
    return int(x)

def addStuff(x):
    print(x)
    return int(str(x[0])+str(x[1]))
    
def getMeta(x):
    return int(x.split(';')[2].split('=')[1])    

def readFile():
    convertFile()
    df = pd.read_csv("gnomad.exomes.r2.1.1.sites.Y.vcf",sep = '\\t', comment='##', header=0)
    df = df.loc[df['ID'] != '.']
    df['#CHROM'] = df['#CHROM'].apply(convertChrom)
    df['ID'] = df['ID'].apply(convertID)
    df['POSCHROM'] = df.apply(addStuff)
    df['AF'] = df['INFO'].apply(getMeta)
    dataset2 = list(df[['POS', '#CHROM', 'POSCHROM']].itertuples(index=False, name=None))
    dataset3 = list(df[['ID', 'REF', 'ALT', 'POS', 'AF']].itertuples(index=False, name=None))
    
    mydb = mysql.connector.connect(
      host="192.168.99.101",
      port="3306",
      user="user",
      passwd="pass",
      database="mydb"
    )
    mycursor = mydb.cursor()
    
    stmt2 = "INSERT INTO Position (position, Chromosome_ID, ID_position) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE ID_position=ID_position;"
    stmt3 = "INSERT INTO Stats (ID_stats, REF, ALT, Position_ID_position, AF) VALUES (%s, %s, %s, %s %s) ON DUPLICATE KEY UPDATE ID_stats=ID_stats;"
    mycursor.executemany(stmt2, dataset2)
    mycursor.executemany(stmt3, dataset3)  
    mydb.commit()
    
    print(mycursor.rowcount, "record inserted.")    
     
readFile()       