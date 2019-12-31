#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd

if platform.system() == 'Darwin' or platform.system() == 'Linux':
    source_projects = os.getcwd() + '/se_all_projects_with_other_attributes.csv'
else:
    source_projects = os.getcwd() + '\\se_all_projects_with_other_attributes.csv'

source_projects = pd.read_csv(source_projects)

small_projects = source_projects[(source_projects['Developers'] >= 8) & (source_projects['Developers'] < 15)]
medium_projects = source_projects[(source_projects['Developers'] >= 15) & (source_projects['Developers'] < 30)]
large_projects = source_projects[source_projects['Developers'] >= 30]

number_of_samples = 100
starting_index = 14

for i in range(starting_index,number_of_samples+starting_index):
    print("Here at i = " + str(i))
    small_sample = small_projects.sample(20)
    medium_sample = medium_projects.sample(20)
    large_sample = large_projects.sample(19)
    sample_projects = pd.concat([small_sample, medium_sample, large_sample], axis=0)
    sample_projects.reset_index(inplace=True, drop=True)
    file_name = 'Samplings_with_mined_data/se_projects_' + str(i) + '_with_other_attributes.csv'
    sample_projects.to_csv(file_name, index=False)
    #print(sample_projects)
