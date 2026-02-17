import pytest
import allure
import shutil
import os
from helpers import delete_courier, create_courier_payload, register_new_courier


@pytest.fixture
def courier_credentials():
    """Фикстура создает курьера и возвращает его credentials.
    НЕ содержит assert - только подготовку данных."""
    payload = create_courier_payload()
    login = payload["login"]
    password = payload["password"]
    
    register_new_courier(login, password, payload["firstName"])
    
    yield {"login": login, "password": password}
    
    delete_courier(login, password)


@pytest.fixture
def existing_courier_login():
    """Фикстура создает курьера и возвращает только login."""
    payload = create_courier_payload()
    login = payload["login"]
    password = payload["password"]
    
    register_new_courier(login, password, payload["firstName"])
    
    yield login
    
    delete_courier(login, password)
