# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:53:10 2019

@author: thijs
"""
#vullen van db
onstart:
    shell('curl Localhost:5000/filldb')

#instaleren van dependencies    
onstart:
    shell('pip3 install pandas')

#de database queryen
rule querry_db:
    input:
        "{sample}.txt"
    output:
        "{sample}_output.json"
    run:
        shell('cp {input} ./app/data/querry')
        shell("""curl http://Localhost:5000/getresults -X POST -d '{{"bestand":"{input}"}}' -H 'Content-type:application/json' > {output}""")

#rapportje genereren
rule get_stuff:
    input:
        "{sample}_output.json"
    output:
        "{sample}_report.HTML"
    script:
        "./make_rapport.py"


