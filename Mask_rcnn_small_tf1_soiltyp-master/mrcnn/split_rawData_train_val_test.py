# -*- coding: utf-8 -*-
"""
Split one dataset to trainig and validation
Created on Sat Jun 20 14:45:00 2020

@author: sven
"""
# Merge two or more VIA2 projects
#
# Author: Abhishek Dutta <adutta@robots.ox.ac.uk>
# Date: 18 May 2020


#%%
import json
import numpy as np
import shutil
import os

def split_rawData_train_val_test(raw_Data_folder_path, filename_json, new_Dataset_path, train_prop=0.7, val_prop=0.25,
                                 soiltypes_to_detect = 'all',
                                 copy_img = True, copy_json = True):  
    """
    raw_Data_folder_path: path to folder with snipped IMG in RGB format and labeld + Annotation from VGG.
        rememder to change region_names to id 
    filename_json: file name of json has to be stored in raw_Data_folder_path
    new_Dataset_path: path to new folder './Dataset_splited'
    
    train_prop, val_prop, (test_prop): ratio of Images 
    soiltypes_to_detect: 'all' or 'Feinsand'  TODO add further types
    """
    root_project_path = raw_Data_folder_path
    # load json of all images
    path_filename_json = os.path.join(root_project_path,filename_json) #'changed_json.json') #via_project_merged.json')
    # copy attributes and other project settings from one of the projects
    # assumption: all the projects have same attributes and settings
    via2 = {}
    with open(path_filename_json, 'r') as f:
      via2 = json.load(f)
    #
    #
    data_keys_json = list(via2.keys()) 
    if soiltypes_to_detect == 'Feinsand':
        data_new2 = via2               
        data_keys_json2 = list(data_new2.keys())
        
        for key in data_keys_json2:
            no_region_counter = 0
            region_remove = []
            for idx_regions, regions_i in enumerate(data_new2[key]['regions']):

                if len(regions_i['region_attributes']) == 0:
                    print(key)
                    print('jooooo')
                    no_region_counter = 1
                else:
                    soiltype = regions_i['region_attributes']['soiltype']

                    if soiltype != 5 : #5 for Feinsand
                        print(idx_regions)
                        region_remove.append(idx_regions)
    #                else:
    #                    print('not in class')
    #                region_counter = region_counter + 1
            if no_region_counter == 0:
                for i_remove in sorted(region_remove, reverse=True):
    #                print(data_new2[key]['regions'][i_remove])
                    del data_new2[key]['regions'][i_remove]
    #
    #
    #seperate json
    data_keys_json_train_val_test = []       
    data_keys_json_train = data_keys_json[0: int(train_prop * np.size(data_keys_json))]
    data_keys_json_val = data_keys_json[int(train_prop * np.size(data_keys_json)):int(train_prop * np.size(data_keys_json))+ int(val_prop * np.size(data_keys_json))]
    data_keys_json_test = data_keys_json[int(train_prop * np.size(data_keys_json))+ int(val_prop * np.size(data_keys_json)):]
    data_keys_json_train_val_test = [data_keys_json_train, data_keys_json_val, data_keys_json_test]
    
    via2_split = []
    if soiltypes_to_detect == 'all':
        via2_train = dict((k,via2[k]) for k in data_keys_json_train)
        via2_val = dict((k,via2[k]) for k in data_keys_json_val)
        via2_test = dict((k,via2[k]) for k in data_keys_json_test)
    
    elif soiltypes_to_detect == 'Feinsand':
        via2_train = dict((k,data_new2[k]) for k in data_keys_json_train)
        via2_val = dict((k,data_new2[k]) for k in data_keys_json_val)
        via2_test = dict((k,via2[k]) for k in data_keys_json_test)
    via2_split= [via2_train, via2_val, via2_test ]
    #
    #
    #copy images to train, val and test folder
    
    # define the name of the directory to be created
    train_val_test= ['train', 'val', 'test']
    for i_train_val_test in range(0,3):
        path_train_val_test = os.path.join(new_Dataset_path,train_val_test[i_train_val_test])
        if os.path.exists(path_train_val_test):
            shutil.rmtree(path_train_val_test)
            os.mkdir(path_train_val_test)
        else:
            os.mkdir(path_train_val_test)
            
        if copy_img:
            for i in data_keys_json_train_val_test[i_train_val_test]:
                img_filename = via2_split[i_train_val_test][i]['filename'] 
                src = os.path.join(root_project_path,img_filename)
                dst = path_train_val_test
                shutil.copy(src,dst)    
        new_splited_json_all = ['via_train.json', 'via_val.json', 'via_test.json']   
        new_splited_json_Feinsand = ['via_train_Feinsand.json', 'via_test_Feinsand.json', 'via_test_Feinsand.json']
        if copy_json:
            if soiltypes_to_detect == 'all':
                output_filename = os.path.join(path_train_val_test,new_splited_json_all[i_train_val_test])
            elif soiltypes_to_detect == 'Feinsand':
                output_filename = os.path.join(path_train_val_test,new_splited_json_Feinsand[i_train_val_test])
            with open(output_filename, 'w') as fout:
              json.dump(via2_split[i_train_val_test], fout)  
    
    #
    #
