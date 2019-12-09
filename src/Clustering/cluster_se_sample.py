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

number_of_samples = 10

for i in range(4,number_of_samples+4):
    small_sample = small_projects.sample(20)
    medium_sample = medium_projects.sample(20)
    large_sample = large_projects.sample(19)
    sample_projects = pd.concat([small_sample, medium_sample, large_sample], axis=0)
    sample_projects.reset_index(inplace=True, drop=True)
    file_name = 'SE_projects_' + str(i) + '.csv'
    sample_projects.to_csv(file_name, index=False)
    #print(sample_projects)
