#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


xAttributes = ['Commit #','Closed Issues','Releases','Tags','Duration', 'Open Issues']

def normalize(x):
    mn = x.min()
    mx = x.max()
    diff = mx - mn
    return x.map(lambda z: (z - mn)/diff)

def getKGraph(i):
    extraAttributesToBeKept = ['Developers', 'Project Name', 'git_url', 'Type', 'Language', 'Forks', 'Watchers', 'Latest commit year', 'Stars']

    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        source_projects = os.getcwd() + '/Combined/' + 'combined_data_' + str(i) + '.csv'
    else:
        source_projects = os.getcwd() + '\\Combined\\' + 'combined_data_' + str(i) + '.csv'

    combined_df = pd.read_csv(source_projects)
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

getKGraph(9)
