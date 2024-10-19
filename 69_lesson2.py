import datetime
import json
from pprint import pprint
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


# работаем с https://books.toscrape.com/
URL = 'https://books.toscrape.com/'
IMPLICIT_WAIT = 5

# инициализация драйвера
driver = webdriver.Edge()

# имплицитное ожидание — применяется ко всем элементам на странице
driver.implicitly_wait(IMPLICIT_WAIT)

# get — метод для открытия сайта
driver.get(URL)

books_list = []
page = 1

while True:

    # нужно найти все товарные карточки на странице
    # в переменную попадут список элементов
    product_pods_list = driver.find_elements(By.CLASS_NAME, 'product_pod')

    for product_pod in product_pods_list:
        # Объявляем словарь для хранения информации о книге
        product_dict = {}

        try:
            # получим название книги. h3 > a — селектор, который найдёт ссылку внутри h3
            # h3 — заголовок третьего уровня, a — ссылка
            product_pod_title = product_pod.find_element(By.CSS_SELECTOR, 'h3 a').get_attribute("title")
            product_dict['title'] = product_pod_title
        except NoSuchElementException:
            print('Название книги не найдено')
            product_dict['title'] = None

        try:
            # получим рейтинг книги
            product_pod_rating = product_pod.find_element(By.CSS_SELECTOR, 'p.star-rating')
            product_pod_rating_text = product_pod_rating.get_attribute('class').split()[-1]
            product_dict['rating'] = product_pod_rating_text
        except NoSuchElementException:
            print('Рейтинг книги не найден')
            product_dict['rating'] = None

        try:
            # получим ссылку на книгу
            product_pod_link = product_pod.find_element(By.TAG_NAME, 'a')
            product_pod_link_href = product_pod_link.get_attribute('href')
            product_dict['link'] = product_pod_link_href
        except NoSuchElementException:
            print('Ссылка на книгу не найдена')
            product_dict['link'] = None

        try:
            # получим ссылку на картинку книги
            product_pod_img = product_pod.find_element(By.TAG_NAME, 'img')
            product_pod_img_src = product_pod_img.get_attribute('src')
            product_dict['img'] = product_pod_img_src
        except NoSuchElementException:
            print('Ссылка на картинку книги не найдена')
            product_dict['img'] = None

        try:
            # получим описание книги
            product_pod_description = product_pod.find_element(By.TAG_NAME, 'p')
            product_dict['description'] = product_pod_description.text
        except NoSuchElementException:
            print('Описание книги не найдено')
            product_dict['description'] = None

        try:
            # получим цену книги
            product_pod_price = product_pod.find_element(By.CLASS_NAME, 'price_color')
            product_dict['price'] = product_pod_price.text
        except NoSuchElementException:
            print('Цена книги не найдена')
            product_dict['price'] = None

        # добавили несуществующий тег автора, чтобы проверить работу try-except
        # try:
        #     # получим автора книги
        #     product_pod_author = product_pod.find_element(By.CLASS_NAME, 'author')
        #     product_dict['author'] = product_pod_author.text
        # except NoSuchElementException:
        #     print('Автор книги не найден')
        #     product_dict['author'] = None

        # добавим словарь с данными о книге в список
        books_list.append(product_dict)
        print(f'Добавлена книга {product_dict["title"]}')

    try:
        # перейдём к следующей странице
        next_page = driver.find_element(By.CSS_SELECTOR, 'ul.pager > li.next > a')
        next_page_href = next_page.get_attribute('href')
        print(f'Информация со страницы {page} собрана \n')
        page += 1
        driver.get(next_page_href)

    except NoSuchElementException:
        print('Это последняя страница')
        break


with open('books.json', 'w', encoding='utf-8') as json_file:
    json.dump(books_list, json_file, indent=4, ensure_ascii=False)
    print('Данные успешно сохранены в файл books.json')


pprint(books_list)
