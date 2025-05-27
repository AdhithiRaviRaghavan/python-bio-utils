################################################################################
# homology.py — Identify Reciprocal Best Homologs Using BLAST XML Output
# Author: Adhithi R. Raghavan
# Created: 2023
#
# Description:
# This script defines two functions:
# - getBestHomolog(xmlfilepath): extracts best homologs for each query sequence
# - getReciprocalBestHomology(xml1, xml2, output): finds reciprocal best hits (RBHs)
#
# Usage:
# Import these functions in another script or run as a standalone module
# with appropriate XML BLAST outputs from two species.
################################################################################

#Making function to obtain best homolog.
def getBestHomolog(xmlfilepath1):
    """This function reads an the output of Blast search (Xml file)
    and returns the best Homolog for each protein, if it exists.
    
    Input required: Path to blast output as an Xml file. """
    
    #Importing modules
    from Bio.Blast import NCBIXML
    import pandas as pd

    #Creating empty dictionary so it can be populated in the for loop below
    my_dict = {}
    
    #Parsing the XML file - used parse versus read because it has multiple records - ie one for each protein.
    record = NCBIXML.parse(open(xmlfilepath1))
    
    
    #Making a for loop to go over every record 
    for eachrecord in record:
        
        #Because every record may not have an alignment, so saying if alignment exists then do the stuff below.
        if eachrecord.alignments:
            
            #Get TargetID title
            TargetID  = (eachrecord.alignments[0].title)
            
            #Get query ID (ie is protein being searched for, for homology)
            QueryID  = (eachrecord.query)
            
            #Saving it as a dictionary with QueryID as key and TargetID as values.
            my_dict[QueryID]= TargetID
            
    
    
    #Returning the dictionary outside the loop.
    return(my_dict)


def getReciprocalBestHomology(xmlfilepath1, xmlfilepath2, outputpath = "homologs.txt"):
    
    """This function gives proteins with the best reciprocal homology in the two species.
    Input required: 
    xmlfilepath1: Path to blast output as an Xml file for Species 1.
    xmlfilepath2: Path to blast output as an Xml file for Species 2.
    outputpath = default is homologs.txt
    
    """
    #Importing modules
    from Bio.Blast import NCBIXML
    import pandas as pd


    #Using the earlier function getBestHomolog to obtain best homolog for each species
    print("Obtaining best identified homolog for each protein for Species 1 ...")
    output_of_Drosophila = getBestHomolog("drosophila_celegans.xml")
    print("Best homolog for each protein (if it exists) in Species 1 has been identified! ")  
    print("...............................................................................")
    
    print("Obtaining best identified homolog for each protein for Species 2 ...")
    output_of_Celegans = getBestHomolog("celegans_drosophila.xml")
    print("Best homolog for each protein (if it exists) in Species 2 has been identified! ")  
    print("...............................................................................")
    
    #Find reciprocal best homology between the two species:
    print("Obtaining reciprocal best homology between Species 1 and 2...")
    
    #Making a for loop that first iterates over every key and value in output_of_Drosophila dictionary made earlier
    for eachkey_Drosophilia, eachvalue_Drosophilia in output_of_Drosophila.items():
        
        #Making a second for loop that first iterates over every key and value in output_of_Celegans dictionary made earlier
        #So basically eachkey_Drosophilia and eachvalue_Drosophilia will be checked with all keys and values in C.elegans dictionary.
        for eachkey_Celegans, eachvalue_Celegans in output_of_Celegans.items():
            
            #For matching reciprocal homology
            #searching if key of Drosophilia (which was the Query ID) - matches values in C.elgans(TargetID)
            if eachkey_Drosophilia == eachvalue_Celegans:
                
                #And also nesting the otherway 
                #if key of C.elegans (which was the Query ID) - matches values in Drosophilia(TargetID)
                if eachkey_Celegans == eachvalue_Drosophilia:
                    
                    #If it does: Then asking it to open and append values to outputfile - whatever user defined/default
                    f = open(outputpath, "a") 
                    
                    #Append eachkey_Drosophilia
                    f.write(eachkey_Drosophilia)
                    
                    #Adding a tab to separate
                    f.write("\t")
                    
                    #Append eachkey_Drosophilia
                    f.write(eachvalue_Drosophilia)
                    
                    #So that every reciprocal best homology is on a new line.
                    f.write("\n") 
                    
                     #Close the file
                    f.close()
    print("Reciprocal best homology between Species 1 and 2 has been obtained, and can be found in the output file! ")


                                   