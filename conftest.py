import pytest
import allure
import shutil
import os
from helpers import delete_courier


@pytest.fixture
def cleanup_courier():
    courier_data = None
    
    def _save_courier_data(login, password):
        nonlocal courier_data
        courier_data = {"login": login, "password": password}
    yield _save_courier_data
    
    if courier_data:
        with allure.step(f"Очистка: удаление курьера {courier_data['login']}"):
            try:
                delete_result = delete_courier(
                    courier_data["login"], 
                    courier_data["password"]
                )
                if delete_result and delete_result.status_code == 200:
                    allure.attach(
                        f"Курьер {courier_data['login']} успешно удален", 
                        name="Успешная очистка"
                    )
            except Exception as e:
                allure.attach(
                    f"Ошибка при удалении курьера: {str(e)}", 
                    name="Исключение при очистке"
                )
