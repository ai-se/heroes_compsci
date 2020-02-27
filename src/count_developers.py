#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

file_name = 'contributor_countries_all.csv'
path = os.getcwd() + '/' + file_name

df = pd.read_csv(path)

val = df['Total Developers'].sum()
print(val)

print(df)
