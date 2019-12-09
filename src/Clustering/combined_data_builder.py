#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd

def cleanup_moissi(file_name):
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        source_projects = os.getcwd() + '/' + file_name
    else:
        source_projects = os.getcwd() + '\\' + file_name

    source_projects = pd.read_csv(source_projects)
    source_projects['Type'] = 'MoISSI'
    source_projects = source_projects[source_projects['git_url'] != '?']
    return source_projects

def cleanup_se(file_name):
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        source_projects = os.getcwd() + '/' + file_name
    else:
        source_projects = os.getcwd() + '\\' + file_name

    source_projects = pd.read_csv(source_projects)
    source_projects['Type'] = 'SE'
    return source_projects

number_of_samples = 10
starting_index = 4

for i in range(starting_index, number_of_samples+starting_index):
    se_df = cleanup_se('Samplings_with_mined_data/' + 'se_projects_' + str(i) + '_with_other_attributes.csv')
    moissi_df = cleanup_moissi('moissi_projects_with_other_attributes.csv')

    combined_df = pd.concat([moissi_df, se_df], axis=0)
    output_file_name = 'Combined/combined_data_' + str(i) + '.csv'
    combined_df.to_csv(output_file_name, index=False)
