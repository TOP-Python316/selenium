import datetime
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


# By — класс, который позволяет использовать разные селекторы
# By.ID — поиск по id
# By.TAG_NAME — поиск по тегу
# By.CLASS_NAME — поиск по классу
# By.NAME — поиск по имени
# By.LINK_TEXT — поиск по тексту ссылки
# By.PARTIAL_LINK_TEXT — поиск по части текста ссылки
# By.CSS_SELECTOR — поиск по css селектору
# By.XPATH — поиск по xpath (/html/body/div[1]/div/div/div/section/div[2]/ol/li[1]/article/div[2]/p[1])


# работаем с https://books.toscrape.com/
URL = 'https://books.toscrape.com/'
IMPLICIT_WAIT = 5

# инициализация драйвера
driver = webdriver.Edge()

# Создание объекта драйвера для браузера Firefox
# driver = webdriver.Firefox()

# Создание объекта драйвера для браузера Edge
# driver = webdriver.Edge()

# Создание объекта драйвера для браузера Safari
# driver = webdriver.Safari()

# Создание объекта драйвера для браузера Chrome
# driver = webdriver.Chrome()


# имплицитное ожидание — применяется ко всем элементам на странице
driver.implicitly_wait(IMPLICIT_WAIT)

# get — метод для открытия сайта
driver.get(URL)

# нужно найти все товарные карточки на странице
# в переменную попадут список элементов
product_pods_list = driver.find_elements(By.CLASS_NAME, 'product_pod')
print(len(product_pods_list))

# возьмём первую книгу
first_product_pod = product_pods_list[0]

# возьмём ссылку на книгу
# в переменной уже лежит книга, поэтому можем просто поискать в ней ссылку
# тег a — это ссылка, атрибут href — это ссылка
first_product_pod_link = first_product_pod.find_element(By.TAG_NAME, 'a')
first_product_pod_link_href = first_product_pod_link.get_attribute('href')
print(first_product_pod_link_href)

# найдём картинку книги.
# её можно найти либо внутри ссылки, либо внутри карточки товара
# в данном случае, ищем внутри ссылки
first_product_pod_img = first_product_pod_link.find_element(By.TAG_NAME, 'img')
first_product_pod_img_src = first_product_pod_img.get_attribute('src')
print(first_product_pod_img_src)

# перейдём в карточку книги по ссылке найденной ранее
driver.get(first_product_pod_link_href)

# подождём 5 секунд
time.sleep(3)
# cделаем шаг назад
driver.back()

# сделаем скриншот в формате дата_время.jpg

date_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# url = driver.current_url
driver.save_screenshot(f'{date_time}.png')

# get_attribute — метод для получения атрибута
# save_screenshot — метод для сохранения скриншота

# проверяем отображение рейтинга книг
# p.star-rating — класс содержащий рейтинг книги

try:
    first_product_pod_rating = first_product_pod.find_element(By.CSS_SELECTOR, 'p.star-rating')
except NoSuchElementException:
    print(f'Рейтинг книги {first_product_pod_link_href} не найден.')
    driver.save_screenshot(f'{date_time}_rating_not_found.png')

# получим оценку книги в виде текста
product_pod_rating_text = first_product_pod_rating.get_attribute('class').split()[-1]
print(f'Рейтинг книги: {product_pod_rating_text}')

# получим название книги. h3 > a — селектор, который найдёт ссылку внутри h3
# h3 — заголовок третьего уровня, a — ссылка
product_pod_title = first_product_pod.find_element(By.CSS_SELECTOR, 'h3 > a')
print(f'Частичное название книги: {product_pod_title.text}')

# полное название можно получить изъяв атрибут title у ссылки
product_pod_title_full = product_pod_title.get_attribute('title')
print(f'Полное название книги: {product_pod_title_full}')

# driver.quit()