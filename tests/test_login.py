import pytest
import requests
import allure
from helpers import create_courier_payload, generate_random_string
from config import BASE_URL, Endpoints


@allure.feature('Авторизация курьера')
class TestCourierLogin:
    
    @allure.title('Успешная авторизация существующего курьера')
    def test_login_courier_success(self):
        payload = create_courier_payload()
        reg_response = requests.post(
            BASE_URL + Endpoints.COURIER_CREATE,
            data=payload
        )
        
        if reg_response.status_code != 201:
            pytest.skip(f"Не удалось создать курьера: {reg_response.status_code}")
        
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
        
        try:
            from helpers import delete_courier
            delete_courier(payload["login"], payload["password"])
        except:
            pass
    
    @allure.title('Авторизация без логина возвращает ошибку')
    def test_login_without_login_fails(self):
        payload = create_courier_payload()
        reg_response = requests.post(
            BASE_URL + Endpoints.COURIER_CREATE,
            data=payload
        )
        
        if reg_response.status_code != 201:
            pytest.skip(f"Не удалось создать курьера: {reg_response.status_code}")
        
        with allure.step('Отправить запрос без логина'):
            bad_payload = {"password": payload["password"]}
            response = requests.post(
                BASE_URL + Endpoints.COURIER_LOGIN,
                data=bad_payload
            )
        
        with allure.step('Проверить ошибку'):
            assert response.status_code == 400, (
                f"Ожидался код 400, получен {response.status_code}"
            )
        
        try:
            from helpers import delete_courier
            delete_courier(payload["login"], payload["password"])
        except:
            pass
    
    @allure.title('Авторизация без пароля возвращает ошибку')
    def test_login_without_password_fails(self):
        payload = create_courier_payload()
        reg_response = requests.post(
            BASE_URL + Endpoints.COURIER_CREATE,
            data=payload
        )
        
        if reg_response.status_code != 201:
            pytest.skip(f"Не удалось создать курьера: {reg_response.status_code}")
        
        with allure.step('Отправить запрос без пароля'):
            bad_payload = {"login": payload["login"]}
            response = requests.post(
                BASE_URL + Endpoints.COURIER_LOGIN,
                data=bad_payload
            )
        
        with allure.step('Проверить ошибку'):
            assert response.status_code == 400, (
                f"Ожидался код 400, получен {response.status_code}"
            )
        
        try:
            from helpers import delete_courier
            delete_courier(payload["login"], payload["password"])
        except:
            pass
    
    @allure.title('Авторизация с неверным логином возвращает ошибку')
    def test_login_with_wrong_login_fails(self):
        payload = create_courier_payload()
        reg_response = requests.post(
            BASE_URL + Endpoints.COURIER_CREATE,
            data=payload
        )
        
        if reg_response.status_code != 201:
            pytest.skip(f"Не удалось создать курьера: {reg_response.status_code}")
        
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
        
        try:
            from helpers import delete_courier
            delete_courier(payload["login"], payload["password"])
        except:
            pass
    
    @allure.title('Авторизация с неверным паролем возвращает ошибку')
    def test_login_with_wrong_password_fails(self):
        payload = create_courier_payload()
        reg_response = requests.post(
            BASE_URL + Endpoints.COURIER_CREATE,
            data=payload
        )
        
        if reg_response.status_code != 201:
            pytest.skip(f"Не удалось создать курьера: {reg_response.status_code}")
        
        with allure.step('Аворизоваться с неверным паролем'):
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
        
        try:
            from helpers import delete_courier
            delete_courier(payload["login"], payload["password"])
        except:
            pass
    
    @allure.title('Авторизация несуществующего курьера возвращает ошибку')
    def test_login_nonexistent_courier_fails(self):
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