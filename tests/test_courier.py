import pytest
import requests
import allure
from helpers import create_courier_payload, generate_random_string
from config import BASE_URL, Endpoints


@allure.feature('Создание курьера')
class TestCourierCreation:
    
    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self, cleanup_courier):
        payload = create_courier_payload()
        
        with allure.step('Отправить запрос на создание курьера'):
            response = requests.post(
                BASE_URL + Endpoints.COURIER_CREATE,
                data=payload
            )
        
        with allure.step('Проверить ответ сервера'):
            assert response.status_code == 201, (
                f"Ожидался код 201, получен {response.status_code}"
            )
            assert response.json()["ok"] is True, (
                f"Ответ должен содержать {{'ok': true}}, получен {response.json()}"
            )
        
        cleanup_courier(payload["login"], payload["password"])
    
    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_fails(self):
        login = f"user_{generate_random_string(8)}"
        
        payload1 = create_courier_payload(login=login)
        response1 = requests.post(
            BASE_URL + Endpoints.COURIER_CREATE,
            data=payload1
        )
        
        if response1.status_code != 201:
            pytest.skip(f"Не удалось создать первого курьера: {response1.status_code}")
        
        with allure.step('Попытаться создать такого же курьера'):
            payload2 = payload1  # Используем те же данные
            response2 = requests.post(
                BASE_URL + Endpoints.COURIER_CREATE,
                data=payload2
            )
        
        with allure.step('Проверить ошибку дубликата'):
            assert response2.status_code == 409, (
                f"Ожидался код 409, получен {response2.status_code}"
            )
            error_message = response2.json().get("message", "")
            assert "логин уже используется" in error_message, (
                f"Сообщение об ошибке должно указывать на дубликат логина, получено: {error_message}"
            )
        
        try:
            from helpers import delete_courier
            delete_courier(payload1["login"], payload1["password"])
        except:
            pass  
    
    @allure.title('Создание курьера без логина')
    def test_create_courier_without_login_fails(self):
        """Проверка создания курьера без логина - должен вернуть код 400"""
        payload = {
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        with allure.step('Отправить запрос без логина'):
            response = requests.post(
                BASE_URL + Endpoints.COURIER_CREATE,
                data=payload
            )
        
        with allure.step('Проверить ошибку'):
            assert response.status_code == 400, (
                f"Ожидался код 400, получен {response.status_code}"
            )
    
    @allure.title('Создание курьера без пароля')
    def test_create_courier_without_password_fails(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        with allure.step('Отправить запрос без пароля'):
            response = requests.post(
                BASE_URL + Endpoints.COURIER_CREATE,
                data=payload
            )
        
        with allure.step('Проверить ошибку'):
            assert response.status_code == 400, (
                f"Ожидался код 400, получен {response.status_code}"
            )