# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 15:16:30 2020

@author: sven
"""
from xml.dom import minidom
import pandas as pd
import os
import csv
#%%


def convert_xml_to_List(xml_doc):
    items_SoilLayer = xml_doc.getElementsByTagName('SoilLayer')
    print('%i Soillayer:' % items_SoilLayer.length)
    Layer_depths = []
    for depth in items_SoilLayer:    
        depth_i = depth.getAttribute('depth')
        Layer_depths.append(depth_i)
    Soil_infos = []
    for info in items_SoilLayer:
        info_i = info.getAttribute('info')
        Soil_infos.append([info_i])
    Layer_depths_and_info_list = [Layer_depths, Soil_infos]
    return Layer_depths_and_info_list
#%%
## change paths
rootdir = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\8205_1\xml_to_csv\bop'

dst_folder_csv = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\8205_1\xml_to_csv'
path_xml_csv_extension = os.path.join(dst_folder_csv,'xml_to_csv_8205_1.csv')

number_xml = 0
with open(path_xml_csv_extension, "w", newline="") as f:
    #check if JPG and get folder name for copied img 
    for subdir, dirs, files_unsorted in os.walk(rootdir):
    #    files_all.append(files)
    #    dirs_all.append(dirs)
#        print(files_unsorted[0])
#        files = sorted(files_unsorted, key=lambda s: s[-5])
        for file in files_unsorted:
            number_xml = number_xml + 1
            path_file_xml = os.path.join(subdir,file)
            split_path_file_img_and_extension = os.path.splitext(path_file_xml)
            #        file_all2.append(file)
            if (split_path_file_img_and_extension[1] == '.xml'):
    #            split_path_file_img_and_extension_sum.append(split_path_file_img_and_extension[1])
    #            get_name_from_copied_folder = ntpath.basename(subdir)
    #            filename_with_foldername_path = split_path_file_img_and_extension[0]+ get_name_from_copied_folder+ split_path_file_img_and_extension[1]
                
                path_file_xml
                #path_file_xml = r'C:\Users\sven\Desktop\Anlage 2.5 BKF 5.xml'
                xml_doc = minidom.parse(path_file_xml)
                Layer_depths_and_info_list = convert_xml_to_List(xml_doc)
                
                split_path_file_img_and_extension = os.path.splitext(path_file_xml)
                csv_file = split_path_file_img_and_extension[0] + '.csv'
                basename_path_file_csv = os.path.basename(csv_file)
                print(basename_path_file_csv)
    #            path_xml_csv_extension = os.path.join(dst_folder_csv, basename_path_file_csv) # + split_path_file_img_and_extension[0] + '.csv'
    
    #            path_xml_csv_extension = os.path.join(dst_folder_csv,'xml_to_csv_8205_1.csv')
    #            if True: #True False
    #                with open(path_xml_csv_extension, "w", newline="") as f:
                if True: #True False            
                    writer = csv.writer(f)
                    writer.writerow([basename_path_file_csv])
                    writer.writerows(Layer_depths_and_info_list)
                    
                                 

#%%

