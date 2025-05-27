"""
gffparser.py — Extract Gene Names from GFF Files by Region

Author: Adhithi R. Raghavan  
Date: May 2023 

Description:
This script parses a GFF file to extract gene names from a specific chromosome and coordinate range.
It supports both command-line usage and output redirection to a file.

Command-line arguments:
-i / --filepath           : Path to input GFF file [Required]  
-c / --chromosomenumber   : Chromosome (e.g., Chr1, Chr2) [Required]  
-s / --startcoordinate    : Start coordinate [Required]  
-e / --endcoordinate      : End coordinate [Required]  
-o / --outputpath         : Optional path to save output

Example usage:
python gffparser.py -i example.gff -c Chr1 -s 10000 -e 50000
"""


if __name__=="__main__": 
    #To run only on command line:
    import argparse #So that arguments can be parsed
       
    parser = argparse.ArgumentParser() #Saving the argparse.ArgumentParser with a variable name so it can be used below. 

    #This is to add flags, add as many as you want.
    #https://docs.python.org/3/library/argparse.html - Found this to be useful for information on parsing arguements.
    
    #Adding parsers as suggested in the question
    parser.add_argument("-i", "--filepath", help ="Please provide path to file",
                       required = True)
    
    parser.add_argument("-c", "--chromosomenumber", 
                        help ="Please provide chromosome number, eg. Chr1, Chr2, etc", 
                        required = True)
    
    parser.add_argument("-s", "--startcoordinate",
                       help ="Please provide start coordinate of region", 
                       type = int, required = True)    
    
    parser.add_argument("-e", "--endcoordinate", 
                        help ="Please provide end coordinate of region", 
                        type = int, required = True)
    
    parser.add_argument("-o", "--outputpath", 
                        help ="Please provide path where the output should be stored", 
                       # action = 'store',
                        required = False) #Setting required to be false, because if is provided then the output will be saved, if not I want to only print the output.

    args = parser.parse_args()
    
    #Making empty variables, so that it can be populated later.
    enteries =[]
    nameofenteries =[]
    finaloutput=[]
   

    import re
    with open(args.filepath, 'r') as file:
        
        reader1 = file.readlines()
        reader = []
        
        for line in reader1:
           
           #print(line.split('\t'))
            reader2 = line.rstrip().split('\t') 
            reader.append(reader2)
        #print(reader)   
            
        for row in reader:
                if row[0] == args.chromosomenumber: 
                    #print(row) #Column 0 - is chromosome number
                    if row[2] == 'gene': #Column 2 - is gene. Setting this as a set feature with gene. 
                        if int(row[3]) >= args.startcoordinate: #Values greater and equal to the provided start
                            if int(row[4]) <= args.endcoordinate:#Values lesser and equal to the provided stop
                                #print(row)
                                enteries =row[8].split(';') #Now the last column has names and other info. Split by ;
                            
                            #The third column of that has only name, split that by =, that is name=genename. Need only something.
                                nameofenteries = enteries[2].split('=') 
    
                            #Getting the genename, which is the first column.
                                finaloutput = (nameofenteries[1]) #Save that finaloutput variable name.

                                if args.outputpath: #if argsoutput path is set, then it is telling to do this/
                                    my_output = args.outputpath #Storing outputpath as a variable name
                                
                             #opening the file/filepath, a is for append. So it will append, write "w" was overwriting values. 
                                    f = open(my_output, "a") 
                                    f.write(finaloutput)#So within the file now adding the finaloutput value
                                    f.write("\n") #So that every output is on a new line.
                                    f.close() #Close the file
                            
                                else:    #If no outputpath arguement given
                        
                                    print(finaloutput) #Then just print the finaloutput.
                            
                

                        
            
                
                
        
    
    
