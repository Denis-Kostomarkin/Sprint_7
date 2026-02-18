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

        response_data = response.json()
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert "id" in response_data, f"В ответе отсутствует поле 'id'. Ответ: {response_data}"
        assert isinstance(response_data["id"], int), f"Поле 'id' должно быть числом. Получено: {type(response_data['id'])}"
    
    @allure.title('Авторизация без логина возвращает 400')
    def test_login_without_login_fails(self, courier_credentials):
        password = courier_credentials["password"]
        
        bad_payload = {"password": password}
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=bad_payload
        )

        response_data = response.json()
        
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert "message" in response_data, f"В ответе отсутствует поле 'message'. Ответ: {response_data}"
        assert len(response_data["message"]) > 0, "Поле 'message' не должно быть пустым"
    
    @allure.title('Авторизация без пароля возвращает 400')
    def test_login_without_password_fails(self, courier_credentials):
        login = courier_credentials["login"]
        
        bad_payload = {"login": login}
        response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=bad_payload
        )

        response_data = response.json()
        
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert "message" in response_data, f"В ответе отсутствует поле 'message'. Ответ: {response_data}"
        assert len(response_data["message"]) > 0, "Поле 'message' не должно быть пустым"
    
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

        response_data = response.json()
        
        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
        assert "message" in response_data, f"В ответе отсутствует поле 'message'. Ответ: {response_data}"
        assert "Учетная запись не найдена" in response_data["message"] or "not found" in response_data["message"].lower(), \
            f"Ожидалось сообщение об ошибке 'Учетная запись не найдена', получено: {response_data['message']}"
    
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

        response_data = response.json()
        
        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
        assert "message" in response_data, f"В ответе отсутствует поле 'message'. Ответ: {response_data}"
        assert "Учетная запись не найдена" in response_data["message"] or "not found" in response_data["message"].lower(), \
            f"Ожидалось сообщение об ошибке 'Учетная запись не найдена', получено: {response_data['message']}"
    
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

        response_data = response.json()
        
        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
        assert "message" in response_data, f"В ответе отсутствует поле 'message'. Ответ: {response_data}"
        assert "Учетная запись не найдена" in response_data["message"] or "not found" in response_data["message"].lower(), \
            f"Ожидалось сообщение об ошибке 'Учетная запись не найдена', получено: {response_data['message']}"