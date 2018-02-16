#!/usr/bin/env python
""" kalaniroxrubberspheres.py  reads a list of words and then figures out the longest wordpath
    assumptions: standard english characters, python2. """

__author__ = "Kalani Thompson"
__copyright__ = ""
__credits__ = ["Kalani Thompson"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Kalani Thompson"
__email__ = "thompson.kalani@gmail.com"
__status__ = "Development"

import re
import sys

debug=False

def debugLog(s):
    if(debug):
        sys.stderr.write(s)
    return

def progressLog(p):
    if(not debug):
        sys.stderr.write("\rCurrent path length:" + str(p))
    return

# this function takes a pair of lists and assumes the last word in the path 
def findMatches(thePath,theList):
    
    theWord = thePath[-1]                                                   # slurp up the last element
    possibleMatches = []
    
    for c in range(0,len(theWord)):                                         # iterate over every character in the word, to create a fuzzy-match regex for each character position
                                                                            # regex will match an ADDED character, a REPLACED character or a MISSING character
                                                                            # ^W(?:(?:[^O])?|(?:O.))RD$ will match WRD, WARD or WOORD but not WORD
        debugLog("\n^" + theWord[:c] + "(?:(?:[^" + theWord[c] + "])?|(?:" + theWord[c] + ".))" + theWord[c+1:] + "$\n")
        theRegEx = re.compile("^" + theWord[:c] + "(?:(?:[^" + theWord[c] + "])?|(?:" + theWord[c] + ".))" + theWord[c+1:] + "$")
        for w in theList:                                                   # step through the list to find matches
            if(theRegEx.match(w) and w not in thePath):
                possibleMatches.append(w)
                  
    return possibleMatches
    
    
# This function will find matches in the list for a path, and iterate over them to find and return the longest
def followPath(thePath,theList):
    progressLog(len(thePath))
    debugLog("FOLLOWING " + "".join(thePath) + "...\n")
    nodeList = findMatches(thePath,theList)
    pathMatches = [];
    longestPath = thePath;
    
    if(len(nodeList)):
        for n in nodeList:
            debugLog("Processing " + thePath[-1] + " " + n + "\n")
            thisPath = thePath[:]
            thisPath.append(n)
            for fullPath in followPath(thisPath,theList):
                if(len(fullPath) > len(longestPath)):
                    debugLog("This path is bigger\n")
                    longestPath = fullPath
                    del pathMatches[:]
                    pathMatches.append(fullPath)
                elif(len(fullPath) == len(longestPath)):
                    debugLog("This path is the same len\n")
                    pathMatches.append(fullPath)
    else:
        pathMatches.append(thePath)
    return(pathMatches)
    

# main program code starts here

input_filename = ""
input_word = ""

# see if we've input parameters -- otherwise give us a nastygram
if(len(sys.argv) > 2):
    input_filename = sys.argv[1]
    input_word = sys.argv[2]
else:
    print("Usage: kalanirocksrubberspheres.py <filename> <word>")
    print("   ex:   kalanirocksrubberspheres.py /usr/share/dict/words rubbish")
    exit()

with open(input_filename) as f:
    wordList = f.read().splitlines()                                        # read file line-by-line and cut off the \n characters


wordPath = []
wordPath.append(input_word)

for longestPath in followPath(wordPath,wordList):
    progressLog("\r")                                                       # clear the number
    print(longestPath)