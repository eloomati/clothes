import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os

def get_page(category, subcategory, identi, page_counter):
  url = f"https://sklep-domwhisky.pl/{category}{subcategory}{identi}.html?counter={page_counter}"
  try:
    response = requests.get(url)
    content = response.content
    return content
  except:
    print('Web doesnt exist')


def parse_url(content):
  soup = BeautifulSoup(content, 'html.parser')
  imgs = soup.find_all('img',{'class': 'b-lazy'})
  end_link = [img['data-src'] for img in imgs]
  return end_link

def get_img(url, path, subcategory):
  try:
    response = requests.get(url)
    content = response.content
    img = Image.open(BytesIO(content))
    img_name = url.split('/')[-1].split('.')[0] + '.jpg'
    os.makedirs(f'{path}/{subcategory}', exist_ok=True)
    img.save(f'{path}/{subcategory}/{img_name}')
  except:
    print('Fail')

def get_data(category,
             subcategory,
             identi,
             start_page,
             end_page,
             path):
  for page_counter in range(start_page, end_page + 1):
    content = get_page(category, subcategory, identi, page_counter)
    urls =  parse_url(content)

    for i, url in enumerate(urls):
      link = 'https://sklep-domwhisky.pl' + url
      get_img(link, path, subcategory)
      if i % 20 == 0:
        print(f'Downloaded {i} for page {page_counter} from {subcategory}')