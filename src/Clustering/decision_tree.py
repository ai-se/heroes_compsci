#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd
from sklearn import tree
from sklearn.tree.export import export_text
import matplotlib.pyplot as plt
import math

def getDecisionTree(index):
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        file_name = 'Combined/combined_data_' + str(index) + '.csv'
        source_projects = os.getcwd() + '/' + file_name
    else:
        file_name = 'Combined\\combined_data_' + str(index) + '.csv'
        source_projects = os.getcwd() + '\\' + file_name
    combined_df = pd.read_csv(source_projects)

    n_samples = combined_df.shape[0]
    sq = math.sqrt(n_samples)
    myTree = tree.DecisionTreeClassifier(min_samples_leaf = 2, min_samples_split=int(sq), ccp_alpha=0.015)
    myTree = myTree.fit(combined_df.drop(['Language', 'Project Name', 'git_url','Type', 'Latest commit year'], axis=1), combined_df['Type'])
    return combined_df, myTree

sample_count = 100
starting_index = 14

xAttributes = [ 'Developers', 'Commit #', 'Closed Issues', 'Releases', 'Tags', 'Open Issues', 'Duration', 'Stars', 'Forks', 'Watchers']

counts = {}
for attr in xAttributes:
    counts[attr] = 0

for index in range(starting_index, starting_index+sample_count):
    combined_df, myTree = getDecisionTree(index)
    #tree.plot_tree(myTree)
    #plt.show()
    r = export_text(myTree, feature_names=xAttributes, show_weights=True)
    print('index = ' + str(index))
    print(r)
    #print('Importances:')
    for i in range(0, len(xAttributes)):
        imp = myTree.feature_importances_[i]
        feature_name = xAttributes[i]
        #print(feature_name + " = " + str(imp))
        if (imp != 0):
            val = counts.get(feature_name, 0)
            counts[feature_name] = val+1

print("Attribute wise counts for the sample decision trees")
arr = [(k, counts[k]) for k in sorted(counts, key=counts.get, reverse=True)]
for pr in arr:
    print(pr[0] + ' = ' + str(pr[1])) 

