import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
    return


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    filename = sanitize_filename(filename)
    filepath = f"{os.path.join(folder, filename)}.txt"
    with open(filepath, "w", encoding='UTF-8') as my_file:
        my_file.write(response.text)
    return filepath


for book_id in range(1, 11):
    """book_url = f'https://tululu.org/txt.php?id={book_id}'
    book_response = requests.get(book_url)
    book_response.raise_for_status()
    try:
        check_for_redirect(book_response)
    except requests.HTTPError:
        continue"""

    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except requests.HTTPError:
        continue

    soup = BeautifulSoup(response.text, 'lxml')
    book_header = soup.find('h1').text.replace(u'\xa0', u'').split('::')
    book_name = book_header[0].strip()
    book_author = book_header[1].strip()

    url = f'https://tululu.org/txt.php?id={book_id}'
    try:
        download_txt(url,f'{book_id}.{book_name}')
    except requests.HTTPError:
        continue


