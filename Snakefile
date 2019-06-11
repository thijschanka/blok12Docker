# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:53:10 2019

@author: thijs
"""

onstart:
    shell('curl Localhost:5000/filldb')
    
rule querry_db:
    input:
        "{sample}.txt"
    output:
        "{sample}_output.json"
    run:
        shell('cp {input} ./app/data/querry')
        shell("""curl http://Localhost:5000/getresults -X POST -d '{{"bestand":"{input}"}}' -H 'Content-type:application/json' > {output}""")
