#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas as pd
from main.git_log import git2data
import geocoder
from collections import Counter
from ratelimiter import RateLimiter

def get_country_name(name):
    if (name == 'United States'):
        return 'United States of America'
    elif (name == 'België / Belgique / Belgien'):
        return 'Belgium'
    elif (name == 'België - Belgique - Belgien'):
        return 'Belgium'
    elif (name == 'Россия'):
        return 'Russia'
    elif (name == '中国'):
        return 'China'
    elif (name == 'Österreich'):
        return 'Austria'
    elif (name == '日本 (Japan)' or name == '日本'):
        return 'Japan'
    elif (name == 'Türkiye'):
        return 'Turkey'
    elif (name == 'Sverige'):
        return 'Sweden'
    elif (name == 'España'):
        return 'Spain'
    elif (name == 'Україна'):
        return 'Ukraine'
    elif (name == 'China 中国'):
        return 'China'
    elif (name == 'ישראל'):
        return 'Israel'
    elif (name == '대한민국'):
        return 'Republic of Korea'
    elif (name == 'Schweiz/Suisse/Svizzera/Svizra'):
        return 'Switzerland'
    elif (name == 'Suomi'):
        return 'Finland'
    elif (name == 'Ísland'):
        return 'Iceland'
    elif (name == 'Česko'):
        return 'Czech Republic'
    elif (name == 'Česká republika'):
        return 'Czech Republic'
    elif (name == 'Ελλάδα'):
        return 'Greece'
    elif (name == 'Беларусь'):
        return 'Belarus'
    elif (name == 'ایران'):
        return 'Iran'
    elif (name == '臺灣'):
        return 'Taiwan'
    else:
        return name

@RateLimiter(max_calls = 1, period = 1)
def get_geo(loc):
    geo_obj = geocoder.osm(loc)
    return geo_obj


if platform.system() == 'Darwin' or platform.system() == 'Linux':
    data_path = os.getcwd() + '/Clustering/'
    #data_path = os.getcwd() + '/Clustering/project_list.csv'
    #print(os.getcwd())
else:
    #data_path = os.getcwd() + '\\Clustering\\project_list.csv'
    data_path = os.getcwd() + '\\Clustering\\'

file_name = 'MolSSI_cleaned_input.csv'
#file_name = 'temp_input.csv'
project_list = pd.read_csv(data_path + file_name)
project_name_available = True if ('Project Name' in project_list.columns) else False

output_list = []

#cache_path = os.getcwd() + '/cache/'

for i in range(project_list.shape[0]):
    try:
        print("I am here at " + str(i))
        access_token = project_list.loc[i,'access_token']
        repo_owner = project_list.loc[i,'repo_owner']
        source_type = project_list.loc[i,'source_type']
        repo_name = project_list.loc[i,'repo_name']
        developers = project_list.loc[i, 'num_dev']
        git_url = project_list.loc[i,'git_url']
        api_base_url = project_list.loc[i,'api_base_url']
        project_name = repo_name if project_name_available == False else project_list.loc[i, 'Project Name']
        if (source_type.lower() == 'github_repo'):
            git_data = git2data.git2data(access_token,repo_owner,source_type,git_url,api_base_url,repo_name)
            contributors = git_data.get_contributors()
            contributor_count = len(contributors)
            #contributors = contributors[:10]
            contributors = [x['login'] for x in contributors]
            user_locations = [git_data.get_user(login)['location'] for login in contributors]
            countries = []
            for loc in user_locations:
                geo_obj = get_geo(loc)
                if (geo_obj == None or geo_obj.osm == None or ('addr:country' not in geo_obj.osm)):
                    if (loc == 'Tromsø / Blacksburg'):
                        countries.append('Norge')
                    elif (loc == 'Frederick, Maryland, U.S.A.' \
                            or loc == 'LOS ALAMOS NATIONAL LABORATORY, T-1 Division, TA-3 Bldg. 200, Room 276 Los Alamos, NM 87545' \
                            or loc == 'Aerospace Engineering & Mechanics | University of Minnesota' or loc == 'New York, NY, U.S.A.' \
                            or loc == 'San Jose, CA - Seattle, WA'):
                        countries.append('United States of America')
                    elif (loc == 'The Netherlands'):
                        countries.append('Nederland')
                    elif (loc == 'Cambridge, MA and Lewiston, ME' or loc == 'Miami-ish' or loc == 'Center for Computational Quantum Chemistry, University of Georgia'):
                        countries.append('United States of America')
                    elif (loc == 'Agartala | Bangalore' or loc == 'BITS PILANI K.K. BIRLA GOA CAMPUS'):
                        countries.append('India')
                    elif (loc == 'Rueil Malmaison / Palaiseau' or loc == 'Earth, ǝɔuɐɹɟ'):
                        countries.append('France')
                    elif (loc == 'Cambrigde, UK'):
                        countries.append('United Kingdom')
                    elif (loc == 'Dresden, Gremany' or loc == 'Garchin bei Muenchen, Germany' \
                            or loc == 'Germany | HHN (computer science)'):
                        countries.append('Deutschland')
                    elif (loc == 'Fysikvej, 2800 Kgs. Lyngby'):
                        countries.append('Danmark')
                    else:
                        if (loc != None):
                            print('Location not found for %s' % loc)
                        countries.append('Unknown')
                else:
                    countries.append(geo_obj.osm['addr:country'])

            countries = [get_country_name(x) for x in countries]
            print('Countries')
            print(countries)
            country_counter = Counter(countries)

            #commit_df, issue_df, create_date,release_df,git_stars,git_forks_count,git_watchers_count,max_language,git_tags_count = git_data.get_additional_data()
            #repo_reader = cluster_attribute_collector.repo_attributes_reader(commit_df, issue_df, release_df,git_stars, git_forks_count, git_watchers_count, max_language, create_date, git_tags_count)
            #xAttributes = repo_reader.read_attributes()
            print(project_name)
            print(user_locations)

            #row = [project_name, git_url, developers] + user_locations
            row = [project_name, contributor_count, country_counter]
            #df = pd.DataFrame(row, columns=['Project Name', 'All Developers', 'Countries'])
            #df.to_pickle(file_path)
            output_list.append(row)
            #cache[git_url] = row
            #git_data = git_commit_info.git2data(access_token,repo_owner,source_type,git_url,api_base_url,repo_name)
            #git_data.create_data()
        else:
            print('%s is not github repo' % project_name)
            #row = [project_name, git_url, developers] + ['?']
            #output_list.append(row)
    except ValueError as e:
        print("Exception occured for ",project_list.loc[i,'git_url'])
        print(e)

all_countries = set()
for item in output_list:
    for country in item[2]:
        all_countries.add(country)
#all_countries = [country for item in output_list for country in item[2]]
print('All countries')
print(all_countries)
all_countries_list = list(all_countries)
cols = ['Project Name', 'Total Developers'] + all_countries_list
print('Columns')
print(cols)

data = []

for item in output_list:
    row = [item[0], item[1]]
    counter = item[2]
    for country in all_countries_list:
        row.append(counter[country])
    data.append(row)

final_df = pd.DataFrame(data, columns=cols)
print(final_df)
final_df.to_csv('contributor_countries_all.csv', index=False)
