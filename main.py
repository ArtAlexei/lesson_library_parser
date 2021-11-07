import requests, os

books_directory = 'books'
os.makedirs(books_directory, exist_ok=True)

for book_id in range(1, 11):
    url = 'https://tululu.org/txt.php?id=32168'
    response = requests.get(url)
    response.raise_for_status()
    with open(f"{books_directory}/id{book_id}.txt", "w",encoding='UTF-8') as my_file:
        my_file.write(response.text)
