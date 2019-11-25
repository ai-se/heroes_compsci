# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 16:54:11 2018

@author: suvod
"""

from __future__ import division
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import networkx as nx
import os
from main.utils import utils as utils
import platform
from os.path import dirname as up

class create_social_inteaction_graph(object):
    
    def __init__(self,project_name):
        self.project_name = project_name
        self.read_data()
        
    def read_data(self):
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.comments_details_df = pd.read_pickle(up(os.getcwd()) + '/data/' + self.project_name+ '_issue_comment.pkl')
            #print(self.comments_details_df)
            self.issue_details_df = pd.read_pickle(up(os.getcwd()) + '/data/' + self.project_name+ '_issue.pkl')
            self.user_map = pd.read_pickle(up(os.getcwd())+ '/data/' + self.project_name+ '_user.pkl')
        else:
            self.comments_details_df = pd.read_pickle(up(os.getcwd()) + '\\data\\' + self.project_name+ '_issue_comment.pkl')
            self.issue_details_df = pd.read_pickle(up(os.getcwd()) + '\\data\\' + self.project_name+ '_issue.pkl')
            self.user_map = pd.read_pickle(up(os.getcwd()) + '\\data\\' + self.project_name+ '_user.pkl')
        self.comments_details_df.drop(['commenter_type'], inplace=True, axis = 1)
        self.issue_details_df.drop(['author_type','Desc','title','commits'], inplace=True, axis = 1)
        #TODO: The Issue_id and Issue_number columns are different and are not getting merged in concat
        self.comm_details_df = pd.concat([self.comments_details_df,self.issue_details_df])
        print("Combined column names for comm_details")
        print(list(self.comm_details_df.columns))
        
    def create_adjacency_matrix(self):
        uniq_users = self.comm_details_df.user_logon.unique()
        connection_matrix = np.ndarray(shape=(len(uniq_users),len(uniq_users)))
        # TODO O(n^2)... Can we use adjancency list instead for better performance?
        connection_matrix = np.zeros((len(uniq_users),len(uniq_users)), dtype=np.int)
        self.user_dict = {}
        rev_user_dict = {}
        user_id = 0
        for i in range(len(uniq_users)):
            self.user_dict[uniq_users[i]] = user_id
            rev_user_dict[user_id] = uniq_users[i]
            user_id += 1

        issue_to_user_counts = {}
        for index,row in comm_details.iterrows():
            user_count_dict = issue_to_user_counts.get(row['Issue_id'], dict())
            count = user_count_dict.get(row['user_logon'], 0)
            user_count_dict[row['user_logon']] = count+1
            issue_to_user_counts[row['Issue_id']] = user_count_dict

        for issue_id in issue_to_user_counts:
            user_count_dict = issue_to_user_counts[issue_id]
            if (len(user_count_dict) > 1):
                for user1 in user_count_dict:
                    user1_count = user_count_dict[user1]
                    for user2 in user_count_dict:
                        if (user2 != user1):
                            connection_matrix[user1][user2] += user1_count
        return connection_matrix
                    
    
    def get_user_node_degree(self):
        graph_util = utils.utils()
        print("starting social graph get_node_degree creation of adjacency matrix")
        degree,G = graph_util.create_graph(self.create_adjacency_matrix())
        print("done social graph get_node_degree creation of adjacency matrix")
        user_degree = {}
        user_mapping = self.user_map.values.tolist()
        for i in range(len(user_mapping)):
            logon  = user_mapping[i][1]
            user_name = user_mapping[i][0]
            user_id = self.user_dict[logon]
            if user_id not in degree.keys():
                continue
            user_degree[user_name] = degree[user_id]
        print('Done with social graph')
        return user_degree
        
