# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:33:41 2019

@author: thijs
"""
import pandas as pd
import mysql.connector
from flask import Flask

app = Flask(__name__)

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
    return int(str(x[0])+str(x[1]))
    
def getMeta(x):
    return int(x.split(';')[2].split('=')[1])    

@app.route('/filldb', methods=['GET', 'POST'])
def readFile():
    convertFile()
    df = pd.read_csv("gnomad.exomes.r2.1.1.sites.Y.vcf",sep = '\\t', comment='##', header=0)
    df = df.loc[df['ID'] != '.']
    df['#CHROM'] = df['#CHROM'].apply(convertChrom)
    df['ID'] = df['ID'].apply(convertID)
    df['POSCHROM'] = df.apply(addStuff)
    df['AF'] = df['INFO'].apply(getMeta)
    dataset = list(df[['POS', '#CHROM', 'POSCHROM', 'ID', 'REF', 'ALT', 'POS', 'AF']].itertuples(index=False, name=None))
    mydb = mysql.connector.connect(
      host="192.168.99.101",
      port="3306",
      user="user",
      passwd="pass",
      database="mydb"
    )
    mycursor = mydb.cursor()
    
    stmt = "INSERT INTO Position (position, Chromosome_ID, ID_position, REF, ALT, AF) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ID_position=ID_position;"
    mycursor.executemany(stmt, dataset)  
    mydb.commit()
    
    return (mycursor.rowcount, "record inserted.")

@app.route('/getresults', methods=['GET', 'POST'])
def get_significant(lijstje):
    mydb = mysql.connector.connect(
      host="192.168.99.101",
      port="3306",
      user="user",
      passwd="pass",
      database="mydb"
    )
    mycursor = mydb.cursor()
    #[(chr,pos, REF, ALT, AF)]
    stmt = """
    SELECT Position,
    Chromosome,
    REF,
    ALT,
    AF
    FROM Position
    WHERE Chromosome = %s AND Position = %s AND
    REF = %s AND ALT = %s AND AF < 0,1
    ;"""
    mycursor.executemany(stmt, lijstje)  
    myresult = mycursor.fetchall()
    
    return myresult

@app.route('/make_db', methods=['GET', 'POST'])
def make_db(script):
    mydb = mysql.connector.connect(
      host="192.168.99.101",
      port="3306",
      user="user",
      passwd="pass",
      database="mydb"
    )
    mycursor = mydb.cursor()
    for line in open("FileName.sql"):
        mycursor.execute(line)    
    mydb.commit()
    
if __name__ == '__main__':
    app.run(debug=True)
