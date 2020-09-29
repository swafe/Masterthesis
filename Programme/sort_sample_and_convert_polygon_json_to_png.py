# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 11:12:38 2020

@author: sven
This script creates

    a new sorted json file, where the regions are sorted from top to bottom and
    cuts the detected regions from the original image and saves as e new cutted image. The new filename consists of the filename( image number, 'BKF', sample mumber/location) and sample id


"""
import shutil
import os

import numpy as np
import json 

from PIL import Image, ImageDraw
#%%
#falls git existiert löschen
git_data = False
local_data = True

if git_data:
    path_data = '/content/data'
    if os.path.exists(path_data):
      print('g')
      shutil.rmtree(path_data)
      #os.remove(path_data)
    #!git clone https://github.com/swafe/data.git
if local_data:
    path_data = r'C:\Users\sven\Desktop\Masterthesis\github\data'



#%%
# some Methods

def get_access_to_json(image_path):
  image_name = os.path.splitext(os.path.basename(image_path))[0]
  filename = os.path.basename(image_path)
  img_size =  os.path.getsize(image_path)
  filename_and_size = filename + str(img_size)
  return filename_and_size, filename

# Iterating through the json 
# list 
def get_points_label_from_json_as_array(data, image_path):
  detected = []
  sample_id = []
  countsigns = 0
  countsample = 0
  filename_and_size, filename = get_access_to_json(image_path)
  for i_data_regions in data[filename_and_size]['regions']: #[filename_and_size]: 
    # print(i)
    points_x = i_data_regions['shape_attributes']['all_points_x']
    points_y = i_data_regions['shape_attributes']['all_points_y']
    sample_id_i = i_data_regions["region_attributes"] ["sample"]
    # # für ImageDraw.Draw tuple erforderlich
    points =[]
    for i in range(0,len(points_x)):
      points_i = (points_x[i],points_y[i])
      points.append(points_i)

    detected.append(points)
    sample_id.append(sample_id_i)
    
    # count signs and samples
    
    if i_data_regions['region_attributes']['sample'][0] == 'sample':
        countsample = countsample +1
    elif i_data_regions['region_attributes']['sample'][0] == 'sign':
        countsigns = countsigns+1
    
  return detected, filename_and_size, filename, sample_id, countsample, countsigns  


#%%
# Python program to read json file 
# change here !!!!!!
path_test_in_data = r'vgg_annotation/img_horizontal/project_9091/all_img_train_val_and_json'
path_test_dir = os.path.join(path_data,path_test_in_data)
json_name = 'regions_and sign2.json'  #'via_project_merged.json'
json_file_dir = os.path.join(path_test_dir, json_name) 

#get all images in path_test_dir
image_paths = []
for filename in sorted(os.listdir(path_test_dir), key=str.lower):
    if os.path.splitext(filename)[1].lower() in ['.png', '.jpg', '.jpeg']:
      image_paths.append(os.path.join(path_test_dir, filename))
# Opening JSON file 
f = open(json_file_dir) 
# returns JSON object as a dictionary 
data = json.load(f) 
# Closing file 
f.close() 

#sorting regions in json from upside to bottom
# https://stackoverflow.com/questions/26924812/python-sort-list-of-json-by-value
# Sorting objects doesn't make sense since object keys have no positional value. 

# // First create the array of keys/net_total so that we can sort it:
#store
data_sorted = data
# i= 1
# image_path = image_paths[i]
for path_i in image_paths:
#path_i = image_paths[2]


  ## get points_x_all, points_y_all, sample_id
  sample_id = []
  points_x_all = []
  points_y_all = []
  points_x_all_sign = []
  points_y_all_sign = []
  
  regions_all=[]
  # labels = []
  filename_and_size, filename = get_access_to_json(path_i)

  for i in data_sorted[filename_and_size]['regions']: #[filename_and_size]: 
      regions_all.append(i)
  #    print(len(regions_all))
       
      

  for i_regions in regions_all:
      sample_name_i = i_regions['region_attributes']['sample']
      points_x = 0
      points_y = 0
      if sample_name_i == 'sample':
          
          if i_regions['shape_attributes']['name'] == 'polygon':
            points_x =  i_regions['shape_attributes']['all_points_x']
            points_y =  i_regions['shape_attributes']['all_points_y']
            
            points_x_all.append(points_x)
            points_y_all.append(points_y)
          elif i_regions['shape_attributes']['name'] == 'rect':
            x1 = i_regions['shape_attributes']['x']
            y1 = i_regions['shape_attributes']['y']
            width = i_regions['shape_attributes']['width']
            height = i_regions['shape_attributes']['height']
            x2 = x1 + width
            y2 = y1 + height
            points_x = [x1, x2, x2, x1]
            points_y = [y1, y1, y2, y2]
            
            points_x_all.append(points_x)
            points_y_all.append(points_y)
      elif sample_name_i == 'sign':
      
          if i_regions['shape_attributes']['name'] == 'polygon':
            points_x =  i_regions['shape_attributes']['all_points_x']
            points_y =  i_regions['shape_attributes']['all_points_y']
            
            points_x_all.append(points_x)
            points_y_all.append(points_y)
          elif i_regions['shape_attributes']['name'] == 'rect':
            x1 = i_regions['shape_attributes']['x']
            y1 = i_regions['shape_attributes']['y']
            width = i_regions['shape_attributes']['width']
            height = i_regions['shape_attributes']['height']
            x2 = x1 + width
            y2 = y1 + height
            points_x = [x1, x2, x2, x1]
            points_y = [y1, y1, y2, y2]
            
            points_x_all_sign.append(points_x)
            points_y_all_sign.append(points_y)
           
            
      
  ##
  # // Now sort it:

  points_y_all_first = []
  for i_y in points_y_all:
    points_y_all_first_i = i_y[0]
    points_y_all_first.append(points_y_all_first_i)
  
  points_y_all_first_sign = []
  for i_y_sign in points_y_all_sign:
    points_y_all_first_sign_i = i_y_sign[0]
    points_y_all_first_sign.append(points_y_all_first_sign_i)  



  sort_index_min_to_max = np.argsort(points_y_all_first)#[::-1]
  sort_index_min_to_max_sign = np.argsort(points_y_all_first_sign)
  #print(sort_index_min_to_max)
  # create regions with new values
  regions_mask_rois_adapted = []
  regions_mask_rois_adapted_sign = []
  
  print(filename)
  i_sample = 0
  for i_sort in sort_index_min_to_max:
    sample_name = ['sample',int(i_sample)]
    print(sample_name)
    regions_i_adapted = {"shape_attributes": {
                                  "name": "polygon",
                                  "all_points_x": points_x_all[i_sort], 
                                  "all_points_y": points_y_all[i_sort] },
                                  "region_attributes": { "sample": sample_name}}        
    regions_mask_rois_adapted.append(regions_i_adapted)
    i_sample = i_sample + 1
    
  i_sample_sign = 0
  for i_sort_sign in sort_index_min_to_max_sign:
    sample_name_sign = ['sign',int(i_sample_sign)]
    print(sample_name_sign)
    regions_i_adapted_sign = {"shape_attributes": {
                                  "name": "polygon",
                                  "all_points_x": points_x_all_sign[i_sort_sign], 
                                  "all_points_y": points_y_all_sign[i_sort_sign] },
                                  "region_attributes": { "sample": sample_name_sign}}        
    regions_mask_rois_adapted.append(regions_i_adapted_sign)
    i_sample_sign = i_sample_sign + 1
  # annotation_json_via_format_rois_mask_adapted_i = {
  #                   "filename": filename, 
  #                   "size": img_size, 
  #                   "regions": regions_mask_rois_adapted,
  #                   "file_attributes": {}
  #                   }
  # update json with new regions
  # annotation_json_via_format.update({filename_and_size : annotation_json_via_format_rois_mask_adapted_i})
#      regions_mask_rois_adapted.append(regions_mask_rois_adapted_sign)
  data_sorted.update({filename_and_size:{"regions":regions_mask_rois_adapted}})
# save annotation as json
if True:
  path_result_masks_data_sorted = os.path.join(path_test_dir,'result_masks_data_sorted.json' ) 
  with open(path_result_masks_data_sorted, 'w') as fp:
      json.dump(data_sorted, fp)

#%%
google_drive = False
if google_drive:
    #Connect to google drive to load weights from '.h5'-file. '.h5'file is to big to store in github
    from google.colab import drive
    drive.mount('/content/drive')

#%%
path_snip_ohne_sign_all = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\snipped_ohne_sign_all'
#path_snip_ohne_sign = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\snipped_ohne_sign'#'/content/drive/My Drive/Colab/snipped'
path_snip_sign = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\snipped_sign'
#os.mkdir(path_snip)


#%%
#  MAIN

#%%
# cutting detected images 
# https://stackoverflow.com/questions/22588074/polygon-crop-clip-using-python-pil

# read image as RGB and add alpha (transparency)
#I added a section in the wiki about training with images of different channel size (e.g. Graysclae or RGBD). If I missed something, please let me know.
#https://github.com/matterport/Mask_RCNN/wiki

### path_snip_ohne_sign_all for later classification, use change_json_key.py to edit key names
for path_i in image_paths:
  im = Image.open(path_i).convert("RGBA")
  im = Image.open(path_i).convert("RGB") #"RGBA"
  # convert to numpy (for convenience)
  imArray = np.asarray(im)
  # create mask
  detected, filename_and_size, filename_jpg, sample_id, countsample, countsigns = get_points_label_from_json_as_array(data_sorted, path_i)
  print(countsample, countsigns)
  if True:
      for i_sample in range(countsample):
          
          polygon = detected[i_sample]
          sample_id_i = sample_id[i_sample][1]
          #print(polygon)
          maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
          ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
          mask = np.array(maskIm)
          # assemble new image (uint8: 0-255)
          newImArray = np.empty(imArray.shape,dtype='uint8')   
          #colors (three first columns, RGB)
          newImArray[:,:,:3] = imArray[:,:,:3]  
          #transparency (4th column)
#          newImArray[:,:,3] = mask*255
          #back to Image from numpy
#          newIm = Image.fromarray(newImArray, "RGBA")  
          newIm = Image.fromarray(newImArray, "RGB")  #'RGBA'
          #save snipped image with name of originimage plus index
          filename = os.path.splitext(filename_jpg)
          if True: # True False
              path = path_snip_ohne_sign_all #'/content/drive/My Drive/Colab/snipped' #'/content/snipped_img'
              if not os.path.exists(path):
                  os.makedirs(path)
              newIm.save("%s/%s_%s.png"%(path,filename[0],sample_id_i))
              print(filename[0],sample_id_i)
            
#%%  
#### path_snip_sign, devide into countsample != countsigns(shows all signs) and countsample == countsigns (shows only related sign)
for path_i in image_paths:
  im = Image.open(path_i).convert("RGBA")
  # convert to numpy (for convenience)
  imArray = np.asarray(im)
  # create mask
  detected, filename_and_size, filename_jpg, sample_id, countsample, countsigns = get_points_label_from_json_as_array(data_sorted, path_i)
  print(countsample, countsigns)
  if countsample != countsigns:
      print(filename_jpg)
      filename_countsample_no_countsigns = filename_jpg
      for i_sample in range(countsample):
          polygon = detected[i_sample]
          polygon_sign = []
          for i in range(countsample, countsample + countsigns):
                         polygon_sign_i = detected[i] 
                         polygon_sign.append(polygon_sign_i)
          sample_id_i = sample_id[i_sample][1]
          #print(polygon)
          
          maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
          ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
          for countsigns_i in range(0,countsigns):
              ImageDraw.Draw(maskIm).polygon(polygon_sign[countsigns_i], outline=1, fill=1)
          mask = np.array(maskIm)
          #assemble new image (uint8: 0-255)
          newImArray = np.empty(imArray.shape,dtype='uint8')
          #colors (three first columns, RGB)
          newImArray[:,:,:3] = imArray[:,:,:3]
          #transparency (4th column)
          newImArray[:,:,3] = mask*255
          #back to Image from numpy
          newIm = Image.fromarray(newImArray, "RGBA")
          #save snipped image with name of originimage plus index
          filename = os.path.splitext(filename_jpg)
          if True: # True False
              path = path_snip_sign #'/content/drive/My Drive/Colab/snipped' #'/content/snipped_img'
              if not os.path.exists(path):
                  os.makedirs(path)
              newIm.save("%s/%s_%s.png"%(path,filename[0],sample_id_i))
              print(filename[0],sample_id_i)
  elif countsample == countsigns:
      for i_sample in range(countsample):
          polygon = detected[i_sample]
          polygon_sign =detected[countsample + i_sample] 
          sample_id_i = sample_id[i_sample][1]
          #print(polygon)
          
          maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
          ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
          ImageDraw.Draw(maskIm).polygon(polygon_sign, outline=1, fill=1)
          mask = np.array(maskIm)
          #assemble new image (uint8: 0-255)
          newImArray = np.empty(imArray.shape,dtype='uint8')
          #colors (three first columns, RGB)
          newImArray[:,:,:3] = imArray[:,:,:3]
          #transparency (4th column)
          newImArray[:,:,3] = mask*255
          #back to Image from numpy
          newIm = Image.fromarray(newImArray, "RGBA")
          #save snipped image with name of originimage plus index
          filename = os.path.splitext(filename_jpg)
          if True: # True False
              path = path_snip_sign #'/content/drive/My Drive/Colab/snipped' #'/content/snipped_img'
              if not os.path.exists(path):
                  os.makedirs(path)
              newIm.save("%s/%s_%s.png"%(path,filename[0],sample_id_i))
              print(filename[0],sample_id_i)
  
    
    
    
    
    
    
    
    
# eigentlich nicht erforderlich       
#          maskIm_sample = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
#          ImageDraw.Draw(maskIm_sample).polygon(polygon, outline=1, fill=1)
#          mask_sample = np.array(maskIm_sample)
#          #assemble new image (uint8: 0-255)
#          newImArray_sample = np.empty(imArray.shape,dtype='uint8')
#          #colors (three first columns, RGB)
#          newImArray_sample[:,:,:3] = imArray[:,:,:3]
#          #transparency (4th column)
#          newImArray_sample[:,:,3] = mask_sample*255
#          #back to Image from numpy
#          newIm_sample = Image.fromarray(newImArray_sample, "RGBA")
#          #save snipped image with name of originimage plus index
#          filename = os.path.splitext(filename_jpg)
#          if True: # True False
#              path = path_snip_ohne_sign #'/content/drive/My Drive/Colab/snipped' #'/content/snipped_img'
#              if not os.path.exists(path):
#                  os.makedirs(path)
#              newIm_sample.save("%s/%s_%s.png"%(path,filename[0],sample_id_i))
#              print(filename[0],sample_id_i)
                  
#  #save snipped images in folder strukture, where snipped images are stored in folder named as origin image
#  if False: # True False
#      path = '/content/snipped_img/%s'%(filename_jpg)
#      print(path)
#      if not os.path.exists(path):
#          os.makedirs(path)
#          newIm.save("%s/%s.png"%(path,i)) 
#  #save snipped image with name of originimage plus index
#  filename = os.path.splitext(filename_jpg)
#  if True: # True False
#      path = path_snip #'/content/drive/My Drive/Colab/snipped' #'/content/snipped_img'
#      if not os.path.exists(path):
#          os.makedirs(path)
#          newIm.save("%s/%s_%s.png"%(path,filename[0],sample_id_i))
#      print(filename[0],sample_id_i)
#
              
              
              
              
              
              
              
              
              
    #%% convert RGBA to RGB 
#https://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil/9459208
from PIL import Image
import os 
import numpy as np
img_RGBA_folder_path = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\Soil_Classification\val01'
img_RGB_folder_path = r'E:\Datasets_GGU_Bodenproben\Bodenproben_recognition\snipped_img\Soil_Classification\val01\RGB'
if not os.path.exists(img_RGB_folder_path):
    os.mkdir(img_RGB_folder_path)
image_paths = []
for filename in sorted(os.listdir(img_RGBA_folder_path), key=str.lower):
    if os.path.splitext(filename)[1].lower() in ['.png', '.jpg', '.jpeg']:
      image_paths.append(os.path.join(img_RGBA_folder_path, filename))
      
for path_i in image_paths:
    png = Image.open(path_i)
    print(np.shape(png))
    png.load() # required for png.split()
    
    background = Image.new("RGB", png.size, (255, 255, 255))
    background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
    print(np.shape(background))
    img_filename = os.path.basename(path_i)
  
    image_save_path = os.path.join(img_RGB_folder_path,img_filename)  
    background.save(image_save_path, 'PNG') #, quality=80)
print('süper')
  
      
      
      
      
      
      
      