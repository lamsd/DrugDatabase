import os 
import shutil
import requests
from bs4 import BeautifulSoup
from tqdm import trange
import math 
import time


def download_data(path_image, path_out, name_path):
    """
    Checking data with python

    """
    response = requests.get(path_image, stream=True)
    with open(f"{path_out}/{name_path}", 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

def crawpling_data(name_out, name_number=1 , check_sytem=True):
    url = f'https://www.medicine.com/pill-finder/search?imprint=&shape={name_number}&color='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    index_x = soup.find_all("p", {'class':'mdc-search-results-count'})
    index_x1 = index_x[0].find_all("b")
    index_pages = index_x1[0].get_text().split(" - ")[1]
    number_pages = math.ceil(int(index_x1[1].get_text().replace(",", ""))/ int(index_pages))
    path_out = f"Image1/{name_out}"
    if not os.path.exists(path_out):
        os.makedirs(path_out)
    for i in trange(int(number_pages)):
        url = f'https://www.medicine.com/pill-finder/search?imprint=&shape={name_number}&color=&page={i+1}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        if len(images) == 0:
            continue
        for image in images:
            path_image = image['src']
            name_path = path_image.split("/")[-1]
            if os.path.exists(f"{path_out}/{name_path}"):
                continue
            if path_image.endswith((".jpg",".png", ".webp", "jpeg")) &  path_image.startswith("https://"):
                download_data(path_image, path_out, name_path)
        # time.sleep(1)

def crawpling_data_v1(name_out, name_number=1):
    url = f'https://www.medicine.com/pill-finder/search?imprint=&shape={name_number}&color=&page=1'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    index_x = soup.find_all('ul',{"class":"mdc-pagination"})
    index_number = index_x[0].find_all("a")[-2].get_text()
    path_out = f"Image1/{name_out}"
    if not os.path.exists(path_out):
        os.makedirs(path_out)
    for i in trange(int(index_number)):
        url = f'https://www.medicine.com/pill-finder/search?imprint=&shape={name_number}&color=&page={i+1}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        if len(images) == 0:
            continue
        for image in images:
            path_image = image['src']
            # download_data(path_image, path_out)

if __name__ == "__main__":
    url = f'https://www.medicine.com/pill-finder/search?imprint=&shape=1&color='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('select', {"name":"shape"})
    for i in images[0].find_all("option"):
        index  = i["value"]
        name_index = i.get_text()
        if index != "":
            crawpling_data(name_index, name_number = index)