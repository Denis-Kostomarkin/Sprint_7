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

        response_data = response.json()
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "ok" in response_data, f"В ответе отсутствует поле 'ok'. Ответ: {response_data}"
        assert response_data["ok"] is True, f"Поле 'ok' должно быть true, получено: {response_data['ok']}"
        
        delete_courier(login, password)
    
    @allure.title('Создание курьера с существующим логином возвращает 409')
    def test_create_courier_with_existing_login_fails(self, courier_credentials):
        existing_login = courier_credentials["login"]
        
        payload2 = create_courier_payload(
            login=existing_login,
            password=generate_random_string(10),
            first_name=generate_random_string(10)
        )
        response2 = requests.post(
            BASE_URL + Endpoints.COURIER_CREATE,
            data=payload2
        )

        response_data = response2.json()
        
        assert response2.status_code == 409, f"Ожидался статус 409, получен {response2.status_code}"
        assert "message" in response_data, f"В ответе отсутствует поле 'message'. Ответ: {response_data}"
        assert "логин уже используется" in response_data["message"].lower(), \
            f"Ожидалось сообщение 'логин уже используется', получено: {response_data['message']}"
    
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

        response_data = response.json()
        
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert "message" in response_data, f"В ответе отсутствует поле 'message'. Ответ: {response_data}"
        assert len(response_data["message"]) > 0, "Поле 'message' не должно быть пустым"
    
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

        response_data = response.json()
        
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert "message" in response_data, f"В ответе отсутствует поле 'message'. Ответ: {response_data}"
        assert len(response_data["message"]) > 0, "Поле 'message' не должно быть пустым"