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

    print("SE count:")
    print(se_df.shape[0])
    print("MoISSI count:")
    print(mossi_df.shape[0])
    extraAttributesToBeKept = ['Project Github Link', 'Type']

    combined_df = pd.concat([mossi_df, se_df], axis=0)
    combined_df.reset_index(inplace=True, drop=True)

    print(combined_df)

    xAttributesNorm = []

    # Scale the features from 0 to 1
    for xLabel in xAttributes:
        combined_df[xLabel+'_norm'] = normalize(combined_df[xLabel])
        xAttributesNorm.append(xLabel+'_norm')

    # Determined as per elbow analysis
    desiredK = 8
    desired_clustering = KMeans(n_clusters=desiredK).fit(combined_df.drop(xAttributes + extraAttributesToBeKept, axis=1).dropna(axis=1))
    combined_df['cluster_no'] = desired_clustering.labels_

    m_count_map = {}
    se_count_map = {}

    for index,row in combined_df.iterrows():
        cluster_no = row['cluster_no']
        if (row['Type'] == 'SE'):
            cnt = se_count_map.get(cluster_no, 0)
            se_count_map[cluster_no] = cnt+1
        else:
            cnt = m_count_map.get(cluster_no, 0)
            m_count_map[cluster_no] = cnt+1

    print("MoISSI / SE ratios: (ideal count ~ " + str(mossi_df.shape[0]/se_df.shape[0]) + ")")
    print("INF = Only MoISSI cluster, 0.0 = Only SE cluster")
    for cluster_no in range(0,desiredK):
        m_val = m_count_map.get(cluster_no, 0)
        se_val = se_count_map.get(cluster_no, 0)
        ratio = (m_val / se_val) if se_val != 0 else 'INF'
        print("Cluster no " + str(cluster_no) + ": " + str(ratio) + "  (cluster count = " + str(m_val+se_val) + ")")

    something = combined_df.groupby(combined_df['cluster_no'])[xAttributes].median()
    print(something)

    #print(combined_df.drop(xAttributesNorm, axis=1).sort_values(by=['cluster_no']))

getKGraph()
