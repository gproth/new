
'''
Created on Mar 27, 2010
This module is designed to run the necessary code to spider the information from 
code.google.com and add the information to the oss_mole database.

RUN INSTRUCTIONS
Run this module from command line with the following format:
[Interpreter] GoogleCodeSpider.py [datasource_id] [Test T/F]
Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
Otherwise use 'F'.

@author: StevenNorris
'''

from GCutils import GoogleCodeUtils
import sys
import GChome
import GCupdates
import GCpeople
import GCwiki
import GCissues
import GCindividualPeople
import GCindividualIssues
import GCdownloads

#this method runs all necessary method for spidering sourceforge.net
def main(argv):
    
    #set variables
    try:
        datasource_id=argv[1]
        test=argv[2]
    except:
        print("""RUN INSTRUCTIONS
Run this module from command line with the following format:
[Interpreter] GoogleCodeSpider.py [datasource_id] [Test T/F]
Test is a string variable. Be sure to use a capital 'T' to denote test mode. 
Otherwise use 'F'.""")
        sys.exit()
    
    #Checks for test mode
    try:
        if (test=='T'):
            print("TEST MODE ACTIVATED")
            utils=GoogleCodeUtils()
        else:
            utils=GoogleCodeUtils()
    except:
        print("Please create the dbInfo.txt and the dbInfoTest.txt files. See ReadMe for formatting.")
        sys.exit()
    
    #runs the spidering
    GChome.run(utils,datasource_id)
    GCupdates.run(utils,datasource_id)
    GCpeople.run(utils,datasource_id)
    GCdownloads.run(utils,datasource_id)
    GCissues.run(utils,datasource_id)
    GCwiki.run(utils,datasource_id)
    GCindividualPeople.run(utils,datasource_id)
    GCindividualIssues.run(utils,datasource_id)

main(sys.argv)
