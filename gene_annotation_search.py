"""
gene_annotation_search.py — Command-Line Tool for Querying Gene Annotations

Author: Adhithi R. Raghavan
Date: May 2023

Description:
This script allows users to search for specific keywords in gene annotations
stored in a local SQLite database (`arabidopsis.sqlite`). Results are returned
as a formatted table using pandas.

Usage:
    python gene_annotation_search.py -q kinase

Dependencies:
    - pandas
    - sqlite3
    - argparse
"""

def keyword_search(word):
    con = sqlite3.connect("arabidopsis.sqlite") #Creating a connection with the database
    cursor = con.cursor() 
    cursor.execute("""SELECT  * FROM geneannotation WHERE annotation like '%{word}%'""".format(word=word))
   #Select *: All columns,
   #From the table  with name  geneannotation table, 
   #Where column name is annotation, 
   # Need wild card search for string or name 
   #Using % - the stuff ahead or behind the string, I don't know, but find anything with it . Can have any string of zero or more characters before or after.
    #Like - not definitive, but may have something like the string with anything behind or in front of it.
    #.format(word = word): Assign word in the {} statement
    output = cursor.fetchall() 
    df = pd.DataFrame(data = output)
    return(df)

    
#To run only on command line:

if __name__=="__main__": 
    

    #Importing required modules
    import argparse #So that arguments can be parsed
    import pandas as pd
    import sqlite3
   
    #Using arg parser
    parser = argparse.ArgumentParser()

    #This is to add flags, add as many as you want.
    #https://docs.python.org/3/library/argparse.html - Found this to be useful for information on parsing arguements.
    
    #Adding parsers as suggested in the question
    parser.add_argument("-q", "--query", help ="Please provide query argument", required = True, type = str) #flag is required so setting it to true.
    
    args = parser.parse_args()
    
    #Calling the keyword_search function that was made up above, and running it with the query(that is user inputted).
    print(keyword_search(args.query) )
        
