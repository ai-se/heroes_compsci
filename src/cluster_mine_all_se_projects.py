#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd
from main.git_log import git2data
from Clustering import cluster_attribute_collector

if platform.system() == 'Darwin' or platform.system() == 'Linux':
    clustering_data_path = os.getcwd() + '/Clustering/'
    earlier_samples_data_path = clustering_data_path + 'Samplings_with_mined_data/'
else:
    clustering_data_path = os.getcwd() + '\\Clustering\\'
    earlier_samples_data_path = clustering_data_path + 'Samplings_with_mined_data\\'

hero_list_path = clustering_data_path + 'hero_list.csv'

start = 4
end = 13

cache = {}

for index in range(start, end+1):
    file_name = earlier_samples_data_path + 'se_projects_' + str(index) + '_with_other_attributes.csv'
    earlier_data = pd.read_csv(file_name)
    for i,row in earlier_data.iterrows():
        git_url = row['git_url']
        if (git_url not in cache):
            cache[git_url] = row.to_numpy()

print('Old files read. Cache size = ' + str(len(cache)))

hero_list_df = pd.read_csv(hero_list_path)

output_list = []
project_name_available = True if ('Project Name' in hero_list_df.columns) else False

for i in range(hero_list_df.shape[0]):
        try:
            print("I am here at i = " + str(i))
            access_token = hero_list_df.loc[i,'access_token']
            repo_owner = hero_list_df.loc[i,'repo_owner']
            source_type = hero_list_df.loc[i,'source_type']
            repo_name = hero_list_df.loc[i,'repo_name']
            developers = hero_list_df.loc[i, 'num_dev']
            git_url = hero_list_df.loc[i,'git_url']
            api_base_url = hero_list_df.loc[i,'api_base_url']
            project_name = repo_name if project_name_available == False else hero_list_df.loc[i, 'Project Name']
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
            print("Exception occured for ",hero_list_df.loc[i,'git_url'])
            print(e)

print(output_list)

output_df = pd.DataFrame(output_list, columns = ['Project Name', 'git_url', 'Developers', 'Commit #', 'Closed Issues', 'Releases', 'Tags', 'Open Issues', 'Duration', 'Stars', 'Forks', 'Watchers', 'Language', 'Latest commit year'])

print(output_df)

output_df.to_csv('Clustering/se_all_projects_with_other_attributes.csv', index=False)
