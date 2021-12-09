import os
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(url, params, file_name, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, params)
    response.raise_for_status()
    check_for_redirect(response)
    file_name = sanitize_filename(file_name)
    file_path = f"{os.path.join(folder, file_name)}.txt"
    with open(file_path, "w", encoding='UTF-8') as file:
        file.write(response.text)
    return file_path


def download_image(url, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    file_name = urlsplit(url).path.split('/')[-1]
    response = requests.get(url)
    response.raise_for_status()
    file_path = os.path.join(folder, file_name)
    with open(file_path, "wb") as file:
        file.write(response.content)
    return file_path


def parse_book_page(html):
    soup = BeautifulSoup(html, 'lxml')
    name, author = soup.select_one('h1').text.replace(u'\xa0', u'').split('::')
    comments = soup.select('.texts')
    genres = soup.select('span.d_book a')
    book = {"title": name.strip(),
            "author": author.strip(),
            'img_src': soup.select_one('.bookimage img')['src'],
            'comments': [comment.text for comment in comments],
            'genres': [genre.text for genre in genres]}
    return book


def total_pages():
    url = f'https://tululu.org/l55/1/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.select('.npage')[-1].text
