# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:31:39 2018

@author: soren
"""

### PMID - Abstracts - Human Aging Pheome terms with Snowmed Extension ###

### Aging feature found -> Pmid with abstracts ###

## Import packages ##

import os
import re

## Subdirectories ##

Sub_in = "Term lists"
Sub_in2 = "PMID with Abstracts"

Sub_out = "Hallmarks of Aging analysis"

try:
    os.mkdir(Sub_out)
except Exception:
    pass

## Files ##

File1 = "Final_list_105_terms_with_synonyms.txt"
File2 = "pmid_abstract.txt"
File3 = "Hallmark_features_found_in_Abstracts.txt"

File_out = "105_terms_found_in_Hallmark_Abstracts.txt"

## Variables ##

feature_list = {}
PMID_Abstract = {}
PMID_Found_feature = {}
Hallmark_pmid_list = []

#For progress
"""
PMID_file_length = 0
#Get number of pmids
with open(os.path.join(Sub_in2,File2), "r",encoding="utf-8") as pmid_file:
    for line in pmid_file:
        PMID_file_length += 1
pmid_file.close
"""
File_line_counter = 0
percentage = 0

## Load list files ##

with open(os.path.join(Sub_in,File1), "r") as feature_file:
    for line in feature_file:
        line = line.strip().split(';')
        feature_list[line[0]] = line
feature_file.close

with open(os.path.join(Sub_out,File3), "r") as pmid_list_file:
    next(pmid_list_file)
    for line in pmid_list_file:
        line = line.strip().split(";")
        Hallmark_pmid_list.append(line[0])
pmid_list_file.close

#For progress

PMID_file_length = 0
#Get number of pmids
with open(os.path.join(Sub_in2,File2), "r",encoding="utf-8") as pmid_file:
    for line in pmid_file:
        PMID_file_length += 1
pmid_file.close

File_line_counter = 0
percentage = 0

#To handle the 22gb large file (pmid with abstract) the file is read and handled on the go.
with open(os.path.join(Sub_in2,File2), "r",encoding="utf-8") as pmid_file:
    i = 0
    for line in pmid_file:
        line = line.strip().split(';')
        #Printing progress
        File_line_counter += 1
        if File_line_counter % int(PMID_file_length/100) == 0:
            percentage += 1
            print("Progress: {} / 100 %".format(percentage))
        ##Trying to to find aging terms in abstracts
        #only go through abstracts with hallmark terms in them.
        if i >= len(Hallmark_pmid_list):
            break
        if line[0] != Hallmark_pmid_list[i]:
            continue
        if i < len(Hallmark_pmid_list):
            i += 1
        #Reset variables
        Found_features = [0]*len(feature_list)
        Counter = 0
        
        #Run through features
        for feature in feature_list:
            for features in feature_list[feature]:
                #check if ";" is incorporated in an abstract and handle if present, else search abstracts for features
                if len(line) > 2:
                    for abstract_piece in line[1:]:
                        if features.lower() in abstract_piece.lower():
                            counts = len(re.findall(r'(?=\b{}\b)'.format(features.lower()), line[1].lower()))
                            Found_features[Counter] += counts
                else: 
                    if features.lower() in line[1].lower():
                        counts = len(re.findall(r'(?=\b{}\b)'.format(features.lower()), line[1].lower()))
                        Found_features[Counter] += counts
            #Counter is for saving the count in right order
            Counter += 1
            #Check if any feature is found and skips if none, then converts to 1 or 0 (categorial values)
            if sum(Found_features) > 0:
                Found_features = [1 if x > 0 else 0 for x in Found_features]
                PMID_Found_feature[line[0]] = Found_features
    print("100 / 100 %".format(percentage))
pmid_file.close

print("Search done!")

#Writes the Clinical feature found to a file: Header with mimnumber + features (from feature list)
with open(os.path.join(Sub_out,File_out), "w+") as PMID_Found_feature_file:
    PMID_Found_feature_file.write("PMID;{}\n".format(';'.join(map(str, feature_list.keys())))) 
    for key in PMID_Found_feature:
            PMID_Found_feature_file.write("{};{}\n".format(key, ';'.join(map(str, PMID_Found_feature[key]))))
PMID_Found_feature_file.close

print("File saved.")

print("Done!")
