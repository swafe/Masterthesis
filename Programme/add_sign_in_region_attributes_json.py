# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 10:51:47 2020

@author: sven
automaticcly add  "sample": "sign" to  "region_attributes": { in json
"""


#%%
import shutil
import os

import numpy as np
import json 




#%%

path_test_dir_signs = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_1\dataset\dataset_8205_1\snipped_sign'#'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\dataset\dataset_9091\all_img_horizonal' #'C:\Users\sven\Desktop\Masterthesis\github\data\vgg_annotation\img_horizontal\project_9091\all_img_train_val_and_json'
json_name_signs = 'via_project_4Sep2020_17h29m_json.json'#'sign_via_project_9Jul2020_22h46m_json(2).json' #'via_project_9Jul2020_22h46m_json(2).json'
json_file_dir_signs = os.path.join(path_test_dir_signs, json_name_signs) 

# Opening JSON file 
f_signs = open(json_file_dir_signs) 
# returns JSON object as a dictionary 
data_signs = json.load(f_signs) 
# Closing file 
f_signs.close()
#%%
data_new = data_signs
data_keys_json = list(data_new.keys())#['IMG_0332.JPG1076716']
#smaple_sign = "region_attributes": {"sample": "sign"}
for s in data_keys_json:
    for i_regions in data_new[s]['regions']:
        i_regions['region_attributes'] = {"sample": "sign"}# = 'sign'

# save annotation as json
if True:
    json_name_regions_and_sign = 'new_json_sings.json'
    json_file_dir_region_and_sign = os.path.join(path_test_dir_signs, json_name_regions_and_sign) 
    with open(json_file_dir_region_and_sign, 'w') as fp_new:
        json.dump(data_new, fp_new)
