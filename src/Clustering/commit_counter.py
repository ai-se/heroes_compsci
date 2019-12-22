#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd

if platform.system() == 'Darwin' or platform.system() == 'Linux':
    input_dir_path = os.getcwd() + '/'
else:
    input_dir_path = os.getcwd() + '\\'

input_path = input_dir_path + 'moissi_projects_with_other_attributes.csv'

input_df = pd.read_csv(input_path)

commit_sum = input_df['Commit #'].sum()

print(commit_sum)
