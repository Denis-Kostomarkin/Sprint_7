import requests
import allure
from helpers import create_courier_payload, register_new_courier, delete_courier, generate_random_string
from config import BASE_URL, Endpoints


@allure.feature('Авторизация курьера')
class TestCourierLogin:
    
    @allure.title('Авторизация с корректными данными возвращает 200 и id')
    def test_login_courier_success(self):
        payload = create_courier_payload()
        login = payload["login"]
        password = payload["password"]
        first_name = payload["firstName"]
        
        response_reg = register_new_courier(login, password, first_name)
        assert response_reg.status_code == 201
        
        login_payload = {"login": login, "password": password}
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=login_payload
        )
        
        assert response.status_code == 200
        assert "id" in response.json()
        
        delete_courier(login, password)
    
    @allure.title('Авторизация без логина возвращает 400')
    def test_login_without_login_fails(self):
        payload = create_courier_payload()
        login = payload["login"]
        password = payload["password"]
        first_name = payload["firstName"]
        
        response_reg = register_new_courier(login, password, first_name)
        assert response_reg.status_code == 201
        
        bad_payload = {"password": password}
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=bad_payload
        )
        
        assert response.status_code == 400
        
        delete_courier(login, password)
    
    @allure.title('Авторизация без пароля возвращает 400')
    def test_login_without_password_fails(self):
        payload = create_courier_payload()
        login = payload["login"]
        password = payload["password"]
        first_name = payload["firstName"]
        
        response_reg = register_new_courier(login, password, first_name)
        assert response_reg.status_code == 201
        
        bad_payload = {"login": login}
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=bad_payload
        )
        
        assert response.status_code == 400
        
        delete_courier(login, password)
    
    @allure.title('Авторизация с неверным логином возвращает 404')
    def test_login_with_wrong_login_fails(self):
        payload = create_courier_payload()
        login = payload["login"]
        password = payload["password"]
        first_name = payload["firstName"]
        
        response_reg = register_new_courier(login, password, first_name)
        assert response_reg.status_code == 201
        
        bad_payload = {
            "login": f"wrong_{login}",
            "password": password
        }
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=bad_payload
        )
        
        assert response.status_code == 404
        
        delete_courier(login, password)
    
    @allure.title('Авторизация с неверным паролем возвращает 404')
    def test_login_with_wrong_password_fails(self):
        payload = create_courier_payload()
        login = payload["login"]
        password = payload["password"]
        first_name = payload["firstName"]
        
        response_reg = register_new_courier(login, password, first_name)
        assert response_reg.status_code == 201
        
        bad_payload = {
            "login": login,
            "password": f"wrong_{password}"
        }
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=bad_payload
        )
        
        assert response.status_code == 404
        
        delete_courier(login, password)
    
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