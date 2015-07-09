'''
Created on Mar 27, 2010
This module does the spidering for the code.google.com project wiki pages.
@author: StevenNorris
'''

BASE_LINK="http://code.google.com/p/"

import sys
import time
import traceback

def run(utils,datasource_id):
    print("\nGathering wiki pages.")
    
    #runs jobs
    job=utils.get_job(datasource_id,"gather_wiki")
    if(utils.error):
        sys.exit()
    while(job!=None):
        time.sleep(3)
        try:
            unixname=job[0]
            print("Gathering for "+unixname)
            
            #gets home page
            wiki=utils.get_page(BASE_LINK+unixname+"/w/list")
            
            #inserts home page
            if(wiki):
                insert="""UPDATE gc_project_indexes SET wikihtml=%s, last_modified=NOW() WHERE unixname=%s AND datasource_id=%s"""
                utils.db_insert(insert,wiki,unixname,datasource_id)
                utils.change_status('gather_people_specific','gather_wiki',datasource_id,unixname)
                
                #get new job
                job=utils.get_job(datasource_id,'gather_wiki')
                if(utils.error):
                    sys.exit()
            
            #if wiki page does not collect properly, post error and get new job
            else:
                print("!!!!WARNING!!!! Wiki page gathering failed for "+unixname)
                utils.post_error('gather_wiki: \nWiki page either did not exist or fail to collect.' ,datasource_id,unixname)
                job=utils.get_job(datasource_id,'gather_wiki')
                if(utils.error):
                    sys.exit()
                    
        #if process fails, post error and get new job
        except:
            print("!!!!WARNING!!! Wiki page collection failed")
            utils.post_error('gather_wiki:\n'+traceback.format_exc(),datasource_id,unixname)
            job=utils.get_job(datasource_id,'gather_wiki')
            if(utils.error):
                sys.exit()
