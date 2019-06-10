# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:53:10 2019

@author: thijs
"""

rule start_docker:
    shell:
        'docker-machine start'
        
rule start_app:
    shell:
        'docker-compose up'
    
rule querry_db:
    input:
        "{sample}.txt"
    output:
        "{sample}_output.json"
    shell:
        'cp -a {sample}.txt /app/query'
        'wget: --post-data "file={sample}.txt" Localhost:5000/getresults'