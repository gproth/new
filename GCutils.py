'''
Created on Mar 27, 2010
This module includes the necessary utilities for the Google Code spider.
@author: StevenNorris
'''

import MySQLdb
import traceback
import urllib2
import socket

class GoogleCodeUtils:
    #this gathers the initial connection to the database
    def __init__(self):
        self.db = MySQLdb.connect(host="grid6.cs.elon.edu", user="groth", passwd="Monsterhunter12", db="test", use_unicode=True, charset = "utf8")
        self.cursor = self.db.cursor()
        self.error=False
        
    '''
    This method provides the ability to gather a page
    '''
    def get_page(self,url):
        try:
            response = urllib2.urlopen(url)
            html = response.read()
            return html
        except:
            print ("The page request failed.")
    
    '''
    This method provides the ability to insert into a database
    '''
    def db_insert(self,query_string,*params):
        try:
            self.cursor.execute(query_string, params) 
        except:
            print("!!!!WARNING!!!! Insertion into "+self.database+" failed.")
            print(traceback.format_exc())
            
    '''
    This method provides the ability to get a job from the job database.
    '''
    def get_job(self, datasource_id, status):
        lock = '''LOCK TABLE gc_jobs READ, gc_jobs AS t WRITE'''
        select = '''SELECT unixname
            FROM gc_jobs AS t
            WHERE status = %s
            AND datasource_id = %s 
            ORDER BY unixname
            LIMIT 1'''
        update='''UPDATE gc_jobs AS t SET status='In_Progress', last_modified=NOW()
        WHERE datasource_id=%s
        AND unixname=%s
        '''
        unlock = '''UNLOCK TABLES'''
        try:
            self.cursor.execute(lock)
            self.cursor.execute(select, (status,datasource_id))
            result = self.cursor.fetchone()
            self.cursor.execute(update,(datasource_id, result[0]))
            self.cursor.execute(unlock)
            return result
        except:
            print ("Finding job failed.")
            self.cursor.execute(unlock)     
            
    #this method allows for status changes
    def change_status(self,status,previous,datasource_id,unixname):
        update='''UPDATE gc_jobs 
        SET status=%s, last_modified=NOW(), previous_stage=%s, modified_by=%s
        WHERE datasource_id=%s 
        AND unixname=%s
        '''
        try:
            self.cursor.execute(update,(status,previous,socket.gethostname(),datasource_id,unixname))
        except:
            print('!!!!WARNING!!!! Status '+status+' did not update correctly for '+unixname+' with id '+datasource_id+'.')
            print(traceback.format_exc())
            self.error=True
   
    #this method allows for error posting 
    def post_error(self,message,datasource_id,unixname):
        update='''UPDATE gc_jobs 
        SET error_msg=%s, status='error', last_modified=NOW(), modified_by=%s
        WHERE datasource_id=%s
        AND unixname=%s'''
        try:
            self.cursor.execute(update,(message,socket.gethostname(),datasource_id,unixname))
        except:
            print('!!!!WARNING!!!! Error '+message+'could not be posted for'+unixname+' at '+datasource_id+'.')
            self.error=True
            
    #Gathers the projects list from projects_list
    def get_projects(self,datasource_id):
        try:
            select="SELECT proj_name FROM gc_projects WHERE datasource_id=%s"
            self.cursor.execute(select,(datasource_id))
            projects_list=self.cursor.fetchall()
            return projects_list
        except:
            print("!!!!WARNING!!! Collecting projects list failed.")
    
    #Gathers the homepage for a specific project
    def get_home(self,datasource_id,unixname):
        try:
            select='''SELECT homehtml FROM gc_project_indexes WHERE datasource_id=%s AND unixname=%s'''
            self.cursor.execute(select,(datasource_id,unixname))
            home=self.cursor.fetchone()
            return home
        except:
            print("!!!!WARNING!!!! Collecting home page failed.")
            print(traceback.format_exc())
            
    #Gathers the issuespage for a specific project
    def get_issues(self,datasource_id,unixname):
        try:
            select='''SELECT issueshtml FROM gc_project_indexes WHERE datasource_id=%s AND unixname=%s'''
            self.cursor.execute(select,(datasource_id,unixname))
            home=self.cursor.fetchone()
            return home
        except:
            print("!!!!WARNING!!!! Collecting issues page failed.")
            print(traceback.format_exc())
            
    #Gathers the issues ids for a specific project
    def get_issue_ids(self,unixname):
        try:
            select='''SELECT issue_id FROM gc_issues_indexes WHERE unixname=%s'''
            self.cursor.execute(select,(unixname))
            idsRaw=self.cursor.fetchall()
            ids=[]
            for id in idsRaw:
                ids.append(id[0])
            return ids
        except:
            print("!!!!WARNING!!!! Collecting issue ids failed.")
            print(traceback.format_exc())
    
    '''
    This method provides the ability to get a clean up job from the job database.
    '''
    def get_cleanup_job(self, datasource_id, previousStage):
        lock = '''LOCK TABLE gc_jobs READ, gc_jobs AS t WRITE'''
        select = '''SELECT unixname
            FROM gc_jobs AS t
            WHERE status = 'In_Progress'
            AND datasource_id = %s
            AND previous_stage = %s
            ORDER BY unixname
            LIMIT 1'''
        update='''UPDATE gc_jobs AS t SET status='Clean_Up', last_modified=NOW()
        WHERE datasource_id=%s
        AND unixname=%s
        '''
        unlock = '''UNLOCK TABLES'''
        try:
            self.cursor.execute(lock)
            self.cursor.execute(select, (datasource_id,previousStage))
            result = self.cursor.fetchone()
            self.cursor.execute(update,(datasource_id, result[0]))
            self.cursor.execute(unlock)
            return result
        except:
            print ("Finding job failed.")
            self.cursor.execute(unlock)
            
    #This method allows for the deletion of a project from the gc_project_indexes
    def delete_home(self,unixname,datasource_id):
        try:
            update="""DELETE FROM gc_project_indexes WHERE unixname=%s AND datasource_id=%s"""
            self.cursor.execute(update,(unixname,datasource_id))
        except:
            print("!!!!WARNING!!!! Deletion of home failed.")
            print (traceback.format_exc())
            
    #This method allows for the deletion of a updates page for a project from the gc_project_indexes
    def delete_updates(self,unixname,datasource_id):
        try:
            update="""UPDATE gc_project_indexes SET updateshtml=NULL WHERE unixname=%s AND datasource_id=%s"""
            self.cursor.execute(update,(unixname,datasource_id))
        except:
            print("!!!!WARNING!!!! Deletion of updates page failed.")
            print (traceback.format_exc()) 
            
    #This method allows for the deletion of a people page for a project from the gc_project_indexes
    def delete_people(self,unixname,datasource_id):
        try:
            update="""UPDATE gc_project_indexes SET peoplehtml=NULL WHERE unixname=%s AND datasource_id=%s"""
            self.cursor.execute(update,(unixname,datasource_id))
        except:
            print("!!!!WARNING!!!! Deletion of people page failed.")
            print (traceback.format_exc()) 
        
    #This method allows for the deletion of a downloads page for a project from the gc_project_indexes
    def delete_downloads(self,unixname,datasource_id):
        try:
            update="""UPDATE gc_project_indexes SET downloadshtml=NULL WHERE unixname=%s AND datasource_id=%s"""
            self.cursor.execute(update,(unixname,datasource_id))
        except:
            print("!!!!WARNING!!!! Deletion of downloads page failed.")
            print (traceback.format_exc())

    #This method allows for the deletion of a issues page for a project from the gc_project_indexes
    def delete_issues(self,unixname,datasource_id):
        try:
            update="""UPDATE gc_project_indexes SET issueshtml=NULL WHERE unixname=%s AND datasource_id=%s"""
            self.cursor.execute(update,(unixname,datasource_id))
        except:
            print("!!!!WARNING!!!! Deletion of issues page failed.")
            print (traceback.format_exc()) 
            
    #This method allows for the deletion of a wiki page for a project from the gc_project_indexes
    def delete_wiki(self,unixname,datasource_id):
        try:
            update="""UPDATE gc_project_indexes SET wikihtml=NULL WHERE unixname=%s AND datasource_id=%s"""
            self.cursor.execute(update,(unixname,datasource_id))
        except:
            print("!!!!WARNING!!!! Deletion of wiki page failed.")
            print (traceback.format_exc())  
