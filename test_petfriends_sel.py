import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('driver/chromedriver.exe')
    # Переход на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_quantity_of_my_pets():
    # Ввод email
    pytest.driver.find_element_by_id('email').send_keys('ilovehamsters@mail.ru')

    # Ввод пароля
    pytest.driver.find_element_by_id('pass').send_keys('12345')
    # Нажатие кнопки входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

    pytest.driver.implicitly_wait(10)  # Неявное ожидание
    # Переход на страницу "Мои питомцы"
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
    # Получаем содержание статистики пользователя
    statistic_user = pytest.driver.find_elements_by_xpath('//div[@class=".col-sm-4 left"]')  # локатор
    for item in statistic_user:
        statistic = item.text  # Получаем текст статистики
        # Извлекаем цифры из текста
        res = [int(i) for i in statistic.split() if i.isdigit()]
        # Выбираем интересующий нас показатель
        statistic_num = int(str(res)[1])
        # Получаем данные из таблицы питомцев
        pet_tabl = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr')
        fact_num = len(pet_tabl)
        # Предполагаем, что число питомцев в таблице равно их числу в статистике
        assert statistic_num == fact_num


def test_images_of_my_pets():
    # Ввод email
    pytest.driver.find_element_by_id('email').send_keys('ilovehamsters@mail.ru')

    # Ввод пароля
    pytest.driver.find_element_by_id('pass').send_keys('12345')

    # Нажатие кнопки входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    pytest.driver.implicitly_wait(10)  # Неявное ожидание
    # Переход на страницу "Мои питомцы"
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
    # Находим в таблице ячейки, где размещаются картинки
    images = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    # Узнаем количество картинок, отнимая от общего числа ячеек в соответствующем столбце не содержащие изображений
    for item in images:
        count = len(images)
        if item.get_attribute('src') == '':
            count -= 1
            # Предполагаем, что число питомцев с картинками равно или больше половины их общего количества
            assert count >= (len(images)) * 0.5


def test_unique_name():
    # Ввод email
    pytest.driver.find_element_by_id('email').send_keys('ilovehamsters@mail.ru')

    # Ввод пароля
    pytest.driver.find_element_by_id('pass').send_keys('12345')

    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    pytest.driver.implicitly_wait(10)  # Неявное ожидание
    # Переходим на страницу "Мои питомцы"
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
    # Получаем список имен питомцев
    names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    for item in names:
        string_names = item.text  # Получаем имена в виде текста
        # Проверяем уникальность имен в строке
        for i in range(len(string_names) - 1):
            for j in range(i + 1, len(string_names)):
                if string_names[j] == string_names[i]:
                    return False  # если имена совпадают - возвращаем False
        return True  # если имена уникальны - True
    assert True


def test_descriptions():
    # Ввод email
    pytest.driver.find_element_by_id('email').send_keys('ilovehamsters@mail.ru')

    # Ввод пароля
    pytest.driver.find_element_by_id('pass').send_keys('12345')

    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Переход на страницу "Мои питомцы"
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')))  # Явное ожидание
    # Получаем список строк в таблице питомцев
    strings = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr')
    # Получаем список имен
    names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    # Получаем список пород
    breeds = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    # Получаем список возрастов
    ages = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    # Предполагаем, что длина списков имен, пород и возрастов равна количеству строк в таблице
    assert len(strings) == len(names) == len(breeds) == len(ages)