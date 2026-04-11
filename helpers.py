import random
import string
import allure
import requests
from config import BASE_URL, Endpoints


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def create_courier_payload(login=None, password=None, first_name=None):
    return {
        "login": login or generate_random_string(10),
        "password": password or generate_random_string(10),
        "firstName": first_name or generate_random_string(10)
    }


@allure.step("Регистрация нового курьера")
def register_new_courier(login, password, first_name):
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(
        BASE_URL + Endpoints.COURIER_CREATE,
        data=payload
    )
    return response


@allure.step("Удаление курьера")
def delete_courier(login, password):
    login_payload = {"login": login, "password": password}
    login_response = requests.post(
        BASE_URL + Endpoints.COURIER_LOGIN,
        data=login_payload
    )
    
    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        response = requests.delete(
            BASE_URL + Endpoints.COURIER_DELETE.format(courier_id=courier_id)
        )
        return response
    return login_response


@allure.step("Создание заказа")
def create_order(color=None):
    payload = {
        "firstName": "Denchik",
        "lastName": "Slazit",
        "address": "Leninsky prospekt 3",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2024-06-06",
        "comment": "Привет всем!",
        "color": color if color else []
    }
    response = requests.post(
        BASE_URL + Endpoints.ORDER_CREATE,
        json=payload
    )
    return response


@allure.step("Получение списка заказов")
def get_orders_list(limit=30, page=0):
    params = {"limit": limit, "page": page}
    response = requests.get(
        BASE_URL + Endpoints.ORDERS_LIST,
        params=params
    )
    return response