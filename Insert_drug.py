import pandas as pd
import shutil
import os
from PIL import Image
from tqdm import tqdm


def remove_insertfolder(path_result, condition=True):
    """
    Target: Remove folders
    """
    if condition:
        if os.path.exists(path_result):
            shutil.rmtree(path_result)

def processing_insert(name_image_background, 
                      name_backg,
                      path_folder_output,
                      path_result,
                      name_image,
                      name_label,
                      list_position_background,
                      ratio = 0.5):
    list_columns_name =["label_name", "bbox_x", "bbox_y", "bbox_width", "bbox_height", "image_name", "image_width", "image_height", "label_shape"] 
    dict_columns_value = {x:[] for x in list_columns_name}
    for name in tqdm(os.listdir(path_folder_output)):
        dict_columns_value = {x:[] for x in list_columns_name}
        if not os.path.exists(os.path.join(path_result, name, name_image )):
            os.makedirs(os.path.join(path_result, name, name_image ))
            os.makedirs(os.path.join(path_result, name, name_label ))
        im1 = Image.open(name_image_background)
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
                dict_columns_value["image_name"].append(f"{name_backg}_{name_out}.png")
                dict_columns_value["image_width"].append(im1.size[0])
                dict_columns_value["image_height"].append(im1.size[1]) 
                dict_columns_value["label_shape"].append(name)
            back_im.save(f"{path_result}/{name}/{name_image}/{name_backg}_{name_out}.png", quality=95, format="png")
        pd.DataFrame(dict_columns_value).to_csv(f"{path_result}/{name}/{name_label}/label_{name_backg}_{name}.csv", index=False)

def background_folder(background_path, path_folder_output, path_result, name_image, name_label, ratio = 0.5):
    for i in range(1, 5):
        path_file_csv = f"{background_path}/image_convert{i}.csv"
        name_image_background = f"{background_path}/image_convert{i}.jpg"
        name_backg = f"image_convert{i}"
        list_position_background = []
        df = pd.read_csv(path_file_csv)
        for i in range(df.shape[0]):
            x, y, w, h = df["bbox_x"].iloc[i], df["bbox_y"].iloc[i], df["bbox_width"].iloc[i], df["bbox_height"].iloc[i]
            list_position_background.append([int(x+w/2), int(y+h/2), w, h])
        processing_insert(name_image_background, 
                        name_backg,
                        path_folder_output,
                        path_result,
                        name_image,
                        name_label,
                        list_position_background,
                        ratio = 0.5)
def main():
    path_result = "Result" 
    name_image = "images"
    name_label = "labels"
    path_folder_output = "Output"
    background_path = "Background"
    remove_insertfolder(path_result, condition=True)
    background_folder(background_path, 
                      path_folder_output, 
                      path_result, 
                      name_image, 
                      name_label, 
                      ratio = 0.5)

if __name__=="__main__":
    main()