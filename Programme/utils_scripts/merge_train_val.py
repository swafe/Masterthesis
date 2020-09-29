# -*- coding: utf-8 -*-
"""
Split one dataset to trainig and validation
Created on Sat Jun 20 14:45:00 2020
from: https://gitlab.com/vgg/via/-/blob/master/via-2.x.y/scripts/io/merge_via2_projects.py
@author: sven
"""
# Merge two or more VIA2 projects
#
# Author: Abhishek Dutta <adutta@robots.ox.ac.uk>
# Date: 18 May 2020

import json
import os
# add the filename of all VIA2 projects
# Note: all VIA projects should have same attributes and project settings
path_1 = r'C:\Users\sven\Desktop\Masterthesis\github\data\vgg_annotation\img_horizontal\project_8205_1\prepare_test_for_new_train_02\till_0106'
filename_1 = 'edit_till_0106.json'
pat_filename_1 = os.path.join(path_1,filename_1)

path_2 = r'C:\Users\sven\Desktop\Masterthesis\github\data\vgg_annotation\img_horizontal\new_train_01\all_img_train_val_and_json'
filename_2 = 'via_project_merged.json'
pat_filename_2 = os.path.join(path_2,filename_2)

filename_list = [pat_filename_1, pat_filename_2]
path_output= r'C:\Users\sven\Desktop\Masterthesis\github\data\vgg_annotation\img_horizontal\new_train_02'
filename_output = ' via_project_merged.json'
output_filename = os.path.join(path_output,filename_output)

# copy attributes and other project settings from one of the projects
# assumption: all the projects have same attributes and settings
via2 = {}
with open(filename_list[0], 'r') as f:
  via2 = json.load(f)

discarded_count = 0
for i in range(1, len(filename_list)):
  with open(filename_list[i], 'r') as f:
    pdata_i = json.load(f)
    for metadata_i in pdata_i:
      # check if a metadata already exists
      if metadata_i not in via2:
        via2[metadata_i] = pdata_i[metadata_i]
      else:
        discarded_count = discarded_count + 1

with open(output_filename, 'w') as fout:
  json.dump(via2, fout)
print('Written merged project to %s (discarded %d metadata)' % (output_filename, discarded_count))

