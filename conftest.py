import pytest
import allure
import shutil
import os
from helpers import delete_courier


@pytest.fixture
def courier_credentials():
    from helpers import create_courier_payload, register_new_courier
    
    # Создаем данные курьера
    payload = create_courier_payload()
    login = payload["login"]
    password = payload["password"]
    
    # Регистрируем курьера
    response = register_new_courier(login, password, payload["firstName"])
    assert response.status_code == 201, f"Не удалось создать курьера: {response.status_code}"
    
    # Передаем данные в тест
    yield {"login": login, "password": password}
    
    # Удаляем курьера после теста
    delete_courier(login, password)


@pytest.fixture
def existing_courier_login():
    from helpers import create_courier_payload, register_new_courier
    
    payload = create_courier_payload()
    login = payload["login"]
    password = payload["password"]
    
    response = register_new_courier(login, password, payload["firstName"])
    assert response.status_code == 201
    
    yield login
    
    delete_courier(login, password)
