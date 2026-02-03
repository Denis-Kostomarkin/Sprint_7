import requests
import random
import string
import allure

# метод регистрации нового курьера возвращает список из логина и пароля
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
    
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass

def login_courier(login, password):
    """Авторизация курьера"""
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
    return response

def delete_courier(login, password):
    """Удаление курьера"""
    # Сначала получаем ID курьера
    login_response = login_courier(login, password)
    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        # Удаляем курьера
        response = requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
        return response
    return None

def create_order(color=None):
    """Создание заказа"""
    payload = {
        "firstName": "Denchik",
        "lastName": "Slazit",
        "address": "Ленинский проспект 4",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2024-06-06",
        "comment": "Всем привет!",
        "color": color if color else []
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', json=payload)
    return response

def get_orders_list():
    """Получение списка заказов"""
    response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders')
    return response