# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:33:41 2019

@author: thijs
"""
import pandas as pd
import mysql.connector
from flask import Flask, jsonify, request
from os import listdir

app = Flask(__name__)

def convertChrom(x):
    if x in ['y', 'Y']:
        x = 23
    if x in ['x', 'X']:
        x = 24
    return int(x)

def convertID(x):
    x = x[2:]
    return int(x)
    
def getMeta(x):
    return float(x.split(';')[2].split('=')[1])    

@app.route('/filldb', methods=['GET', 'POST'])
def readFile():
    files = listdir("/data/insert/")
    rowsinsert = 0
    mydb = mysql.connector.connect(
     host="db",
     port="3306",
     user="root",
     passwd="root",
     database="mydb"
    )
    mycursor = mydb.cursor()
    for bestand in files:
        df = pd.read_csv("/data/insert/"+bestand,sep = '\\t', comment='##', header=0)
        df = df.loc[df['ID'] != '.']
        df['#CHROM'] = df['#CHROM'].apply(convertChrom)
        df['ID'] = df['ID'].apply(convertID)
        df['AF'] = df['INFO'].apply(getMeta)
        dataset = list(df[['POS', '#CHROM', 'ID', 'REF', 'ALT', 'AF']].itertuples(index=False, name=None))
        
        stmt = "INSERT INTO Position (position, Chromosome, ID_position, REF, ALT, AF) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ID_position=ID_position;"
        mycursor.executemany(stmt, dataset)  
        mydb.commit()
        rowsinsert += mycursor.rowcount
    return (str(rowsinsert), "record inserted.")

def read_data(bestand):
    datalist = []
    
    with open('/data/querry/'+bestand) as f:
        for line in f:
            #datalist.append(tuple
            lijstje = (line.replace('\n','').split(','))
            lijstje[1] = int(lijstje[1])
            lijstje[0] = convertChrom(lijstje[0])
            datalist.append(tuple(lijstje))
    return datalist

@app.route('/getresults',methods = ['POST', 'GET'])
def get_significant():
    bestand = request.json.get('bestand')
    lijstje = read_data(bestand)
    mydb = mysql.connector.connect(
      host="db",
      port="3306",
      user="root",
      passwd="root",
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
    WHERE AF < 0.1"""
    if len(lijstje) != 0:
        stmt += 'AND Chromosome = %s AND Position = %s AND REF = %s AND ALT = %s'
    stmt += ' ;'
    #mycursor.executemany(stmt, lijstje)
    payload = []
    for data in lijstje:
        mycursor.execute(stmt, data)
        myresult = mycursor.fetchall()
    
        
        for result in myresult:
           content = {'pos': result[0], 'chr': result[1], 'ref': result[2], 'alt': result[3], 'af': result[4]}
           payload.append(content)
           content = {}
    
    return jsonify(payload)     

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
