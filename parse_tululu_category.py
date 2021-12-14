import argparse
import json
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from download import download_image, download_txt, parse_book_page, check_for_redirect, get_pages_number


def main():
    books = []
    parser = argparse.ArgumentParser(description='Download books from tululu.org')
    parser.add_argument('--start_page', default=1, type=int)
    parser.add_argument('--end_page', default=get_pages_number(), type=int)
    parser.add_argument('--dest_folder', default=os.getcwd(), type=str,
                        help='path to the directory with parsing results')
    parser.add_argument('--skip_imgs', action='store_true', help='do not download images')
    parser.add_argument('--skip_txt', action='store_true', help='do not download books')
    parser.add_argument('--json_path', default=os.getcwd(), type=str,
                        help='specify your path to *.json file with results')

    args = parser.parse_args()
    for page in range(args.start_page, args.end_page):
        url = f'https://tululu.org/l55/{page}/'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        books_from_page = soup.select('.d_book')
        for book in books_from_page:
            href = book.select_one('a').get('href')
            book_id = href[2:-1]
            url = urljoin('https://tululu.org/', href)
            response = requests.get(url)
            try:
                response.raise_for_status()
                check_for_redirect(response)
                book = parse_book_page(response.text)
                if not args.skip_txt:
                    url = 'https://tululu.org/txt.php'
                    params = {'id': book_id}
                    filename = f'{book_id}.{book["title"]}'
                    path = os.path.join(args.dest_folder, 'books/')
                    book['file_path'] = download_txt(url, params, filename, path)
                if not args.skip_imgs:
                    url = urljoin('https://tululu.org/', book["img_src"])
                    download_image(url, os.path.join(args.dest_folder, 'images/'))
            except requests.HTTPError:
                continue
            books.append(book)

    with open(os.path.join(args.json_path, 'books.json'), "w", encoding='utf-8') as file:
        json.dump(books, file, ensure_ascii=False)


if __name__ == "__main__":
    main()
