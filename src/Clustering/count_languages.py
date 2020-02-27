#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd

file_name = "moissi_projects_with_other_attributes.csv"
#file_name = "se_all_projects_with_other_attributes.csv"
file_path = os.getcwd() + '/' + file_name

df = pd.read_csv(file_path)
df = df[['Project Name','Language']]
val = df.groupby(['Language']).count().sort_values(by='Project Name', ascending=False)
print(val)
