import pandas as pd
import shutil
import os
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
from tqdm import tqdm

path_file_csv = f"Dataof/labels_my-project-name_2023-03-22-11-12-24.csv"
name_image_background = "image_convert3.jpg"
# name_image_bone = "1gfg1_0.png"
# name_image_out = "rocket_pillow_paste.png"
path_folder_output = "Output"

ratio = 0.5

list_columns_name =["label_name", "bbox_x", "bbox_y", "bbox_width", "bbox_height", "image_name", "image_width", "image_height", "label_shape"] 
dict_columns_value = {x:[] for x in list_columns_name}
list_position_background = []
df = pd.read_csv(path_file_csv)
for i in range(df.shape[0]):
    x, y, w, h = df["bbox_x"].iloc[i], df["bbox_y"].iloc[i], df["bbox_width"].iloc[i], df["bbox_height"].iloc[i]
    list_position_background.append([int(x+w/2), int(y+h/2), w, h])

path_result = "Result" 
name_image = "images"
name_label = "labels"

if os.path.exists(path_result):
    shutil.rmtree(path_result)

for name in tqdm(os.listdir(path_folder_output)):
    dict_columns_value = {x:[] for x in list_columns_name}
    if not os.path.exists(os.path.join(path_result, name, name_image )):
        os.makedirs(os.path.join(path_result, name, name_image ))
        os.makedirs(os.path.join(path_result, name, name_label ))
    im1 = Image.open(f'background/{name_image_background}')
    for fileout_path_image in os.listdir(os.path.join(path_folder_output, name)):
        im2 = Image.open(os.path.join(path_folder_output, name,fileout_path_image))
        back_im = im1.copy()
        name_out = fileout_path_image.split(".")[0]
        for idx in list_position_background: 
            dict_columns_value["label_name"].append(name_out)
            imA = im2.copy()
            width, height = imA.size
            scale_w = width/ (ratio*idx[2])
            scale_h = height/ (ratio*idx[3])
            if height/scale_w > idx[3]:
                scale_a = scale_h
            else:
                scale_a = scale_w
   
            imA = imA.resize((int(width/scale_a), int(height/scale_a)))
            imA = imA.convert("RGBA")
            w, h = imA.size
            back_im.paste(imA, (idx[0]-int(w/2), idx[1]-int(h/2)), imA)
            dict_columns_value["bbox_x"].append(idx[0]-int(w/2))
            dict_columns_value["bbox_y"].append(idx[1]-int(h/2))
            dict_columns_value["bbox_width"].append(w)
            dict_columns_value["bbox_height"].append(h)
            dict_columns_value["image_name"].append(f"{name_out}.png")
            dict_columns_value["image_width"].append(im1.size[0])
            dict_columns_value["image_height"].append(im1.size[1]) 
            dict_columns_value["label_shape"].append(name)
        back_im.save(f"{path_result}/{name}/{name_image}/{name_out}.png", quality=95, format="png")
    pd.DataFrame(dict_columns_value).to_csv(f"{path_result}/{name}/{name_label}/label_{name}.csv", index=False)