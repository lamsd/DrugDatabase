import cv2
import os
import glob
import xml.etree.ElementTree as ET
from tqdm import tqdm

path_roots = "Result"
path_image = "images" 
path_label = "labels"
for ix1 in  tqdm(os.listdir(path_roots)):
    for file_path in glob.glob(os.path.join(path_roots, ix1, path_label,  '*.txt')):
        with open( file_path) as f:
            lines = f.readlines()
        name_path = os.path.splitext(os.path.basename(file_path))[0]
        xml_path =  os.path.join(path_roots, ix1, path_label, name_path + '.xml')
        root = ET.Element('annotation')
        folder = ET.SubElement(root, 'folder')
        folder.text = 'images'
        filename = ET.SubElement(root, 'filename')
        filename.text = name_path + '.png'
        img = cv2.imread(os.path.join(path_roots, ix1, path_image, name_path+ '.png'))
        w, h, _ = img.shape
        size = ET.SubElement(root, 'size')
        width = ET.SubElement(size, 'width')
        height = ET.SubElement(size, 'height')
        depth = ET.SubElement(size, 'depth')
        width.text = str(w)#'640'
        height.text =str(h)# '480'
        depth.text = '3'
        for line in lines:
            parts = line.strip().split()
            obj = ET.SubElement(root, 'object')
            name = ET.SubElement(obj, 'name')
            name.text = parts[0]
            bndbox = ET.SubElement(obj, 'bndbox')
            xmin = ET.SubElement(bndbox, 'xmin')
            ymin = ET.SubElement(bndbox, 'ymin')
            xmax = ET.SubElement(bndbox, 'xmax')
            ymax = ET.SubElement(bndbox, 'ymax')
            xmin.text = str(int(float(parts[1]) * w))
            ymin.text = str(int(float(parts[2]) * h))
            xmax.text = str(int(float(parts[3]) * w))
            ymax.text = str(int(float(parts[4]) * h))
        tree = ET.ElementTree(root)
        tree.write(xml_path)