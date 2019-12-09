#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

xAttributes = ['Commit #','Closed Issues','Releases','Tags','Open Issues','Duration']
#xAttributes = ['Commit #','Closed Issues','Releases','Tags','Stars']

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
    source_projects['Type'] = 'MoISSI'
    return source_projects

def cleanup_se(file_name):
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        source_projects = os.getcwd() + '/' + file_name
    else:
        source_projects = os.getcwd() + '\\' + file_name

    source_projects = pd.read_csv(source_projects)
    source_projects['Type'] = 'SE'
    return source_projects



def getKGraph(i):
    #extraAttributesToBeKept = ['Developers', 'Project Name', 'git_url', 'Type', 'Language', 'Forks', 'Watchers', 'Latest commit year', 'Duration', 'Open Issues']
    extraAttributesToBeKept = ['Developers', 'Project Name', 'git_url', 'Type', 'Language', 'Forks', 'Watchers', 'Latest commit year','Stars']

    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        source_projects = os.getcwd() + '/Combined/' + 'combined_data_' + str(i) + '.csv'
    else:
        source_projects = os.getcwd() + '\\Combined\\' + 'combined_data_' + str(i) + '.csv'

    combined_df = pd.read_csv(source_projects)

    se_count = combined_df[combined_df['Type'] == 'SE'].shape[0]
    moissi_count = combined_df[combined_df['Type'] == 'MoISSI'].shape[0]
    print("SE count: " + str(se_count))
    print("MoISSI count: " + str(moissi_count))

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

    #print("MoISSI / SE ratios: (ideal count ~ " + str(moissi_count/se_count) + ")")
    pruned_clusters = []
    print("INF = Only MoISSI cluster, 0.0 = Only SE cluster")
    for cluster_no in range(0,desiredK):
        m_val = m_count_map.get(cluster_no, 0)
        se_val = se_count_map.get(cluster_no, 0)
        ratio = (m_val / se_val) if se_val != 0 else 'INF'
        total_val = m_val + se_val
        if (total_val != 1):
            print("Cluster no " + str(cluster_no) + ": " + str(ratio) + "  (cluster count = " + str(m_val+se_val) + ")")
        else:
            pruned_clusters.append(cluster_no)

    print("Following clusters are pruned due to small size: " + str(pruned_clusters))


    something = combined_df[~combined_df.cluster_no.isin(pruned_clusters)].groupby(combined_df['cluster_no'])[xAttributes].median()
    #something = combined_df[(combined_df['cluster_no'] not in pruned_clusters)].groupby(combined_df['cluster_no'])[xAttributes].median()
    print("============================================")
    print("Medians:")
    print(something)

    #print(combined_df.drop(xAttributesNorm, axis=1).sort_values(by=['cluster_no']))

getKGraph(9)
