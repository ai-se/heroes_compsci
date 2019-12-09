#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd
from sklearn import tree
from sklearn.tree.export import export_text
import matplotlib.pyplot as plt

def cleanup_moissi(file_name):
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        source_projects = os.getcwd() + '/' + file_name
    else:
        source_projects = os.getcwd() + '\\' + file_name

    source_projects = pd.read_csv(source_projects)
    source_projects['Type'] = 'MoISSI'
    source_projects = source_projects[source_projects['git_url'] != '?']
    return source_projects

def cleanup_se(file_name):
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        source_projects = os.getcwd() + '/' + file_name
    else:
        source_projects = os.getcwd() + '\\' + file_name

    source_projects = pd.read_csv(source_projects)
    source_projects['Type'] = 'SE'
    return source_projects

def getDecisionTree():
    moissi_df = cleanup_moissi('moissi_projects_with_other_attributes.csv')
    se_df = cleanup_se('Sampling_3/se_projects_3_with_other_attributes.csv')
    combined_df = pd.concat([moissi_df, se_df], axis=0)
    combined_df.reset_index(inplace=True, drop=True)
    combined_df.to_csv('Combined/combined_data_3.csv', index=False)
    myTree = tree.DecisionTreeClassifier(min_samples_leaf = 10)
    myTree = myTree.fit(combined_df.drop(['Language', 'Project Name', 'git_url','Type'], axis=1), combined_df['Type'])
    return combined_df, myTree

combined_df, myTree = getDecisionTree()
#tree.plot_tree(myTree)
#plt.show()
xAttributes = [ 'Developers', 'Commit #', 'Closed Issues', 'Releases', 'Tags', 'Open Issues', 'Duration', 'Stars', 'Forks', 'Watchers','Latest commit year']
r = export_text(myTree, feature_names=xAttributes, show_weights=True)
print(r)
print('Importances:')
for i in range(0, len(xAttributes)):
    print(xAttributes[i] + " = " + str(myTree.feature_importances_[i]))
