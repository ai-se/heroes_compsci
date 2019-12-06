#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


xAttributes = ['Developers', 'Commits #', 'Closed Issues', 'Releases']

def normalize(x):
    mn = x.min()
    mx = x.max()
    diff = mx - mn
    return x.map(lambda z: (z - mn)/diff)

def cleanup_moissi(file_name):
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        source_projects = os.getcwd() + '/' + file_name
    else:
        source_projects = os.getcwd() + '\\' + file_name

    source_projects = pd.read_csv(source_projects)

    removeAttributes = ['Project Name', 'Language', 'Main Link', 'Source', 'Type', 'Testing', 'Active', 'Email', 'Name', 'Timezones', 'Opened Issues', 'Active years']
    extraAttributesToBeKept = ['Project Github Link', 'Sanity_passed']


    #Input cleanup
    input_df = source_projects
    #input_df['active_since'] = input_df['Active years'].map(lambda x: 2019-x+1)
    input_df = input_df.drop(removeAttributes, axis=1)
    input_df = input_df[input_df['Sanity_passed'].map(lambda x: (str(x) == 'yes' or str(x) == 'Yes'))]
    input_df = input_df.drop(['Sanity_passed'], axis=1)
    input_df['Type'] = 'MoISSI'
    return input_df

def cleanup_se(file_name):
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        source_projects = os.getcwd() + '/' + file_name
    else:
        source_projects = os.getcwd() + '\\' + file_name

    source_projects = pd.read_csv(source_projects)

    #removeAttributes = ['Project Name', 'Language', 'Main Link', 'Source', 'Type', 'Testing', 'Active', 'Email', 'Name', 'Timezones', 'Opened Issues', 'active_since', 'Active years']
    extraAttributesToBeKept = ['Project Github Link']


    #Input cleanup
    input_df = source_projects
    #input_df['active_since'] = input_df['Active years'].map(lambda x: 2019-x+1)
    #input_df = input_df.drop(removeAttributes, axis=1)
    #input_df = input_df[input_df['Sanity_passed'].map(lambda x: (str(x) == 'yes' or str(x) == 'Yes'))]
    #input_df = input_df.drop(['Sanity_passed'], axis=1)
    input_df['Type'] = 'SE'
    return input_df



def getKGraph():
    mossi_df = cleanup_moissi('MolSSI Projects DB - top_projects.csv')
    se_df = cleanup_se('se_projects_with_other_attributes.csv')
    extraAttributesToBeKept = ['Project Github Link', 'Type']

    combined_df = pd.concat([mossi_df, se_df], axis=0)
    combined_df.reset_index(inplace=True, drop=True)

    print(combined_df)

    xAttributesNorm = []

    # Scale the features from 0 to 1
    for xLabel in xAttributes:
        combined_df[xLabel+'_norm'] = normalize(combined_df[xLabel])
        xAttributesNorm.append(xLabel+'_norm')

    # Doing the elbow analysis
    maxK = combined_df.shape[0]
    val = list()
    kmeans_objects = list()
    for k in range(1,maxK+1):
        kmeans = KMeans(n_clusters=k).fit(combined_df.drop(xAttributes + extraAttributesToBeKept, axis=1).dropna(axis=1))
        val.append(kmeans.inertia_)
        kmeans_objects.append(kmeans)
    plt.plot(range(1,k+1), val)
    plt.ylabel('Inertia')
    plt.xlabel('K values')
    plt.show()

#getKGraph('MolSSI Projects DB - top_projects.csv')
#getKGraph('se_projects_with_other_attributes.csv')
getKGraph()
