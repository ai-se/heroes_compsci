#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os.path import dirname as up
import os
import platform
from main.git_log import git2repo
import pandas as pd
from datetime import datetime

class repo_attributes_reader(object):

    def __init__(self,commit_df, issue_df, releases_df, git_stars,git_forks_count,git_watchers_count,max_language, create_date, git_tags_count):
        self.commit = commit_df
        self.issues = issue_df
        self.issues = self.issues[self.issues['is_issue'] == True]
        self.releases = releases_df
        self.stars = git_stars
        self.forks = git_forks_count
        self.watchers = git_watchers_count
        self.language = max_language
        self.create_date = create_date
        self.tags = git_tags_count

    def read_attributes(self):
        commit_count = self.commit.shape[0]
        open_issues = self.issues[self.issues['state'] == 'open'].shape[0]
        closed_issues = self.issues[self.issues['state'] == 'closed'].shape[0]
        release_count = self.releases.shape[0]
        latest_commit_time = datetime.fromtimestamp(self.commit['commit_time'].max())
        if latest_commit_time.year == 2019:
            diff = datetime.now() - self.create_date
        else:
            diff = latest_commit_time - self.create_date
        duration = int(diff.days / 7)

        #print('Commit # = ' + str(commit_count))
        #print('Closed issues = ' + str(closed_issues))
        #print('Releases = ' + str(release_count))
        #print('Tags = ' + str(self.tags))
        #print('Open issues = ' + str(open_issues))
        #print('Duration = ' + str(duration))
        #print('Stars = ' + str(self.stars))
        #print('Forks = ' + str(self.forks))
        #print('Watchers = ' + str(self.watchers))
        #print('Language = ' + str(self.language))
        #print('Latest commit time = ' + str(latest_commit_time.year))

        return [commit_count, closed_issues, release_count, self.tags, open_issues, duration, self.stars, self.forks, self.watchers, self.language, latest_commit_time.year]
