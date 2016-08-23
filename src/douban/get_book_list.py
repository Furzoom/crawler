#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) the furzoom.com
# Authors: mn#furzoom.com

import requests
from bs4 import BeautifulSoup


def get_book_list(cat):
    """
    get book list in category 'cat'.
    :param cat:
    :return: book_list
    """
    url = 'https://book.douban.com/tag/%s' % cat
    response = requests.get(url)

    # get response content
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    book_list = soup.find('ul', class_='subject-list')
    book_list = book_list.find_all('li', class_='subject-item')

    books = []
    count = 0
    fmt = '*{}\t{}\n\tAuthor: {}\n\tPress: {}\n\tDate: {}\n\t' \
          'Price: {}\n\tRating: {}\n\n'
    for book in book_list:
        count += 1
        book_name = book.find('h2').get_text(strip=True)
        meta_info = book.find('div', class_='pub').get_text(strip=True)
        meta_info_list = meta_info.split('/')
        book_price = meta_info_list[-1].strip()
        book_publication_date = meta_info_list[-2].strip()
        book_press = meta_info_list[-3].strip()
        book_author = meta_info_list[0].strip()
        book_translator = ''
        if len(meta_info_list) == 5:
            book_translator = meta_info_list[1]

        book_rating = book.find('span', class_='rating_nums').string
        item = fmt.format(count, book_name, book_author, #book_translator,
                          book_press, book_publication_date, book_price,
                          book_rating)

        books.append(item)

    return '\n'.join(books)


def get_books(cat):
    """
    write books information of category 'cat' into file books.txt
    :param cat:
    :return: None
    """
    content = get_book_list(cat)
    f = open('books.txt', 'w', encoding='utf-8')
    f.write(content)
    f.close()


if __name__ == '__main__':
    get_books('编程')
