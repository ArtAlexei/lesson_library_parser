import argparse
import os
from urllib.parse import urljoin, urlsplit

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
    book = {"title": name.strip(),
            "author": author.strip()}
    book['img_src'] = soup.select_one('.bookimage img')['src']
    comments = soup.select('.texts')
    book['comments'] = [comment.text for comment in comments]
    genres = soup.select('span.d_book a')
    book['genres'] = [genre.text for genre in genres]
    return book


def main():
    parser = argparse.ArgumentParser(description='Download books from tululu.org')
    parser.add_argument('--start_id', default=1, type=int)
    parser.add_argument('--end_id', default=10, type=int)
    args = parser.parse_args()
    for book_id in range(args.start_id, args.end_id):
        url = f'https://tululu.org/b{book_id}/'
        response = requests.get(url)
        try:
            response.raise_for_status()
            check_for_redirect(response)
            book = parse_book_page(response.text)

            url = 'https://tululu.org/txt.php'
            params = {'id': book_id}
            download_txt(url, params, f'{book_id}.{book["name"]}')

            url = urljoin('https://tululu.org/', book["image_url"])
            download_image(url)
        except requests.HTTPError:
            continue

        print(book['name'])
        for genre in book['genres']:
            print(genre)
        print('')


if __name__ == "__main__":
    main()
