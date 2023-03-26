import os 
import shutil
import requests
from bs4 import BeautifulSoup
from tqdm import trange

def download_data(path_image, path_out):
    """
    Checking data with python

    """
    if path_image.endswith((".jpg",".png", ".webp", "jpeg")) &  path_image.startswith("https://"):
        response = requests.get(path_image, stream=True)
        name_path = path_image.split("/")[-1]
        with open(f"{path_out}/{name_path}", 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

def crawpling_data(name_out, name_number=1):
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
            download_data(path_image, path_out)

if __name__ == "__main__":
    url = f'https://www.medicine.com/pill-finder/search?imprint=&shape=2&color='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('select', {"name":"shape"})
    for i in images[0].find_all("option"):
        index  = i["value"]
        name_index = i.get_text()
        if index != "":
            crawpling_data(name_index, index)