import chromedriver_autoinstaller
import pytest
from src.settings import valid_email, valid_password
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture()
def go_to_my_pets(driver):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
    # Нажимаем на ссылку "Мои питомцы"
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

@pytest.mark.usefixtures("go_to_my_pets")
def test_show_my_pets(driver):
    '''Проверяем что мы оказались на странице "Мои питомцы"'''
    
    # Проверяем что мы на странице "Мои питомцы"
    assert driver.current_url == 'https://petfriends.skillfactory.ru/my_pets', f"Это не страница 'Мои питомцы'"

@pytest.mark.usefixtures("go_to_my_pets")
def test_get_all_pets(driver):
    # Ожидаем, пока таблица с питомцами станет доступной
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "all_my_pets"))
    )

    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')
    all_pets_images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/th/img')
    
    # Получаем общее количество питомцев
    count_text = driver.find_element(By.CLASS_NAME, 'task3').text
    total_pets = int(count_text.split("\n")[1].split(" ")[-1])

    # Проверка, что список своих питомцев не пуст
    assert len(all_my_pets) > 0, "Список питомцев пуст!"

    pets_info = []
    pets_names = set()
    pets_with_images = 0

    for i in range(len(all_my_pets)):
        # Получаем информацию о питомце
        pet_info = all_my_pets[i].text.split("\n")
        
        # Проверяем, что существует хотя бы имя питомца
        assert len(pet_info) > 0, f"Нет информации о питомце #{i + 1}"

        pet_name = pet_info[0]

        # Проверяем, что имя уникально
        assert pet_name not in pets_names, f"Имя '{pet_name}' повторяется!"
        pets_names.add(pet_name)

        # Увеличиваем счетчик для питомцев с изображениями, если они есть
        if len(all_pets_images) > i and all_pets_images[i].get_attribute('src'):
            pets_with_images += 1

        # Добавляем информацию о питомце в список
        pets_info.append(pet_info)

        # Проверка, что в информации достаточно данных о питомце
        if len(pet_info) < 2:
            raise AssertionError(f"Недостаточно информации о питомце #{i + 1}: {pet_info}")
    
    # Проверка на уникальность питомцев
    unique_pets = len(set(tuple(info) for info in pets_info))  # Используем tuple для сравнения списков
    assert unique_pets == len(pets_info), f"Найдены повторяющиеся питомцы! Найдено: {unique_pets}, Ожидалось: {len(pets_info)}"

    # Проверка, что хотя бы у половины питомцев есть фото
    assert pets_with_images >= len(all_my_pets) / 2, "Менее половины питомцев имеют фото!"

    # Проверка, что количество найденных питомцев соответствует total_pets
    assert len(all_my_pets) == total_pets, f"Количество найденных питомцев ({len(all_my_pets)}) не соответствует ожидаемому количеству ({total_pets})!"
    