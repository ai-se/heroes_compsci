#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd
from main.git_log import git2data
from Clustering import cluster_attribute_collector

if platform.system() == 'Darwin' or platform.system() == 'Linux':
    data_path = os.getcwd() + '/Clustering/'
    #data_path = os.getcwd() + '/Clustering/project_list.csv'
    #print(os.getcwd())
else:
    #data_path = os.getcwd() + '\\Clustering\\project_list.csv'
    data_path = os.getcwd() + '\\Clustering\\'

number_of_samples = 10
starting_index = 4

cache = {}

for file_index in range(starting_index, number_of_samples + starting_index):
    print('Starting file_index = ' + str(file_index))
    file_name = 'SE_projects_' + str(file_index) + '.csv'
    project_list = pd.read_csv(data_path + file_name)

    output_list = []
    project_name_available = True if ('Project Name' in project_list.columns) else False

    for i in range(project_list.shape[0]):
            try:
                print("I am here at " + str(i))
                access_token = project_list.loc[i,'access_token']
                repo_owner = project_list.loc[i,'repo_owner']
                source_type = project_list.loc[i,'source_type']
                repo_name = project_list.loc[i,'repo_name']
                developers = project_list.loc[i, 'num_dev']
                git_url = project_list.loc[i,'git_url']
                api_base_url = project_list.loc[i,'api_base_url']
                project_name = repo_name if project_name_available == False else project_list.loc[i, 'Project Name']
                if (git_url not in cache):
                    if (source_type.lower() == 'github_repo'):
                        git_data = git2data.git2data(access_token,repo_owner,source_type,git_url,api_base_url,repo_name)
                        commit_df, issue_df, create_date,release_df,git_stars,git_forks_count,git_watchers_count,max_language,git_tags_count = git_data.get_additional_data()
                        repo_reader = cluster_attribute_collector.repo_attributes_reader(commit_df, issue_df, release_df,git_stars, git_forks_count, git_watchers_count, max_language, create_date, git_tags_count)
                        xAttributes = repo_reader.read_attributes()

                        row = [project_name, git_url, developers] + xAttributes
                        output_list.append(row)
                        cache[git_url] = row
                        #git_data = git_commit_info.git2data(access_token,repo_owner,source_type,git_url,api_base_url,repo_name)
                        #git_data.create_data()
                    else:
                        row = [project_name, git_url, developers] + ['?']*11
                        output_list.append(row)
                        cache[git_url] = row
                else:
                    output_list.append(cache[git_url])
            except ValueError as e:
                print("Exception occured for ",project_list.loc[i,'git_url'])
                print(e)

    output_df = pd.DataFrame(output_list, columns = ['Project Name', 'git_url', 'Developers', 'Commit #', 'Closed Issues', 'Releases', 'Tags', 'Open Issues', 'Duration', 'Stars', 'Forks', 'Watchers', 'Language', 'Latest commit year'])

    print(output_df)

    output_df.to_csv('Clustering/se_projects_' + str(file_index) + '_with_other_attributes.csv', index=False)
