# Convert csv to yolo format
import os
import pandas  as pd
from tqdm import trange, tqdm

def coco_to_yolo(x1, y1, w, h, image_w, image_h):
    return ((2*x1 + w)/(2*image_w)) , ((2*y1 + h)/(2*image_h)), w/image_w, h/image_h

def yolobbox2bbox(x,y,w,h):
    x1, y1 = x-w/2, y-h/2
    x2, y2 = x+w/2, y+h/2
    return x1, y1, x2, y2

def main():
    path_result = "Result" 
    name_label = "labels"
    path_label_ima1 = "Image1" 

    sort_ls_name = [x for x in os.listdir(path_label_ima1)]
    sort_ls_name.sort()
    d_nametonum = {}
    d_numtoname = {}
    for i, x in enumerate(sort_ls_name):
        d_nametonum[str(x)] = str(i)
        d_numtoname[str(i)] = str(x)
    list_result = os.listdir(path_result)
    for name in tqdm(list_result):
        for name_csv in os.listdir(os.path.join(path_result, name, name_label)):
            if name_csv.endswith(".csv"):
                df = pd.read_csv(os.path.join(path_result, name, name_label, name_csv), index_col=None)
                for i in trange(df.shape[0]):
                    image_w, image_h = df["image_width"].iloc[i], df["image_height"].iloc[i]
                    x, y, w, h = df["bbox_x"].iloc[i], df["bbox_y"].iloc[i], df["bbox_width"].iloc[i], df["bbox_height"].iloc[i]
                    x1, y1, x2, y2 = coco_to_yolo(x, y, w, h, image_w, image_h)
                    name_label_dir = df["label_shape"].iloc[i]
                    name_text = df["image_name"].iloc[i].split(".png")[0]
                    with open(f"{path_result}/{name_label_dir}/{name_label}/{name_text}.txt", "+a") as f:
                        f.write(f"{d_nametonum[str(name_label_dir)]}\t{round(x1,5)}\t{round(y1,5)}\t{round(x2,5)}\t{round(y2,5)}\n")
                        f.close()  

if __name__=="__main__":
    main()