import cv2
import os
import shutil
from rembg import remove
from tqdm import tqdm
from time import sleep

def remove_folder(path_folder_output, condition=False):
    """
    Targets: Reset folder:
    Input: 
        path_folder_output: output folder.
        condition: default = False, remove and new creatition.
    """
    if condition:
        if os.path.exists(path_folder_output):
            shutil.rmtree(path_folder_output)
            sleep(10)
            os.mkdir(path_folder_output)

def processing_drug(path_folder_images, path_folder_output, condition=False):
    """
    Targer: Remove the backgrounds and split the  objects in images.
    Input: 
        path_folder_images: folder occupe the images.
        path_folder_output: output folders.
    """
    list_name = [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE]
    remove_folder(path_folder_output, condition)
    for name in tqdm(os.listdir(path_folder_images)):
        if not os.path.exists(os.path.join(path_folder_output, name)):
            os.mkdir(os.path.join(path_folder_output, name))
        for index_name in os.listdir(os.path.join(path_folder_images, name)):
            # print(index_name)
            name_file = index_name.split(".")[0]
            img = cv2.imread(os.path.join(path_folder_images, name, index_name))
            img = remove(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if len(contours) > 2:
                # print("Name data_fide !!!!!!!!!!!!!!!1")
                continue
            for i in range(len(contours)):
                x, y, width, height = cv2.boundingRect(contours[i])
                src = img[y:y+height, x:x+width]
                tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
                _, alpha = cv2.threshold(tmp, 10, 255, cv2.THRESH_BINARY)#+cv2.THRESH_OTSU)
                b, g, r = cv2.split(src)
                rgba = [b, g, r, alpha]
                dst = cv2.merge(rgba, 10)
                if dst.shape[0] < dst.shape[1]:
                    for j in list_name:
                        dst1 = cv2.rotate(dst, j)
                        cv2.imwrite(f"{path_folder_output}/{name}/{name_file}_{j}.png", dst1)
                else:
                    cv2.imwrite(f"{path_folder_output}/{name}/{name_file}_1.png", dst)

if __name__=="__main__":
    path_folder_images = "Image1"
    path_folder_output = "Output"
    processing_drug(path_folder_images, path_folder_output, condition=False)