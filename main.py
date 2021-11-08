import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin,urlparse,urlsplit


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
    return


def download_txt(url, file_name, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        file_name (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    file_name = sanitize_filename(file_name)
    file_path = f"{os.path.join(folder, file_name)}.txt"
    with open(file_path, "w", encoding='UTF-8') as my_file:
        my_file.write(response.text)
    return file_path

def download_image(url, folder='images/'):
    if "nopic" in image_url: return
    os.makedirs(folder, exist_ok=True)
    file_name= urlsplit(url).path.split('/')[-1]
    response = requests.get(url)
    response.raise_for_status()
    file_path = os.path.join(folder, file_name)
    with open(file_path, "wb") as my_file:
        my_file.write(response.content)
    return file_path




for book_id in range(1, 11):

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
    print(book_name)
    book_author = book_header[1].strip()

    url = f'https://tululu.org/txt.php?id={book_id}'
    try:
        download_txt(url, f'{book_id}.{book_name}')
    except requests.HTTPError:
        continue

    image_url = soup.find('div', class_='bookimage').find('img')['src']
    image_url = urljoin('https://tululu.org/', image_url)
    download_image(image_url)

    comments = soup.find_all('div', class_='texts')
    for comment in comments:
        print(comment.find('span').text)
    print('')

