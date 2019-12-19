#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd

def plot_percentiles(file_name):
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        source_projects = os.getcwd() + '/' + file_name
    else:
        source_projects = os.getcwd() + '\\' + file_name

    source_projects = pd.read_csv(source_projects)
    xAttributes = [ 'Developers', 'Commit #', 'Closed Issues', 'Releases', 'Tags', 'Open Issues', 'Duration', 'Stars', 'Forks', 'Watchers','Latest commit year']
    percentiles = [0.0, 0.25, 0.5, 0.75, 1.0]

    for attr in xAttributes:
        print("For " + attr + ":")
        print("--For SE:")
        temp = source_projects[source_projects['Type'] == 'SE']
        print(temp[attr].quantile(percentiles))
        print("--For CompSci:")
        temp2 = source_projects[source_projects['Type'] == 'MoISSI']
        print(temp2[attr].quantile(percentiles))

plot_percentiles("Combined/combined_data_3.csv")
        
