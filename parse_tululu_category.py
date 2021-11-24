import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from main import download_image, download_txt, parse_book_page, check_for_redirect

books = []
for page in range(1, 2):
    url = f'https://tululu.org/l55/{page}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    books_from_page = soup.find_all("table", class_="d_book")
    for book in books_from_page:
        href = book.find('a').get('href')
        book_id = href[2:-1]
        url = urljoin('https://tululu.org/', href)
        response = requests.get(url)
        try:
            response.raise_for_status()
            check_for_redirect(response)
            book = parse_book_page(response.text)

            url = 'https://tululu.org/txt.php'
            params = {'id': book_id}
            book['file_path'] = download_txt(url, params, f'{book_id}.{book["title"]}')

            url = urljoin('https://tululu.org/', book["img_src"])
            download_image(url)
        except requests.HTTPError:
            continue
        books.append(book)
        print(book)

with open("books.json", "w", encoding='utf-8') as file:
    json.dump(books, file, ensure_ascii=False)
