#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd

if platform.system() == 'Darwin' or platform.system() == 'Linux':
    data_path = os.getcwd() + '/MolSSI Projects DB - top_projects.csv'
    print(os.getcwd())
else:
    data_path = os.getcwd() + '\\MolSSI Projects DB - top_projects.csv'

project_list = pd.read_csv(data_path)
project_list['access_token'] = ['bcddf7453cb063663c3a3fab081ff0e747b2758b']*project_list.shape[0]
project_list['repo_owner'] = [None]*project_list.shape[0]
project_list['repo_name'] = [None]*project_list.shape[0]
project_list['source_type'] = ['github_repo']*project_list.shape[0]
project_list['git_url'] = [None]*project_list.shape[0]
project_list['api_base_url'] = ['http://api.github.com']*project_list.shape[0]
project_list['num_dev'] = project_list['Developers']

for index,row in project_list.iterrows():
    git_link = str(row['Project Github Link'])
    if (git_link.lower().find('github') != -1):
        tokens = git_link.split('/')
        repo_name = tokens[-1]
        repo_owner = tokens[-2]
        git_url = git_link.replace('https', 'git') + '.git'
        project_list.at[index, 'repo_owner'] = repo_owner
        project_list.at[index, 'repo_name'] = repo_name
        project_list.at[index, 'git_url'] = git_url
    else:
        project_list.at[index, 'repo_owner'] = '?'
        project_list.at[index, 'repo_name'] = '?'
        project_list.at[index, 'git_url'] = '?'
        project_list.at[index, 'source_type'] = '?'

removeAttributes = ['Language', 'Main Link', 'Source', 'Type', 'Testing', 'Active', 'Email', 'Name', 'Timezones', 'Opened Issues', 'Active years', 'Developers', 'Commits #', 'Closed Issues', 'Releases']
#extraAttributesToBeKept = ['Project Name', 'Project Github Link', 'Sanity_passed']


project_list = project_list.drop(removeAttributes, axis=1)
project_list = project_list[project_list['Sanity_passed'].map(lambda x: (str(x) == 'yes' or str(x) == 'Yes'))]
project_list = project_list.drop(['Sanity_passed'], axis=1)
print(project_list)

project_list.to_csv('MolSSI_cleaned_input.csv', index=False)