#%%
    
    
raw_Data_folder_path = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_2\snipped_img\snipped_ohne_sign_all\RGB'
filename_json = 'rgb_regions_train_val_test.json'
new_Dataset_path  = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_2\snipped_img\snipped_ohne_sign_all\RGB' 
split_rawData_train_val_test(raw_Data_folder_path, filename_json, new_Dataset_path, train_prop = 0.7, val_prop=0.25,
                                 soiltypes_to_detect = 'all',
                                 copy_img = True, copy_json = True)   
    
    #%%
#change here!!
copy_img = True #True
copy_json = True
train_prop = 0.7 # todo [0:73]
val_prop= 0.25
#testprop = 0.1
soiltypes_to_detect = 'all' #'Feinsand'  # all, Feinsand, Klei, 
#%%
# add the filename of all VIA2 projects
# Note: all VIA projects should have same attributes and project settings

#root_project_path =r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\phase_2\snipped_img\snipped_sign' #'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\Soil_Classification\dataset_train_till_IMG_5203BKF 38_4' #'C:\Users\sven\Desktop\Masterthesis\github\data\vgg_annotation\img_horizontal\new_train_02'
#all_img_json_folder = 'RGB' #'all_img_train_val_and_json'
root_project_path = raw_Data_folder_path
# load json of all images
path_filename_json = os.path.join(root_project_path,filename_json) #'changed_json.json') #via_project_merged.json')
# copy attributes and other project settings from one of the projects
# assumption: all the projects have same attributes and settings
via2 = {}
with open(path_filename_json, 'r') as f:
  via2 = json.load(f)
 
  #%%
data_keys_json = list(via2.keys()) 
if soiltypes_to_detect == 'Feinsand':
    data_new2 = via2               
    data_keys_json2 = list(data_new2.keys())
    
    for key in data_keys_json2:
        no_region_counter = 0
        region_remove = []
        for idx_regions, regions_i in enumerate(data_new2[key]['regions']):
            #print(len(regions_i['region_attributes']))
            if len(regions_i['region_attributes']) == 0:
                print(key)
                print('jooooo')
                no_region_counter = 1
            else:
                soiltype = regions_i['region_attributes']['soiltype']
#                print(soiltype)
#                print('okkkkkk')
                if soiltype != 5 : #5 for Feinsand
                    print(idx_regions)
                    region_remove.append(idx_regions)
#                else:
#                    print('not in class')
#                region_counter = region_counter + 1
        if no_region_counter == 0:
            for i_remove in sorted(region_remove, reverse=True):
#                print(data_new2[key]['regions'][i_remove])
                del data_new2[key]['regions'][i_remove]
#%%
#seperate json
data_keys_json_train_val_test = []       
data_keys_json_train = data_keys_json[0: int(train_prop * np.size(data_keys_json))]
data_keys_json_val = data_keys_json[int(train_prop * np.size(data_keys_json)):int(train_prop * np.size(data_keys_json))+ int(val_prop * np.size(data_keys_json))]
data_keys_json_test = data_keys_json[int(train_prop * np.size(data_keys_json))+ int(val_prop * np.size(data_keys_json)):]
data_keys_json_train_val_test = [data_keys_json_train, data_keys_json_val, data_keys_json_test]

