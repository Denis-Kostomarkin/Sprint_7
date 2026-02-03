import pytest
import requests
import allure
from helpers import login_courier

@allure.feature('Авторизация курьера')
class TestCourierLogin:
    
    @allure.title('Успешная авторизация курьера')
    def test_login_courier_success(self, base_url, create_courier):
        """Проверка успешной авторизации курьера"""
        courier_data = create_courier
        login, password, _ = courier_data
        
        with allure.step('Авторизоваться с корректными данными'):
            response = login_courier(login, password)
            
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            assert "id" in response.json(), "В ответе должен быть id курьера"
    
    @allure.title('Авторизация без логина')
    def test_login_without_login_fails(self, base_url, create_courier):
        """Проверка авторизации без логина"""
        courier_data = create_courier
        _, password, _ = courier_data
        
        with allure.step('Отправить запрос без логина'):
            payload = {"password": password}
            response = requests.post(f'{base_url}/api/v1/courier/login', data=payload)
            
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
    
    @allure.title('Авторизация без пароля')
    def test_login_without_password_fails(self, base_url, create_courier):
        """Проверка авторизации без пароля"""
        courier_data = create_courier
        login, _, _ = courier_data
    
        with allure.step('Отправить запрос без пароля'):
            payload = {"login": login}
            response = requests.post(f'{base_url}/api/v1/courier/login', data=payload)
        
            assert response.status_code != 200, f"Запрос без пароля должен завершиться ошибкой, получен {response.status_code}"
            assert response.status_code in [400, 504, 404], f"Ожидался код ошибки 400, 404 или 504, получен {response.status_code}"
    
    @allure.title('Авторизация с неверным логином')
    def test_login_with_wrong_login_fails(self, base_url, create_courier):
        """Проверка авторизации с неверным логином"""
        courier_data = create_courier
        _, password, _ = courier_data
        
        with allure.step('Авторизоваться с неверным логином'):
            payload = {
                "login": "wrong_login",
                "password": password
            }
            response = requests.post(f'{base_url}/api/v1/courier/login', data=payload)
            
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
    
    @allure.title('Авторизация с неверным паролем')
    def test_login_with_wrong_password_fails(self, base_url, create_courier):
        """Проверка авторизации с неверным паролем"""
        courier_data = create_courier
        login, _, _ = courier_data
        
        with allure.step('Авторизоваться с неверным паролем'):
            payload = {
                "login": login,
                "password": "wrong_password"
            }
            response = requests.post(f'{base_url}/api/v1/courier/login', data=payload)
            
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
    
    @allure.title('Авторизация под несуществующим пользователем')
    def test_login_nonexistent_courier_fails(self, base_url):
        """Проверка авторизации несуществующего курьера"""
        with allure.step('Авторизоваться с несуществующими данными'):
            payload = {
                "login": "nonexistent_user",
                "password": "nonexistent_password"
            }
            response = requests.post(f'{base_url}/api/v1/courier/login', data=payload)
            
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"