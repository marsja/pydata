# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 12:11:58 2014

@author: Erik Marsja, erik at marsja dot se, (http://www.marsja.se)

Written to get (Umea) population statistics from opendata.opennorth.se...
"""
import pandas as pd
import urllib2
from xml.dom import minidom

# Descriptive statistics functions
def calc_mean(y):
    """Compute mean
    y = a sequence of numbers to be calculated,
    returns the mean in float    
    """
    return float(sum(y))/len(y)

def read_csv(f):
    """Read csv from url and return pandas data frame"""
    dat = pd.read_csv(f)
    # Translating the column names from swedish to english
    dat.columns = ['Country_born', 'Country_born_code', 'Gender',
                   'County_Born', 'Keycode', 'Age_code']
    return dat


def countoc(clist):
    """Simply counting unique words in a list
    clist is the list of word to be counted"""
    ncounter = {}
    for item in clist:
        if item in ncounter:
            ncounter[item] += 1
        else:
            ncounter[item] = 1
    return ncounter


def get_text(element):
    """Function for getting the text betweens <key> in xml"""
    return " ".join(t.nodeValue for t in element[0].childNodes
                    if t.nodeType == t.TEXT_NODE)
                        

def split_text(idx, string):
    """Split string and get first, and second part"""
    index = string.find(idx)
    part1 = string[0:index+1]
    part2 = string[index+1:len(string)]
    return part1, part2


def get_data(dat, xurl):
    """Get data from xml"""
    xmldoc = minidom.parse(xurl)
    contlist = xmldoc.getElementsByTagName("dcat:distribution")
    urllist = []
    for element in contlist:
        keys = element.getElementsByTagName('dct:title')
        txt = get_text(keys)
        if len(txt) > 12:
            txt = get_text(keys)
            part1, part2 = split_text('/', txt)
            if part2 == dat:
                urllist.append(part1+part2)
    return urllist


# Search for data files in the xml file:
site = 'http://opendata.opennorth.se'

# Seperating site and xml to be able load a xml file for outher data sets
xml = '/dataset/5235e4f7-162f-4c20-a015-eafa64091193.rdf'
url = urllib2.urlopen(site + xml)

# Data files for population statistics for Umea municipality;
datafiles = get_data('Befolkningsstatistik.csv', url)
# Date of population statistics + creating list of (pandas) data frames
dataurl = 'https://openumea-storage.s3.amazonaws.com/'

# Getting the data files and the dates for them in two lists
dates, dataframes = [], []
for i in range(len(datafiles)):
    date = split_text('T', datafiles[i])
    dates.append(date[0][:-1])
    dataframe = read_csv(dataurl+datafiles[i])
    dataframes.append(dataframe)

