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
def go_to_my_pets():

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

def test_show_my_pets(go_to_my_pets):
   '''Проверяем что мы оказались на странице "Мои питомцы"'''

   if not pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets':
      pytest.driver.quit()
      raise Exception("Это не страница 'Мои питомцы'")


      # Проверяем что мы на странице "Мои питомцы"
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'