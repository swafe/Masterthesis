# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 17:52:15 2020

@author: sven
script to change key in json to rfere regions from one json to other images

"""

import shutil
import os

import numpy as np
import json 
import csv

from PIL import Image, ImageDraw
#%%
def get_access_to_json(image_path):
  image_name = os.path.splitext(os.path.basename(image_path))[0]
  filename = os.path.basename(image_path)
  img_size =  os.path.getsize(image_path)
  filename_and_size = filename + str(img_size)
  return filename_and_size, filename
#%%

# Python program to read json file 
# change here !!!!!!
path_data = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_1\dataset\dataset_8205_1\snipped_sign' #'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_1\dataset\dataset_8205_1\snipped_ohne_sign'#'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_1\dataset\dataset_8205_1\all_img' #'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_2\snipped_img\snipped_ohne_sign_all\RGB' #'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_2\snipped_img\snipped_sign' #'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\Soil_Classification\dataset_train_till_IMG_5203BKF 38_4\RGB' #'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\Soil_Classification\dataset_train_till_IMG_5203BKF 38_4'
#json_name = 'via_project_10Jul2020_12h16m_json(15).json'  #'via_project_merged.json'
json_name = 'changed_json_Plastik.json'#'via_project_4Sep2020_18h28m_json(2).json' #'result_masks(35).json' #'via_train_Feinsand.json' #'rgb_regions_train_val_test.json' #'via_project_5Aug2020_23h19m_json(3)_regions_and_sign.json' #'changed_json_Auffuellung.json' #'changed_json_soiltype_id.json' #'via_val02.json'
json_file_dir = os.path.join(path_data, json_name)     
     

# Opening JSON file 
f = open(json_file_dir) 
# returns JSON object as a dictionary 
data_01 = json.load(f) 
# Closing file 
f.close()   
    
#%%
new_json_path = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_1\dataset\dataset_8205_1\snipped_ohne_sign' #path_data # r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\snipped_ohne_sign_all'
json_name_regions_and_sign = 'rgb_regions_train_val_test.json' #'regions_and_sign.json' #'changed_json.json'
json_file_dir_region_and_sign = os.path.join(new_json_path, json_name_regions_and_sign) 

#get all images in path_test_dir oder new_json_path
image_paths = []
for filename in sorted(os.listdir(new_json_path), key=str.lower):
    if os.path.splitext(filename)[1].lower() in ['.png', '.jpg', '.jpeg']:
      image_paths.append(os.path.join(new_json_path, filename))
      
data_new = data_01
for path_i in image_paths:
    filename_and_size, filename = get_access_to_json(path_i) 
    print(filename_and_size)
    data_keys_json = list(data_new.keys())#['IMG_0332.JPG1076716']
    #            basename_img_file_all.append(basename_img_file)
    for s in data_keys_json:
        if filename in s:
            matching = s    
            data_new[filename_and_size]=data_new.pop(matching)

# save annotation as json
if True:
    with open(json_file_dir_region_and_sign, 'w') as fp_new:
        json.dump(data_new, fp_new)   
    
    
  
    
 
    
    
    
    
    
    
    
#%%   ##############change region name to int in changed_json.json
        
classes_soiltype = ["Mutterboden","Schluff","Klei","Torf","Sand","Feinsand","Mittelsand",
                            "Plastik","Unbekannt","Darg","Mudde","Grobsand","Wurzeln","Torf + Sand",
                            "Braunkohle + Holz","Auffuellung",'Grobschluff','Ton','Tonstein']


#%%
data_new2 = data_new #data_01   
#%%            
data_keys_json2 = list(data_new2.keys())

for key in data_keys_json2:
    for regions_i in data_new2[key]['regions']:
        #print(len(regions_i['region_attributes']))
        if len(regions_i['region_attributes']) == 0:
            print(key)
        else:
            soiltype = regions_i['region_attributes']['soiltype']
#            if soiltype == 'Grobdsand':
#                regions_i['region_attributes']['soiltype']= 'Grobsand'
            if soiltype in classes_soiltype :
                index_class = classes_soiltype.index(soiltype)
                regions_i['region_attributes']['soiltype']=index_class
            else:
                print('not in class')
                print(soiltype)
                print(key)
#%%
new_json_path_soiltype_id = new_json_path #path_data # r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\snipped_ohne_sign_all'
json_name_regions_and_sign_soiltype_id = 'changed_json_soiltype_id.json'
json_file_dir_region_and_sign_soiltype_id = os.path.join(new_json_path_soiltype_id, json_name_regions_and_sign_soiltype_id) 
# save annotation as json
if True:
    with open(json_file_dir_region_and_sign_soiltype_id, 'w') as fp_new2:
        json.dump(data_new2, fp_new2) 
  
    
        
        
 







       
#%% ####change Auffüllung to Auffuellung in via_project_10Jul2020_12h16m_json(15).json and via_project_10Jul2020_12h16m_attributes(14).json
    
classes_soiltype = 'Pastik' #"Auff\u00c3\u00bcllung"
#%%
data_new2 = data_01               
data_keys_json2 = list(data_new2.keys())

for key in data_keys_json2:
    for regions_i in data_new2[key]['regions']:
        #print(len(regions_i['region_attributes']))
        if len(regions_i['region_attributes']) == 0:
            print(key)
            
        else:
            soiltype = regions_i['region_attributes']['soiltype']
            
            if soiltype == classes_soiltype :
        
                regions_i['region_attributes']['soiltype']= 'Plastik' #'Auffuellung'


#%% save new json
new_json_path_soiltype_id = path_data # r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\snipped_ohne_sign_all'
json_name_regions_and_sign_soiltype_id = 'changed_json_Plastik.json' #'changed_json_Auffuellung.json'
json_file_dir_region_and_sign_soiltype_id = os.path.join(new_json_path_soiltype_id, json_name_regions_and_sign_soiltype_id) 
# save annotation as json
if True:
    with open(json_file_dir_region_and_sign_soiltype_id, 'w') as fp_new2:
        json.dump(data_new2, fp_new2) 
      
        
        
        
        
  #%% counting soiltypes from json: important for  inbalanced weights
  
#%%

# Python program to read json file 
# change here !!!!!!
path_data = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_2\project_9091\snipped_img\snipped_ohne_sign_all\RGB' #'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_1\dataset\dataset_8205_1\snipped_ohne_sign' #'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_2\snipped_img\snipped_ohne_sign_all\RGB' #'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_2\snipped_img\snipped_sign' #'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\Soil_Classification\dataset_train_till_IMG_5203BKF 38_4\RGB' #'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\Soil_Classification\dataset_train_till_IMG_5203BKF 38_4'
#json_name = 'via_project_10Jul2020_12h16m_json(15).json'  #'via_project_merged.json'
json_name = 'changed_json_soiltype_id.json' #'via_project_5Aug2020_23h19m_json(3)_regions_and_sign.json' #'changed_json_Auffuellung.json' #'changed_json_soiltype_id.json' #'via_val02.json'
json_file_dir = os.path.join(path_data, json_name)     
     

# Opening JSON file 
f = open(json_file_dir) 
# returns JSON object as a dictionary 
data_01 = json.load(f) 
# Closing file 
f.close() 
#%%
#!!!!! Grobdsand
classes_soiltype = ["Mutterboden","Schluff","Klei","Torf","Sand","Feinsand","Mittelsand",
                            "Plastik","Unbekannt","Darg","Mudde","Grobsand","Wurzeln","Torf + Sand",
                            "Braunkohle + Holz","Auffuellung",'Grobschluff','Ton','Tonstein']
classes_soiltype_id = [*range(0,len(classes_soiltype),1)]


count_soiltypes =[0] *  len(classes_soiltype) #np.zeros((len(classes_soiltype)))

#%%
data_new3 = data_01               
data_keys_json3 = list(data_new3.keys())

for key in data_keys_json3:
    for regions_i_3 in data_new3[key]['regions']:
        soiltype_3 = regions_i_3['region_attributes']['soiltype']
        for i_type in classes_soiltype_id:
            if soiltype_3 == i_type:
                count_soiltypes[i_type] = count_soiltypes[i_type] + 1

soiltypes_train = np.vstack((classes_soiltype, count_soiltypes))

#%% save to csv
path_Soiltypes_csv = os.path.join(path_data,'Soiltypes_all.csv')
with open(path_Soiltypes_csv, "w", newline="") as f_stypes: 
    if True: #True False 
        fieldnames=['id', 'Soiltype']
        writer = csv.writer(f_stypes)
        writer.writerow(fieldnames)
        writer.writerows([soiltypes_train[0]])
        writer.writerows([soiltypes_train[1]])


        
        
        
