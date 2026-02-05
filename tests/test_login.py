import pytest
import requests
import allure
from helpers import create_courier_payload, generate_random_string
from config import BASE_URL, Endpoints


@allure.feature('Авторизация курьера')
class TestCourierLogin:
    
    @allure.title('Успешная авторизация курьера')
    def test_login_courier_success(self, cleanup_courier):
        """Проверка успешной авторизации курьера"""
        payload = create_courier_payload()
        
        with allure.step('Зарегистрировать курьера'):
            reg_response = requests.post(
                BASE_URL + Endpoints.COURIER_CREATE,
                data=payload
            )
            assert reg_response.status_code == 201, (
                f"Курьер должен быть создан, получен код {reg_response.status_code}"
            )
        
        with allure.step('Авторизоваться с корректными данными'):
            login_payload = {
                "login": payload["login"],
                "password": payload["password"]
            }
            response = requests.post(
                BASE_URL + Endpoints.COURIER_LOGIN,
                data=login_payload
            )
        
        with allure.step('Проверить успешную авторизацию'):
            assert response.status_code == 200, (
                f"Ожидался код 200, получен {response.status_code}"
            )
            
            response_json = response.json()
            assert "id" in response_json, "В ответе должен быть id курьера"
            
            courier_id = response_json["id"]
            assert isinstance(courier_id, int), f"ID должен быть числом, получен {type(courier_id)}"
            assert courier_id > 0, f"ID должен быть положительным числом, получен {courier_id}"
        
        cleanup_courier(payload["login"], payload["password"])
    
    @allure.title('Авторизация без логина')
    def test_login_without_login_fails(self, cleanup_courier):
        """Проверка авторизации без логина"""
        payload = create_courier_payload()
        
        with allure.step('Зарегистрировать курьера'):
            reg_response = requests.post(
                BASE_URL + Endpoints.COURIER_CREATE,
                data=payload
            )
            assert reg_response.status_code == 201, "Курьер должен быть создан"
        
        with allure.step('Отправить запрос без логина'):
            bad_payload = {"password": payload["password"]}
            response = requests.post(
                BASE_URL + Endpoints.COURIER_LOGIN,
                data=bad_payload
            )
        
        with allure.step('Проверить ошибку'):
            assert response.status_code != 200, (
                "Запрос без логина должен завершиться ошибкой"
            )
            assert response.status_code >= 400, (
                f"Ожидалась ошибка 4xx, получен {response.status_code}"
            )
        
        cleanup_courier(payload["login"], payload["password"])
    
    @allure.title('Авторизация без пароля')
    def test_login_without_password_fails(self, cleanup_courier):
        """Проверка авторизации без пароля"""
        payload = create_courier_payload()
        
        with allure.step('Зарегистрировать курьера'):
            reg_response = requests.post(
                BASE_URL + Endpoints.COURIER_CREATE,
                data=payload
            )
            assert reg_response.status_code == 201, "Курьер должен быть создан"
        
        with allure.step('Отправить запрос без пароля'):
            bad_payload = {"login": payload["login"]}
            response = requests.post(
                BASE_URL + Endpoints.COURIER_LOGIN,
                data=bad_payload
            )
        
        with allure.step('Проверить ошибку'):
            assert response.status_code != 200, (
                "Запрос без пароля должен завершиться ошибкой"
            )
            assert response.status_code >= 400, (
                f"Ожидалась ошибка 4xx, получен {response.status_code}"
            )
        
        cleanup_courier(payload["login"], payload["password"])
    
    @allure.title('Авторизация с неверным логином')
    def test_login_with_wrong_login_fails(self, cleanup_courier):
        """Проверка авторизации с неверным логином"""
        payload = create_courier_payload()
        
        with allure.step('Зарегистрировать курьера'):
            reg_response = requests.post(
                BASE_URL + Endpoints.COURIER_CREATE,
                data=payload
            )
            assert reg_response.status_code == 201, "Курьер должен быть создан"
        
        with allure.step('Авторизоваться с неверным логином'):
            bad_payload = {
                "login": f"wrong_{payload['login']}",
                "password": payload["password"]
            }
            response = requests.post(
                BASE_URL + Endpoints.COURIER_LOGIN,
                data=bad_payload
            )
        
        with allure.step('Проверить ошибку'):
            assert response.status_code == 404, (
                f"Ожидался код 404, получен {response.status_code}"
            )
        
        cleanup_courier(payload["login"], payload["password"])
    
    @allure.title('Авторизация с неверным паролем')
    def test_login_with_wrong_password_fails(self, cleanup_courier):
        """Проверка авторизации с неверным паролем"""
        payload = create_courier_payload()
        
        with allure.step('Зарегистрировать курьера'):
            reg_response = requests.post(
                BASE_URL + Endpoints.COURIER_CREATE,
                data=payload
            )
            assert reg_response.status_code == 201, "Курьер должен быть создан"
        
        with allure.step('Авторизоваться с неверным паролем'):
            bad_payload = {
                "login": payload["login"],
                "password": f"wrong_{payload['password']}"
            }
            response = requests.post(
                BASE_URL + Endpoints.COURIER_LOGIN,
                data=bad_payload
            )
        
        with allure.step('Проверить ошибку'):
            assert response.status_code == 404, (
                f"Ожидался код 404, получен {response.status_code}"
            )
        
        cleanup_courier(payload["login"], payload["password"])
    
    @allure.title('Авторизация под несуществующим пользователем')
    def test_login_nonexistent_courier_fails(self):
        """Проверка авторизации несуществующего курьера"""
        with allure.step('Авторизоваться с несуществующими данными'):
            payload = {
                "login": f"nonexistent_{generate_random_string(8)}",
                "password": f"nonexistent_{generate_random_string(8)}"
            }
            response = requests.post(
                BASE_URL + Endpoints.COURIER_LOGIN,
                data=payload
            )
        
        with allure.step('Проверить ошибку'):
            assert response.status_code == 404, (
                f"Ожидался код 404, получен {response.status_code}"
            )