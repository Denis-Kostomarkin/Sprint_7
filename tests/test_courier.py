import pytest
import requests
import allure
from helpers import register_new_courier_and_return_login_password, delete_courier

@allure.feature('Создание курьера')
class TestCourierCreation:
    
    @allure.title('Создание курьера')
    def test_create_courier_success(self, base_url, create_courier):
        """Проверка успешного создания курьера"""
        with allure.step('Проверить, что курьер создан'):
            courier_data = create_courier
            assert courier_data is not None, "Курьер не был создан"
            assert len(courier_data) == 3, "Не все данные курьера получены"
    
    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_fails(self, base_url, create_courier):
        """Проверка, что нельзя создать двух одинаковых курьеров"""
        courier_data = create_courier
        login, password, first_name = courier_data
        
        with allure.step('Попытка создания дубликата курьера'):
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
            response = requests.post(f'{base_url}/api/v1/courier', data=payload)
            
            assert response.status_code == 409, f"Ожидался код 409, получен {response.status_code}"
            assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."
    
    @allure.title('Создание курьера без логина')
    def test_create_courier_without_login_fails(self, base_url):
        """Проверка создания курьера без логина"""
        payload = {
            "password": "password123",
            "firstName": "TestName"
        }
        
        with allure.step('Отправить запрос без логина'):
            response = requests.post(f'{base_url}/api/v1/courier', data=payload)
            
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
    
    @allure.title('Создание курьера без пароля')
    def test_create_courier_without_password_fails(self, base_url):
        """Проверка создания курьера без пароля"""
        payload = {
            "login": "testlogin",
            "firstName": "TestName"
        }
        
        with allure.step('Отправить запрос без пароля'):
            response = requests.post(f'{base_url}/api/v1/courier', data=payload)
            
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
    
    @allure.title('Успешный запрос возвращает ok:true')
    def test_successful_creation_returns_ok(self, base_url):
        """Проверка, что успешный запрос возвращает {"ok":true}"""
        import random
        import string
        
        login = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        password = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        
        payload = {
            "login": login,
            "password": password,
            "firstName": "TestName"
        }
        
        with allure.step('Создать нового курьера'):
            response = requests.post(f'{base_url}/api/v1/courier', data=payload)
            
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
            assert response.json()["ok"] == True
            
        # Удаляем созданного курьера
        delete_courier(login, password)