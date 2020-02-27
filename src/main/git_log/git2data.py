# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 10:30:28 2018

@author: suvod
"""
from __future__ import division
from main.api import git_access,api_access
from main.git_log import git2repo,buggy_commit
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import re
import networkx as nx
import platform
from os.path import dirname as up
import operator
from datetime import datetime
from ratelimiter import RateLimiter

class git2data(object):
    
    def __init__(self,access_token,repo_owner,source_type,git_url,api_base_url,repo_name):
        self.repo_name = repo_name
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.data_path = up(os.getcwd()) + '/data/'
        else:
            self.data_path = up(os.getcwd()) + '\\data\\'
        self.git_client = api_access.git_api_access(access_token,repo_owner,source_type,git_url,api_base_url,repo_name)
        self.git_repo = git2repo.git2repo(git_url,repo_name)
        self.repo = self.git_repo.clone_repo()
        
    def get_api_data(self):
        self.git_issues = self.git_client.get_issues(url_type = 'issues',url_details = '')
        self.git_issue_events = self.git_client.get_events(url_type = 'issues',url_details = 'events')
        self.git_issue_comments = self.git_client.get_comments(url_type = 'issues',url_details = 'comments')
        self.user_map = self.git_client.get_users()
            
    def get_commit_data(self):
        #print("Inside get_commit_data in git2data")
        self.git_commits = self.git_repo.get_commits()
        
    def get_committed_files(self):
        #print("Inside get_commit_data in git2data")
        self.git_committed_files = self.git_repo.get_committed_files()
        return self.git_committed_files
    
        
    def create_link(self):
        issue_df = pd.DataFrame(self.git_issues, columns = ['Issue_number','user_logon','author_type','Desc','title','lables'])
        commit_df = pd.DataFrame(self.git_commits, columns=['commit_number', 'message', 'parent','buggy'])
        events_df = pd.DataFrame(self.git_issue_events, columns=['event_type', 'issue_number', 'commit_number'])
        issue_commit_temp = []
        commit_df['issues'] = pd.Series([None]*commit_df.shape[0])
        issue_df['commits'] = pd.Series([None]*issue_df.shape[0])
        #print("Phase one done")
        for i in range(commit_df.shape[0]):
            _commit_number = commit_df.loc[i,'commit_number']
            _commit_message = commit_df.loc[i,'message']
            res = re.search("#[0-9]+$", _commit_message)
            if res is not None:
                _issue_id = res.group(0)[1:]
                issue_commit_temp.append([_commit_number,np.int64(_issue_id)])
        issue_commit_list_1 = np.array(issue_commit_temp)
        links = events_df.dropna()
        links.reset_index(inplace=True)
        issue_commit_temp = []
        issue_set_1 = set(issue_commit_list_1[:,0])
        #print("Phase two done")
        for i in range(links.shape[0]):
            if links.loc[i,'commit_number'] in issue_set_1:
                continue
            else:
                issue_commit_temp.append([links.loc[i,'commit_number'],links.loc[i,'issue_number']])
        issue_commit_list_2 = np.array(issue_commit_temp)
        issue_commit_list = np.append(issue_commit_list_1,issue_commit_list_2, axis = 0)

        commit_to_issues = {}
        issue_to_commits = {}

        #print("Phase three done")
        issue_commit_df = pd.DataFrame(issue_commit_list, columns = ['commit_id','issues'])
        for index,row in issue_commit_df.iterrows():
            commit_num = row['commit_id']
            issue_id = np.int64(row['issues'])
            commit_to_issues.setdefault(commit_num, set()).add(issue_id)
            issue_to_commits.setdefault(issue_id, set()).add(commit_num)

        for index,row in issue_df.iterrows():
            issue_id = np.int64(row['Issue_number'])
            if issue_id in issue_to_commits:
                issue_df.at[index,'commits'] = issue_to_commits[issue_id]

        for index,row in commit_df.iterrows():
            commit_num = row['commit_number']
            if commit_num in commit_to_issues:
                commit_df.at[index,'issues'] = commit_to_issues[commit_num]

        issue_comments_df = pd.DataFrame(self.git_issue_comments, columns = ['Issue_id','user_logon','commenter_type'])
        committed_files_df = pd.DataFrame(self.git_committed_files, columns = ['commit_id','file_id','file_mode','file_path'])
        user_df = pd.DataFrame(self.user_map, columns = ['user_name','user_logon'])
        return issue_df,commit_df,committed_files_df,issue_comments_df,user_df
    
    def create_data(self):
        self.get_api_data()
        print("API done")
        self.get_commit_data()
        print("Commit done")
        self.get_committed_files()
        print("Committed file done")
        issue_data,commit_data,committed_file_data,issue_comment_data,user_data = self.create_link()
        print(self.data_path)
        issue_data.to_pickle(self.data_path + self.repo_name + '_issue.pkl')
        commit_data.to_pickle(self.data_path + self.repo_name + '_commit.pkl')
        committed_file_data.to_pickle(self.data_path + self.repo_name + '_committed_file.pkl')
        issue_comment_data.to_pickle(self.data_path + self.repo_name + '_issue_comment.pkl')
        user_data.to_pickle(self.data_path + self.repo_name + '_user.pkl')
        self.git_repo.repo_remove()
        print(self.repo_name,"Repo Done")

    def get_additional_data(self):
        # Commits
        self.git_commits = self.git_repo.get_commits(extra_details = True)
        commit_data = pd.DataFrame(self.git_commits, columns=['commit_number', 'message', 'parent','buggy', 'commit_time'])
        commit_data.to_pickle(self.data_path + self.repo_name + '_commit.pkl')

        # Issues
        self.git_issues = self.git_client.get_issues(url_type = 'issues',url_details = '',extra_details=True)
        issue_data = pd.DataFrame(self.git_issues, columns = ['Issue_number','user_logon','author_type','Desc','title','lables', 'state','is_issue'])
        #issue_data.drop(['user_logon', 'Desc'], axis=1, inplace=True)
        issue_data.to_pickle(self.data_path + self.repo_name + '_issue.pkl')

        #Create date
        github_repo = self.git_client.get_github_repo()
        create_date = datetime.strptime(github_repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')

        #Releases
        git_releases = self.git_client.get_releases(url_type = 'releases', url_details = '')
        release_data = pd.DataFrame(git_releases, columns = ['Release_id'])
        #release_data.to_pickle(self.data_path + self.repo_name + '_release.pkl')

        #Tags
        git_tags_count = self.git_client.get_list_count(url_type = 'tags', url_details = '')

        #Stars
        #self.git_stars = len(self.git_client.get_list_details(url_type = 'stargazers', url_details = ''))
        git_stars = github_repo['stargazers_count']

        #Forks
        #self.git_forks_count = len(self.git_client.get_list_details(url_type = 'forks', url_details = ''))
        git_forks_count = github_repo['forks_count']

        #Watchers
        #self.git_watchers_count = len(self.git_client.get_list_details(url_type = 'subscribers', url_details = ''))
        git_watchers_count = github_repo['subscribers_count']

        #Language
        #lang = self.git_client.get_languages(url_type = 'languages', url_details = '')
        #self.max_language = max(lang.items(), key = operator.itemgetter(1))[0]
        max_language = github_repo['language']

        print(self.repo_name, "Repo Done")

        return commit_data,issue_data,create_date,release_data,git_stars,git_forks_count,git_watchers_count,max_language,git_tags_count

    #@RateLimiter(max_calls = 1, period = 1)
    def get_contributors(self):
        contributors = self.git_client.get_contributors(url_type = 'contributors', url_details = '')
        return contributors

    @RateLimiter(max_calls = 1, period = 1)
    def get_user(self, user_login):
        return self.git_client.get_user(user_login)

