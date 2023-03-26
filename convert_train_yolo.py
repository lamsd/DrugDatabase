import os
import shutil
from tqdm import tqdm

ratios = 0.3

def main():
    path_roots = "Result"
    path_image = "images" 
    path_label = "labels"
    path_train = "train"
    path_test = "test"
    path_out = "Datatrain"
    if  os.path.exists(path_out):
        shutil.rmtree(path_out)
    if not os.path.exists(os.path.join(path_out, path_train, path_image)):
        os.makedirs(os.path.join(path_out, path_train, path_image))
        os.makedirs(os.path.join(path_out, path_train, path_label))
        os.makedirs(os.path.join(path_out, path_test, path_image))
        os.makedirs(os.path.join(path_out, path_test, path_label))
    for ix1 in tqdm(os.listdir(path_roots)):
        listname = os.listdir(os.path.join(path_roots, ix1, path_image))
        pointer_split = int(ratios*len(listname))
        for i in range(len(listname)):
            if i <= pointer_split:
                source_image = os.path.join(path_roots,ix1, path_image, listname[i])
                source_label = os.path.join(path_roots,ix1, path_label, listname[i].split(".png")[0]+".txt")
                destination_image = os.path.join(path_out, path_test, path_image, listname[i])
                destination_label = os.path.join(path_out, path_test, path_label, listname[i].split(".png")[0]+".txt")
                shutil.copy(source_image, destination_image)
                shutil.copy(source_label, destination_label)
            else:
                source_image = os.path.join(path_roots,ix1, path_image, listname[i])
                source_label = os.path.join(path_roots,ix1, path_label, listname[i].split(".png")[0]+".txt")
                destination_image = os.path.join(path_out, path_train, path_image, listname[i])
                destination_label = os.path.join(path_out, path_train, path_label, listname[i].split(".png")[0]+".txt")
                shutil.copy(source_image, destination_image)
                shutil.copy(source_label, destination_label)

if __name__=="__main__":
    main()