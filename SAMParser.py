################################################################################
# SAMParser.py — Extract Transcript-Level Read Counts
# Raghavan et al., bioRxiv 2025 — https://doi.org/10.1101/2025.02.27.640173
#
# Author: Adhithi R. Raghavan
# Created: 2023
#
# Description:
# This script parses GTF and BAM files to extract transcript-level read counts
# for isoforms with suffix `.1`. It is intended for quantifying reads mapping
# to specific annotated transcripts in yeast.
#
# Dependencies:
# - pysam
# - HTSeq
#
# Usage:
# Import the function `getTranscriptcounts()` into another script or notebook:
#
#     from SAMParser import getTranscriptcounts
#     getTranscriptcounts(gtffile='genes.gtf', bamfile='sample.bam')
#
# Note:
# Designed for yeast transcript quantification from aligned BAM files.
################################################################################




def getTranscriptcounts(gtffile,bamfile, outputfile = "counts.txt" ):
    """
    This function is used to obtain Transcript counts for protein coding genes. 
    It accounts only for transcript 1; and not other splicing variants.
    
    Inputs required to run the function:
    gtffile: Please provide path to gtf file
    bamfile: Please provide path to bam file
    output file: Default output for this function is counts.txt file; 
    if you need to change - please provide output path. """
    
    #####----IMPORTING REQUIRED MODULES-------------###############
    ##Reading the bam file with pysam 
    #Importing packages:
    print("Importing required modules...")
    import pandas as pd
    import pysam

    #####----READING THE TWO FILES-------------###############
    ##Reading the bam file with pysam 
    #Saving it with a variable name
    print("Reading bam file...")
    bam_samplefile = pysam.AlignmentFile(bamfile, "r" )
    
    
    #Viewing the gtf file using pandas 
    #It is a tab separated file so using that as the delimiter and keeping header as none 
    #Saving with a variable name
    print("Reading gtf file")
    df = pd.read_csv(gtffile,sep='\t',header= None)
    
    #####----CALCULATING TRANSCRIPT COUNTS-------------###############
    print("Calculating Transcript counts for genes...")
    
    #Making empty pandas data frame - so that it can be populated in the for loop below
    my_dict = {}
    count = []
    
    #Iterating over the range of gtf file(stored as df)
    #For each row in df
    
    for i in range(len(df)):

    #I am only interested in the gtf rows with exons, 
    #so saying for each row and 2nd column - if it has the word exon then do the below
        if df.iloc[i,2] == "exon" :
            #Also the gtf file has data for ChrM and ChrC - Manny said to iterate only for Chr 1-5 
            #So asking it to check chromosome name, and if it is not ChrM or ChrC, then to do the stuff below
            if (df.iloc[i,0] != "ChrM"):
                if (df.iloc[i,0] != "ChrC"):

                    #Then since I am interested only in transcript 1(ie Transcript ID =.1) 
                    #I am asking it for every row i - to split column 8 (which has Transcript ID and genename)
                    #First spliting by ; and then retriving the 0th element 
                    #Further spliting that by . and retriving the 1st element
                    #That contains 1" or 2", etc. - and I want only the 1/2/etc. not the " - so again getting the 0th element
                    #Wrapping all this in an if statement and saying if that value is 1 - which stands for the first transcript (.1)
                    #Then do the stuff below
                    if (((df.iloc[i,8].split(";")[0]).split(".")[1])[0]) == "1":

                    #Then for those rows, I want to get the counts from bam file
                    #For each row, use the chromosome name from the gtf file as the contig. The chr name is column 0 (python is 0 based)
                    #Similary for each row, use the start from the gtf file - start is in column 3
                    #Similary for each row, use the stop from the gtf file - start is in column 3
                        count =  bam_samplefile.count(contig =df.iloc[i,0], start = df.iloc[i,3] , stop= df.iloc[i,4])


               #For same row (i), I also am appending the Genename - which is stored in the last column; to the pandas dataframe under the column Genename
               #Since the last column has a bunch of other stuff, I am spliting first by ; and retriving the 1st element
               #Then again splitting the above by space and picking the 2nd element. Which is the gene name    
                        Genename = ((df.iloc[i,8].split(";")[1]).split(" ")[2]).strip()

                #Putting it in a dictionary called my_dict:
                #With genename as key and count as value
                #With if statement saying if Genename is present as key already - then add this value of count and sum it (basically like append)
                        if Genename in my_dict:
                            my_dict[Genename] += count 
                 #If genename is present, then just put in the count value       
                        else:
                            my_dict[Genename]= count
                                
    print("Finished calculating transcript counts for protein coding genes (With Transcript .1).")
    print("Creating the output file...")
    
    #Saving the output as a txt file- opening and writing in it                        
    file = open(outputfile,"w")

    #Saying for key and values in the dictionary:
    for key, value in my_dict.items(): 
        #Write key and value - seperated by a tab; and putting "\n" so the next entry can begin in new line.
        file.write('%s\t%s\n' % (key,value))

    #Closing the output file
    file.close()
    print("Output file with transcript counts has been created successfully!")



    
    
    