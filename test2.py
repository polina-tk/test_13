import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = './chromedriver.exe'

def create_driver():
    service = Service(executable_path=DRIVER_PATH)
    return webdriver.Chrome(service=service)

def test_successful_login():
    """Тест-кейс 1: Успешная авторизация."""
    driver = create_driver()
    try:
        driver.get('https://www.saucedemo.com')
        driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        driver.find_element(By.ID, 'password').send_keys('secret_sauce')
        driver.find_element(By.ID, 'login-button').click()

        inventory_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'inventory_container'))
        )
        assert inventory_container.is_displayed(), 'Список товаров не отображается'
        print('Test 1 PASSED: Успешный вход выполнен.')
    except Exception as e:
        print(f'Test 1 FAILED: {e}')
    finally:
        driver.quit()

def test_locked_out_user():
    """Тест-кейс 2: Вход заблокированного пользователя."""
    driver = create_driver()
    try:
        driver.get('https://www.saucedemo.com')
        driver.find_element(By.ID, 'user-name').send_keys('locked_out_user')
        driver.find_element(By.ID, 'password').send_keys('secret_sauce')
        driver.find_element(By.ID, 'login-button').click()

        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="error"]'))
        )
        expected_text = 'Epic sadface: Sorry, this user has been locked out.'
        assert expected_text in error_element.text, 'Сообщение об ошибке не совпадает'

        login_button = driver.find_element(By.ID, 'login-button')
        assert login_button.is_displayed(), 'Кнопка входа не найдена — возможно, вошли в систему'

        print('Test 2 PASSED: Заблокированный пользователь не может войти.')
    except Exception as e:
        print(f'Test 2 FAILED: {e}')
    finally:
        driver.quit()

def test_add_to_cart():
    """Тест-кейс 3: Добавление товара в корзину."""
    driver = create_driver()
    try:
        driver.get('https://www.saucedemo.com')
        driver.find_element(By.ID, 'user-name').send_keys('standard_user')
        driver.find_element(By.ID, 'password').send_keys('secret_sauce')
        driver.find_element(By.ID, 'login-button').click()

        add_button = driver.find_element(By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]')
        add_button.click()

        cart_badge = driver.find_element(By.CLASS_NAME, 'shopping_cart_badge')
        assert cart_badge.text == '1', 'Количество товаров в корзине не равно 1'

        driver.find_element(By.CLASS_NAME, 'shopping_cart_link').click()

        item_name = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'inventory_item_name'))
        )
        assert item_name.text == 'Sauce Labs Backpack', 'Название товара в корзине не совпадает'
        print('Test 3 PASSED: Товар успешно добавлен в корзину.')
    except Exception as e:
        print(f'Test 3 FAILED: {e}')
    finally:
        driver.quit()

if __name__ == '__main__':
    test_successful_login()
    time.sleep(1) 
    test_locked_out_user()
    time.sleep(1)
    test_add_to_cart()
