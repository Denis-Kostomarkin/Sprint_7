import requests
import allure
from helpers import create_courier_payload, register_new_courier, delete_courier, generate_random_string
from config import BASE_URL, Endpoints


@allure.feature('Создание курьера')
class TestCourierCreation:
    
    @allure.title('Успешное создание курьера возвращает 201 и ok:true')
    def test_create_courier_success(self):
        payload = create_courier_payload()
        login = payload["login"]
        password = payload["password"]
        first_name = payload["firstName"]
        
        response = register_new_courier(login, password, first_name)
        
        assert response.status_code == 201
        assert response.json()["ok"] is True
        
        delete_courier(login, password)
    
    @allure.title('Создание курьера с существующим логином возвращает 409')
    def test_create_courier_with_existing_login_fails(self):
        payload = create_courier_payload()
        login = payload["login"]
        password = payload["password"]
        first_name = payload["firstName"]
        
        response1 = register_new_courier(login, password, first_name)
        assert response1.status_code == 201
        
        payload2 = create_courier_payload(
            login=login,
            password=generate_random_string(10),
            first_name=generate_random_string(10)
        )
        response2 = requests.post(
            BASE_URL + Endpoints.COURIER_CREATE,
            data=payload2
        )
        
        assert response2.status_code == 409
        assert "логин уже используется" in response2.json()["message"]
        
        delete_courier(login, password)
    
    @allure.title('Создание курьера без логина возвращает 400')
    def test_create_courier_without_login_fails(self):
        payload = {
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        response = requests.post(
            BASE_URL + Endpoints.COURIER_CREATE,
            data=payload
        )
        
        assert response.status_code == 400
    
    @allure.title('Создание курьера без пароля возвращает 400')
    def test_create_courier_without_password_fails(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        response = requests.post(
            BASE_URL + Endpoints.COURIER_CREATE,
            data=payload
        )
        
        assert response.status_code == 400