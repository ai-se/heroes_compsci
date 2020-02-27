#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

file_name = 'moissi_projects_with_other_attributes.csv'
path = os.getcwd() + '/' + file_name

df = pd.read_csv(path)

val = df['Developers'].sum()
print(val)

print(df)
