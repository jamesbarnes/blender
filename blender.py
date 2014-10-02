#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import csv
import unicodecsv
import sys

def cleanup(rawhtml):
    html_doc = rawhtml
    soup = BeautifulSoup(html_doc)
    bod = soup.find('body')
    # for anchor links 
    for a in bod.find_all('a'):
        try:
            r = "[[LINK: " + bod.find('a')['href'] + "||" + bod.find('a').contents[0].get_text() + "]]"
            bod.a.replace_with(r)
        except:
            r = "[[LINK: " + bod.find('a')['href'] + "||" + bod.find('a').contents[0] + "]]"
            bod.a.replace_with(r)
    #for image tags
    for i in bod.find_all('img'):
        try:
            r = "[[IMAGE: " + bod.find('img').attrs['src'] + "||" + bod.find('img').attrs['alt'] + "]]"
            bod.find('img').replace_with(r)
        except:
            r = "[[IMAGE: " + bod.find('img').attrs['src'] + "]]"
            bod.find('img').replace_with(r)

    for u in bod.find_all('ul'):
        try:
            r = bod.find('ul').contents.get_text()
            bod.find('ul').replace_with(r)
        except:
            pass

    for l in bod.find_all('li'):
        try:
            r = "\n - "+bod.find('li').get_text()+"\n"
            bod.find('li').replace_with(r)
        except:
            pass
            
    for p in bod.find_all('p'):
        bod.find('p').replace_with("\n"+bod.find('p').get_text()+"\n")

    for d in bod.find_all('div'):
        try:
            bod.find('div').replace_with(bod.find('div').get_text()+"\n")
        except:
            pass

    return(soup.find('body').get_text())

f = open(sys.argv[1], 'rU')
fa = []
try:
    reader = csv.reader(f)
    for row in reader:
        fa.append(row)        
finally:
    f.close()

w = open('output.csv', 'wt')
try:
    writer = unicodecsv.writer(w)
    for row in fa:
        writer.writerow((row[0],row[1],cleanup(row[0])))
finally:
    w.close()