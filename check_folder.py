import os  
import shutil
from tqdm import tqdm

"""
Checking folder in folders: 
"""
def checking_folder(path_folder_images):
    """
    Target: check folder in labels and remove the hidden folder. 
    Input: path input, which you want to check.
    """
    for name in tqdm(os.listdir(path_folder_images)):
        try:
            shutil.rmtree(os.path.join(path_folder_images, name, ".ipynb_checkpoints"), ignore_errors=True)
        except Exception as e:
            pass
        for sub_name in os.listdir(os.path.join(path_folder_images,name)):
            if os.path.isdir(os.path.join(path_folder_images,name, sub_name)):
                print(name)
                for subsub_name in os.listdir(os.path.join(path_folder_images, name, sub_name)):
                    if os.path.isdir(os.path.join(path_folder_images,name, sub_name, subsub_name)):
                        print(name)
                        break 
                    source = os.path.join(path_folder_images,name, sub_name, subsub_name)
                    destination = os.path.join(path_folder_images, name, f"{sub_name}_"+subsub_name)
                    shutil.copy(source, destination)
                try:
                    shutil.rmtree(os.path.join(path_folder_images,name, sub_name), ignore_errors=True)
                except Exception as e:
                    pass

if __name__ == "__main__":
    path_folder_images = "Image1"
    checking_folder(path_folder_images)
    
