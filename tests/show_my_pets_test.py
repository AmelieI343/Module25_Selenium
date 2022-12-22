import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('./chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.XPATH, "//button[@type='submit']").click()

   my_pets_button = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/my_pets"]')))
   #my_pets_button = pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]')
   my_pets_button.click()

   yield

   pytest.driver.quit()

def test_number_of_pets():
   pytest.driver.implicitly_wait(10)
   all = pytest.driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left').text
   lst = all.split('\n')
   index=lst[1].find(': ')
   ttl = int(lst[1][index+2:])

   raws = pytest.driver.find_elements(By.TAG_NAME, 'tr')
   if raws:
      assert (len(raws)-1) == ttl
   else:
      assert ttl == 0

def test_number_of_photos():
   img_with_photo = pytest.driver.find_elements(By.XPATH, '//img[contains(@src, "data")]')
   raws = pytest.driver.find_elements(By.TAG_NAME, 'tr')
   if img_with_photo:
      assert ((len(raws)-1)/2 - len(img_with_photo) <= 0) == True
   elif raws:
      assert False
   else:
      assert True

def test_not_empty():
   names = pytest.driver.find_elements(By.XPATH, '//tr/td[1]')
   types = pytest.driver.find_elements(By.XPATH, '//tr/td[2]')
   ages = pytest.driver.find_elements(By.XPATH, '//tr/td[3]')

   count = 0
   for i in range(len(names)):
      if names[i] != '' and types[i] != '' and ages[i] != '':
         count += 1

   assert count == len(names)

def test_unique_names():
   names = pytest.driver.find_elements(By.XPATH, '//tr/td[1]')
   unique_names=[]

   for i in range(len(names)):
      if names[i].text not in unique_names:
         unique_names.append(names[i].text)

   assert len(names) == len(unique_names)

def test_unique_animals():
   names = pytest.driver.find_elements(By.XPATH, '//tr/td[1]')
   types = pytest.driver.find_elements(By.XPATH, '//tr/td[2]')
   ages = pytest.driver.find_elements(By.XPATH, '//tr/td[3]')
   for i in range(len(names)):
      for j in range(i+1, len(names)):
         if names[i].text == names[j].text:
            if types[i].text == types[j].text and ages[i].text == ages[j].text:
               assert False

