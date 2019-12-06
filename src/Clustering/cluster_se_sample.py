#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd

#def fill_other_attributes(project_list):
#    for i in range(project_list.shape[0]):
#            try:
#                access_token = project_list.loc[i,'access_token']
#                repo_owner = project_list.loc[i,'repo_owner']
#                source_type = project_list.loc[i,'source_type']
#                git_url = project_list.loc[i,'git_url']
#                api_base_url = project_list.loc[i,'api_base_url']
#                repo_name = project_list.loc[i,'repo_name']
#                git_data = git2data.git2data(access_token,repo_owner,source_type,git_url,api_base_url,repo_name)
#                #git_data = git_commit_info.git2data(access_token,repo_owner,source_type,git_url,api_base_url,repo_name)
#                git_data.create_data()
#            except ValueError as e:
#                print("Exception occured for ",project_list.loc[i,'git_url'])
#                print(e)

if platform.system() == 'Darwin' or platform.system() == 'Linux':
    source_projects = os.getcwd() + '/hero_list.csv'
else:
    source_projects = os.getcwd() + '\\hero_list.csv'

source_projects = pd.read_csv(source_projects)

small_projects = source_projects[(source_projects['num_dev'] >= 8) & (source_projects['num_dev'] < 15)]
medium_projects = source_projects[(source_projects['num_dev'] >= 15) & (source_projects['num_dev'] < 30)]
large_projects = source_projects[source_projects['num_dev'] >= 30]

# Sampling - TODO: Do this multiple times and ways
small_sample = small_projects.sample(20)
medium_sample = medium_projects.sample(20)
large_sample = large_projects.sample(19)
sample_projects = pd.concat([small_sample, medium_sample, large_sample], axis=0)
sample_projects.reset_index(inplace=True, drop=True)
sample_projects['Developers'] = sample_projects['num_dev']
sample_projects['Commits #'] = [0]*sample_projects.shape[0]
sample_projects['Closed Issues'] = [0]*sample_projects.shape[0]
sample_projects['Releases'] = [0]*sample_projects.shape[0]
#sample_projects['active_since'] = [0]*sample_projects.shape[0]
sample_projects['Active years'] = [0]*sample_projects.shape[0]
xAttributes = ['Developers', 'Commits #', 'Closed Issues', 'Releases']
keepAttributes = ['git_url']
removeAttributes = ['repo_name', 'repo_owner', 'api_base_url', 'source_type', 'access_token', 'lang', 'heros_80', 'heros_85', 'heros_90', 'heros_95', 'num_dev']
sampe_projects = sample_projects.drop(removeAttributes, axis = 1).to_csv("SE_projects_2.csv", index=False)
print(sample_projects)
