#%%
import os
import pandas as pd
import csv
import numpy as np
import shutil
import io

#%%
def get_seperater(profil_bop):
    # check if '1.0000 # 5 # ' is in bop-file, otherwise add in layer_seperater
  layer_seperater = [['1.0000 # 5 # '], ['1.0000 # 6 # ']]
  count_matches = 0                   
  for elem in layer_seperater:
     if elem in profil_bop:
         count_matches = count_matches + 1
         match_layer_seperater = elem
  if count_matches != 1:
     print('Achtung: no or double match of 1.0000 #...#')  
  return(match_layer_seperater)
    
#%%
def reduce_Bohrung_from_profil_bop(profil_bop, name_Bohrung):

  #find index of '1.0000 # 5 # ' and '0' in txt
  start_Bohrung = np.array([i for i,x in enumerate(profil_bop) if x ==[name_Bohrung] ])

  # find '1.0000 # 5 # '
                
  new_layer_index_in_txt = np.array([i for i,x in enumerate(profil_bop) if x ==match_layer_seperater ])
  # find line for "number of Layers"
  number_Layers_index_in_txt = new_layer_index_in_txt[np.where(new_layer_index_in_txt > start_Bohrung)[0][0]]

  #filter info of number of Layers from line
  number_of_Layers = profil_bop[number_Layers_index_in_txt-1][0].split(' ')[0]
  print(number_of_Layers)
  #find end

  # index of n (number of Layers) of '1.0000 # 5 # ' after 'name_Bohrung)
  last_Layer_index_in_txt = new_layer_index_in_txt[np.where(new_layer_index_in_txt > start_Bohrung)[0][int(number_of_Layers)-1]]
  #print(profil_bop[last_Layer_index_in_txt])

  zero_index_in_txt = np.array([i for i,x in enumerate(profil_bop) if x ==['0'] ])
  end_of_Layer = zero_index_in_txt[np.where(zero_index_in_txt> last_Layer_index_in_txt)[0][0]]
  profil_bop_red_start_to_end_layer = profil_bop[int(start_Bohrung):end_of_Layer+1] 
  return profil_bop_red_start_to_end_layer 
#%%

def soiltype_and_depth_for_Layers(profil_bop_red_start_to_end_layer):
  #prepare Layer indices for '1.0000 # 5 # ' to start Layer and '0' to end of Layer

  #find index of '1.0000 # 5 # ' and '0' in txt
  new_layer_index_in_txt = np.array([i for i,x in enumerate(profil_bop_red_start_to_end_layer) if x ==match_layer_seperater ])
  zero_index_in_txt = np.array([i for i,x in enumerate(profil_bop_red_start_to_end_layer) if x ==['         0'] ])
  #filter index of '0' after '1.0000 # 5 # '
  zero_after_Layer_index = []
  for i in new_layer_index_in_txt:
    zero_after_Layer_index.append(zero_index_in_txt[np.where(zero_index_in_txt> i)[0][0]])

  #store all info of Layers from '1.0000 # 5 # ' to '0'
  Layers_all_info = []
  for i,j in zip(new_layer_index_in_txt, zero_after_Layer_index):
    Layer_i = np.array(profil_bop_red_start_to_end_layer[i:j])
    Layers_all_info.append(Layer_i)

  #filter info of Soil type and depth of Layers
  Layers_soil_depth = []
  for i in Layers_all_info:
    n = 1
    if len(i[-n])>1:
      depth_i = i[-n][0] +','+i[-n][1]
    else:
      depth_i = i[-n][0]

    depth_i = depth_i.split('/')[0]
    #Soil type and depth
    Layers_soil_depth_i = [i[1], depth_i]
    Layers_soil_depth.append(Layers_soil_depth_i)
  #print(Layers_soil_depth[0:5])
  return(Layers_soil_depth)

#%%
# change this 
name_Bohrung = 'BKF 5' # B 3 

#file_path_ansi = 'Anlage 2.1 Bodenprofil 1.bop' #"input.txt"
file_path_ansi = r'E:\Datasets_GGU_Bodenproben_orig\9091_\Input\Eigenschaften\9091.3 Bericht Baugrund\Anlagen 2 bopo\Anlage 2.5 BKF 5.bop' 
#file_path_ansi = r'E:\Datasets_GGU_Bodenproben_orig\9091_\Input\Eigenschaften\9091.3 Bericht Baugrund\Anlagen 2 bopo\Anlage 2.6 Bodenprofil 6.bop' #"input.txt"
file_path_utf8 = r'C:\Users\sven\Desktop\get_typ_depth_bop\output.txt'
if not os.path.exists(file_path_utf8):
    with io.open(file_path_ansi, encoding='latin-1', errors='ignore') as source:
        with io.open(file_path_utf8, mode='w', encoding='utf-8') as target:
            shutil.copyfileobj(source, target)

with open(file_path_utf8, newline='') as inputfile:
  profil_bop = list(csv.reader(inputfile)) 
match_layer_seperater = get_seperater(profil_bop)
B_1 = reduce_Bohrung_from_profil_bop(profil_bop, name_Bohrung)
B_1_save =B_1
B_1_Layers = soiltype_and_depth_for_Layers(B_1)
print(B_1_Layers)

with open(r'C:\Users\sven\Desktop\get_typ_depth_bop\typ_depth_output\f1.csv', "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(B_1_Layers)







# %%
