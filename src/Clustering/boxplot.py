#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot(file_name):
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        input_dir_path = os.getcwd() + '/'
    else:
        input_dir_path = os.getcwd() + '\\'

    input_path = input_dir_path + file_name

    input_df = pd.read_csv(input_path)
    input_df = input_df.replace('?', np.nan).dropna()

    boxplots = []
    attributes_to_plot = ['Developers','Commit #','Closed Issues','Releases','Tags','Open Issues','Duration','Stars','Forks','Watchers']
    #attributes_to_plot = ['Watchers']#,'Commit #','Closed Issues','Releases','Tags','Open Issues','Duration','Stars','Forks','Watchers']

    fig, boxplots = plt.subplots(1, 10, constrained_layout=True)
    #fig, boxplots = plt.subplots()

    for i in range(len(attributes_to_plot)):
        attr = attributes_to_plot[i]
        temp = pd.to_numeric(input_df[attr]).plot.box(showfliers=False, whis=[5,95], ax=boxplots[i], patch_artist=True)

    #plt.tight_layout()
    plt.show()

#plot('moissi_projects_with_other_attributes.csv')
plot('se_all_projects_with_other_attributes.csv')
