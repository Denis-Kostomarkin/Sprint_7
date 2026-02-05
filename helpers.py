import random
import string
import allure
import requests
from config import BASE_URL, Endpoints


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


def create_courier_payload(login=None, password=None, first_name=None):
    return {
        "login": login or generate_random_string(10),
        "password": password or generate_random_string(10),
        "firstName": first_name or generate_random_string(10)
    }


def delete_courier(login, password):
    # Сначала авторизуемся, чтобы получить ID
    login_payload = {"login": login, "password": password}
    
    with allure.step(f"Авторизация для удаления курьера {login}"):
        login_response = requests.post(
            BASE_URL + Endpoints.COURIER_LOGIN,
            data=login_payload
        )
    
    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        
        with allure.step(f"Удаление курьера ID: {courier_id}"):
            response = requests.delete(
                BASE_URL + Endpoints.COURIER_DELETE.format(courier_id=courier_id)
            )
            return response
    
    return None


def create_order(color=None):
    payload = {
        "firstName": "Denchick",
        "lastName": "Slazit",
        "address": "Leninsky prospekt 3",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2024-06-06",
        "comment": "Всем привет",
        "color": color if color else []
    }
    
    with allure.step(f"Создание заказа с цветом: {color}"):
        response = requests.post(
            BASE_URL + Endpoints.ORDER_CREATE,
            json=payload
        )
    
    return response


def get_orders_list(limit=30, page=0):
    params = {"limit": limit, "page": page}
    
    with allure.step("Получение списка заказов"):
        response = requests.get(
            BASE_URL + Endpoints.ORDERS_LIST,
            params=params
        )
    
    return response