# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 12:48:17 2019

@author: thijs
"""

import pandas as pd
import sys

def readraport(bestand):
    df = pd.read_json(bestand)
    return df

def get_table(df):
    cols = ['chr', 'pos', 'ref', 'alt', 'af']
    df = df[cols]
    x = df.to_html(classes='w3-table-all', bold_rows=True)
    return str(x)

def get_circle_cos(df):
    df = df['chr']
    x = df.value_counts()
    lijstje = []
    for i,n in enumerate(x):
        data = {'y':n, 'label':x.index[i]}
        lijstje.append(data)
    return str(lijstje)

def get_lowest(df):
    cols = ['chr', 'pos', 'ref', 'alt', 'af']
    df = df[cols]
    df = df.sort_values(by=['af'], ascending=False).head(5)
    x = df.to_html(classes='w3-table-all', bold_rows=True)
    return str(x)
    
def get_highest(df):
    cols = ['chr', 'pos', 'ref', 'alt', 'af']
    df = df[cols]
    df = df.sort_values(by=['af']).head(5)
    x = df.to_html(classes='w3-table-all', bold_rows=True)
    return str(x)

def main(file_in, file_out):
    df = readraport(file_in)
    rapport = '<HTML><BODY><link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">'
    rapport += """<script>
window.onload = function() {

var chart = new CanvasJS.Chart("chartContainer", {
	theme: "light2", // "light1", "light2", "dark1", "dark2"
	exportEnabled: true,
	animationEnabled: true,
	title: {
		text: "Chromosome distrubution"
	},
	data: [{
		type: "pie",
		startAngle: 25,
		toolTipContent: "<b>{label}</b>: {y}%",
		showInLegend: "true",
		legendText: "{label}",
		indexLabelFontSize: 16,
		indexLabel: "{label} - {y}%",
		dataPoints: """
    rapport += get_circle_cos(df)
    rapport += """}]
});
chart.render();

}
</script>
<div id="chartContainer" style="height: 370px; width: 100%;"></div>
<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script><br>Top 5 lowest alele frequencies<br>"""
    rapport += get_highest(df)
    rapport += '<br>Top 5 highest alele frequencies<br>'
    rapport += get_lowest(df)
    rapport += '<br>all potential pathogenic mutations<br>'
    rapport += get_table(df)
    rapport += "<br></BODY></HTML>"
    bestand = open(file_out, 'w+')
    bestand.write(rapport)

    

main(snakemake.input[0], snakemake.output[0])
