# импорт основного класса webdriver
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


# инициализация драйвера
driver = webdriver.Edge()

# метод для открытия сайта
driver.get("https://www.google.com/")

# найдём элемент на сайте гугл по тегу textarea
search_field = driver.find_element(By.TAG_NAME, "textarea")

# вводим текст
search_field.send_keys("Bender Bending Rodriguez")

# .submit() — отправляет форму
search_field.submit()

time.sleep(5)

search_field2 = None
try:
    search_field2 = driver.find_element(By.NAME, "textarealksjdflksdj")
except NoSuchElementException:
    print("Element textarealksjdflksdj not found")

driver.quit()