via2_split = []
if soiltypes_to_detect == 'all':
    via2_train = dict((k,via2[k]) for k in data_keys_json_train)
    via2_val = dict((k,via2[k]) for k in data_keys_json_val)
    via2_test = dict((k,via2[k]) for k in data_keys_json_test)

elif soiltypes_to_detect == 'Feinsand':
    via2_train = dict((k,data_new2[k]) for k in data_keys_json_train)
    via2_val = dict((k,data_new2[k]) for k in data_keys_json_val)
    via2_test = dict((k,via2[k]) for k in data_keys_json_test)
via2_split[via2_train, via2_val, via2_test ]
    #%%
#copy images to train, val and test folder

# define the name of the directory to be created
train_val_test= ['train', 'val', 'test']
path_train_val_test = os.path.join(new_Dataset_path,train_val_test[0])
if os.path.exists(path_train_val_test):
    shutil.rmtree(path_train_val_test)
    os.mkdir(path_train_val_test)
else:
    os.mkdir(path_train_val_test)
    
if copy_img:
    for i in data_keys_json_train_val_test[0]:
        img_filename = via2_split[0][i]['filename'] 
        src = os.path.join(root_project_path,img_filename)
        dst = path_train_val_test[0]
        shutil.copy(src,dst)    
new_splited_json_all = ['via_train.json', 'via_val.json', 'via_test.json']   
new_splited_json_Feinsand = ['via_train_Feinsand.json', 'via_test_Feinsand.json', 'via_test_Feinsand.json']
if copy_json:
    if soiltypes_to_detect == 'all':
        output_filename = os.path.join(path_train,new_splited_json_all[0])
    elif soiltypes_to_detect == 'Feinsand':
        output_filename = os.path.join(path_train,new_splited_json_Feinsand[0])
    with open(output_filename, 'w') as fout:
      json.dump(via2_split[0], fout)    
    #%%
    
    

path_val = os.path.join(new_Dataset_path,'val')
path_test = os.path.join(new_Dataset_path,'test')

if os.path.exists(path_train):
    shutil.rmtree(path_train)
    os.mkdir(path_train)
else:
    os.mkdir(path_train)
if os.path.exists(path_val):  
    shutil.rmtree(path_val)     
    os.mkdir(path_val)
else:
    os.mkdir(path_val)
if os.path.exists(path_test): 
    shutil.rmtree(path_test)      
    os.mkdir(path_test)
else:
    os.mkdir(path_test)
    
if copy_img:
    for i in data_keys_json_train:
        img_filename_train = via2_train[i]['filename'] 
        src = os.path.join(root_project_path,img_filename_train)
        dst = os.path.join(path_train,img_filename_train) #all_img_json_folder
        shutil.copy(src,path_train)
    for i in data_keys_json_val:
        img_filename_val = via2_val[i]['filename']
        src = os.path.join(root_project_path,img_filename_val)
        dst = os.path.join(path_val,img_filename_val)
        shutil.copy(src,path_val)
    for i in data_keys_json_test:
        img_filename_test = via2_test[i]['filename']
        src = os.path.join(root_project_path,img_filename_test)
        dst = os.path.join(path_test,img_filename_test)
        shutil.copy(src,path_test)
        
if copy_json:
    if soiltypes_to_detect == 'all':
        output_filename_train = os.path.join(path_train,'via_train.json')
    elif soiltypes_to_detect == 'Feinsand':
        output_filename_train = os.path.join(path_train,'via_train_Feinsand.json')
    with open(output_filename_train, 'w') as fout_train:
      json.dump(via2_train, fout_train)

    if soiltypes_to_detect == 'all':
        output_filename_val = os.path.join(path_val,'via_val.json')
    elif soiltypes_to_detect == 'Feinsand': 
        output_filename_val = os.path.join(path_val,'via_val_Feinsand.json')
    with open(output_filename_val, 'w') as fout_val:
      json.dump(via2_val, fout_val)
      
    if soiltypes_to_detect == 'all':
        output_filename_test = os.path.join(path_test,'via_test.json')
    elif soiltypes_to_detect == 'Feinsand': 
        output_filename_test = os.path.join(path_test,'via_test_Feinsand.json')
    with open(output_filename_test, 'w') as fout_test:
      json.dump(via2_test, fout_test)
      
#%%
