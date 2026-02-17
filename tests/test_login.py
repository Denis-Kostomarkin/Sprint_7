import requests
import allure
from helpers import generate_random_string
from config import BASE_URL, Endpoints


@allure.feature('Авторизация курьера')
class TestCourierLogin:
    
    @allure.title('Авторизация с корректными данными возвращает 200 и id')
    def test_login_courier_success(self, courier_credentials):
        login = courier_credentials["login"]
        password = courier_credentials["password"]
        
        login_payload = {"login": login, "password": password}
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=login_payload
        )
        
        assert response.status_code == 200
        assert "id" in response.json()
    
    @allure.title('Авторизация без логина возвращает 400')
    def test_login_without_login_fails(self, courier_credentials):
        password = courier_credentials["password"]
        
        bad_payload = {"password": password}
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=bad_payload
        )
        
        assert response.status_code == 400
    
    @allure.title('Авторизация без пароля возвращает 400')
    def test_login_without_password_fails(self, courier_credentials):
        login = courier_credentials["login"]
        
        bad_payload = {"login": login}
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=bad_payload
        )
        
        assert response.status_code == 400
    
    @allure.title('Авторизация с неверным логином возвращает 404')
    def test_login_with_wrong_login_fails(self, courier_credentials):
        login = courier_credentials["login"]
        password = courier_credentials["password"]
        
        bad_payload = {
            "login": f"wrong_{login}",
            "password": password
        }
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=bad_payload
        )
        
        assert response.status_code == 404
    
    @allure.title('Авторизация с неверным паролем возвращает 404')
    def test_login_with_wrong_password_fails(self, courier_credentials):
        login = courier_credentials["login"]
        password = courier_credentials["password"]
        
        bad_payload = {
            "login": login,
            "password": f"wrong_{password}"
        }
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=bad_payload
        )
        
        assert response.status_code == 404
    
    @allure.title('Авторизация несуществующего курьера возвращает 404')
    def test_login_nonexistent_courier_fails(self):
        payload = {
            "login": f"nonexistent_{generate_random_string(8)}",
            "password": f"nonexistent_{generate_random_string(8)}"
        }
        
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=payload
        )
        
        assert response.status_code == 404