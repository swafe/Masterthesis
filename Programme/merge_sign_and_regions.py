# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 17:02:42 2020

@author: sven
"""

#%%
import shutil
import os

import numpy as np
import json 

from PIL import Image, ImageDraw



#%%
# Python program to read json file 
# change here !!!!!!
path_test_dir_regions = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_1\dataset\dataset_8205_1\snipped_sign' #'C:\Users\sven\Desktop\Masterthesis\github\data\vgg_annotation\img_horizontal\project_9091\all_img_train_val_and_json'
json_name_regions = 'via_project_4Sep2020_15h46m_json.json'#'via_project_merged.json'
json_file_dir_regions = os.path.join(path_test_dir_regions, json_name_regions) 

path_test_dir_sign = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_1\dataset\dataset_8205_1\snipped_sign'#'C:\Users\sven\Desktop\Masterthesis\github\data\vgg_annotation\img_horizontal\project_9091\all_img_train_val_and_json'
json_name_sign = 'new_json_sings.json'#'new_json_sings.json'
json_file_dir_sign = os.path.join(path_test_dir_sign, json_name_sign) 

# Opening JSON file 
f_regions = open(json_file_dir_regions) 
# returns JSON object as a dictionary 
data_regions = json.load(f_regions) 
# Closing file 
f_regions.close()
# Opening JSON file 
f_sign = open(json_file_dir_sign) 
data_sign = json.load(f_sign) 
f_sign.close()

#%%
data_new = data_regions
regions = []
for i in data_regions:
    regionsi  = data_sign[i]['regions']
    for i_signs in regionsi:
        data_new[i]['regions'].append(i_signs)
    


#%%
# save annotation as json
if True:
    new_json_path = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_1\dataset\dataset_8205_1\snipped_sign'#'C:\Users\sven\Desktop\Masterthesis\github\data\vgg_annotation\img_horizontal\project_9091\all_img_train_val_and_json'
    json_name_regions_and_sign = 'regions_and_sign.json'
    json_file_dir_region_and_sign = os.path.join(new_json_path, json_name_regions_and_sign) 
    with open(json_file_dir_region_and_sign, 'w') as fp_new:
        json.dump(data_new, fp_new)




#%%




#%%



















