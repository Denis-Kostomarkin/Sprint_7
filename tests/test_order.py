import pytest
import requests
import allure
from helpers import create_order, get_orders_list

@allure.feature('Создание заказа')
class TestOrderCreation:
    
    @allure.title('Создание заказа с разными цветами (параметризация)')
    @pytest.mark.parametrize('color', [
        (["BLACK"]),
        (["GREY"]),
        (["BLACK", "GREY"]),
        ([])
    ])
    def test_create_order_with_different_colors(self, base_url, color):
        """Проверка создания заказа с разными цветами"""
        with allure.step(f'Создать заказ с цветом: {color}'):
            response = create_order(color)
            
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
            assert "track" in response.json(), "В ответе должен быть track номер"
    
    @allure.feature('Список заказов')
    @allure.title('Получение списка заказов')
    def test_get_orders_list(self, base_url):
        """Проверка получения списка заказов"""
        with allure.step('Получить список заказов'):
            response = get_orders_list()
            
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            assert "orders" in response.json(), "В ответе должен быть список orders"
            assert isinstance(response.json()["orders"], list), "Orders должен быть списком"