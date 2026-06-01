from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

browser = webdriver.Chrome(service=Service('./chromedriver.exe'))
browser.get('https://ispi.cdo.vlsu.ru/login/index.php')

username = browser.find_element(by=By.NAME, value='username')
username.send_keys('k1179e6jt')

password = browser.find_element(by=By.ID, value='password')
password.send_keys('NA498bli')

button = browser.find_element(by=By.CSS_SELECTOR, value='#loginbtn')
button.click()

try:
    assert 'Вход на сайт' in browser.title
    errormessage = browser.find_element(by=By.ID, value='loginerrormessage')
    assert 'Неверный логин или пароль' in errormessage.text
    print('The test was completed successfully')
except Exception as err:
    print('The test was failed')

browser.close()
