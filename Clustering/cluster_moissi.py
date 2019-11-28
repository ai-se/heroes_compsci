#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def normalize(x):
    mn = x.min()
    mx = x.max()
    diff = mx - mn
    return x.map(lambda z: (z - mn)/diff)

if platform.system() == 'Darwin' or platform.system() == 'Linux':
    source_projects = os.getcwd() + '/MolSSI Projects DB - top_projects.csv'
else:
    source_projects = os.getcwd() + '\\MolSSI Projects DB - top_projects.csv'

source_projects = pd.read_csv(source_projects)

xAttributes = ['Developers', 'Commits #', 'Closed Issues', 'Releases', 'active_since']
removeAttributes = ['Project Github Link', 'Language', 'Main Link', 'Source', 'Type', 'Testing', 'Active', 'Email', 'Name', 'Timezones', 'Opened Issues']
extraAttributesToBeKept = ['Project Name', 'Active years', 'Sanity_passed']


#Input cleanup
input_df = source_projects.drop(removeAttributes, axis=1)
input_df = input_df[input_df['Sanity_passed'].map(lambda x: (str(x) == 'yes' or str(x) == 'Yes'))]
input_df['active_since'] = input_df['Active years'].map(lambda x: 2019-x+1)

xAttributesNorm = []

# Scale the features from 0 to 1
for xLabel in xAttributes:
    input_df[xLabel+'_norm'] = normalize(input_df[xLabel])
    xAttributesNorm.append(xLabel+'_norm')

# Decided as per elbow analysis
desiredK = 12
desired_clustering = KMeans(n_clusters=desiredK).fit(input_df.drop(xAttributes + extraAttributesToBeKept, axis=1).dropna(axis=1))

input_df['cluster_no'] = desired_clustering.labels_

input_array = input_df.values
print(input_df.drop(xAttributesNorm, axis=1).sort_values(by=['cluster_no']))

