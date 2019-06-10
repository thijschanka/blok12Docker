# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 12:29:33 2019

@author: thijs
"""

rule start_docker:
    shell:
        'docker-machine start'
        
rule start_app:
    shell:
        'docker-compose up'
        
rule make_db:
    shell:
        'wget: Localhost:5000/make_db'
    
rule fill_db:
    input:
        "{sample}"
    output:
        "{sample}"
    shell:
        'cp -a {sample}/. /app/data'
        'wget: Localhost:5000/filldb'