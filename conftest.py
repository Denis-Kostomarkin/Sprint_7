import pytest
import requests
from helpers import register_new_courier_and_return_login_password, delete_courier

@pytest.fixture
def base_url():
    return "https://qa-scooter.praktikum-services.ru"

@pytest.fixture
def create_courier():
    """Фикстура для создания курьера перед тестом"""
    courier_data = register_new_courier_and_return_login_password()
    yield courier_data
    if courier_data:
        login, password, first_name = courier_data
        delete_courier(login, password)