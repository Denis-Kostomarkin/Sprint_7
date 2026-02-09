import pytest
import requests
import allure
from helpers import create_order, get_orders_list


@allure.feature('Создание заказа')
class TestOrderCreation:
    
    @allure.title('Создание заказа с черным цветом')
    def test_create_order_with_black_color(self):
        color = ["BLACK"]
        
        with allure.step(f'Создать заказ с цветом: {color}'):
            response = create_order(color)
        
        with allure.step('Проверить ответ сервера'):
            assert response.status_code == 201, (
                f"Ожидался код 201, получен {response.status_code}"
            )
            assert "track" in response.json(), "В ответе должен быть track номер"
    
    @allure.title('Создание заказа с серым цветом')
    def test_create_order_with_grey_color(self):
        color = ["GREY"]
        
        with allure.step(f'Создать заказ с цветом: {color}'):
            response = create_order(color)
        
        with allure.step('Проверить ответ сервера'):
            assert response.status_code == 201, (
                f"Ожидался код 201, получен {response.status_code}"
            )
            assert "track" in response.json(), "В ответе должен быть track номер"
    
    @allure.title('Создание заказа с обоими цветами')
    def test_create_order_with_both_colors(self):
        color = ["BLACK", "GREY"]
        
        with allure.step(f'Создать заказ с цветом: {color}'):
            response = create_order(color)
        
        with allure.step('Проверить ответ сервера'):
            assert response.status_code == 201, (
                f"Ожидался код 201, получен {response.status_code}"
            )
            assert "track" in response.json(), "В ответе должен быть track номер"
    
    @allure.title('Создание заказа без указания цвета')
    def test_create_order_without_color(self):
        color = None
        
        with allure.step('Создать заказ без указания цвета'):
            response = create_order(color)
        
        with allure.step('Проверить ответ сервера'):
            assert response.status_code == 201, (
                f"Ожидался код 201, получен {response.status_code}"
            )
            assert "track" in response.json(), "В ответе должен быть track номер"
    
    @allure.title('Создание заказа с пустым списком цветов')
    def test_create_order_with_empty_color_list(self):
        color = []
        
        with allure.step(f'Создать заказ с цветом: {color}'):
            response = create_order(color)
        
        with allure.step('Проверить ответ сервера'):
            assert response.status_code == 201, (
                f"Ожидался код 201, получен {response.status_code}"
            )
            assert "track" in response.json(), "В ответе должен быть track номер"


@allure.feature('Список заказов')
class TestOrdersList:
    
    @allure.title('Получение списка заказов возвращает корректную структуру')
    def test_get_orders_list_returns_correct_structure(self):
        with allure.step('Получить список заказов'):
            response = get_orders_list()
        
        with allure.step('Проверить ответ сервера'):
            assert response.status_code == 200, (
                f"Ожидался код 200, получен {response.status_code}"
            )
            
            response_json = response.json()
            assert "orders" in response_json, "В ответе должен быть ключ 'orders'"
            
            orders_list = response_json["orders"]
            assert isinstance(orders_list, list), "Orders должен быть списком"