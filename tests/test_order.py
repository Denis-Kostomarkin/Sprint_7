import pytest
import requests
import allure
from helpers import create_order, get_orders_list
from config import BASE_URL, Endpoints


@allure.feature('Создание заказа')
class TestOrderCreation:
    
    @allure.title('Создание заказа с черным цветом')
    def test_create_order_with_black_color(self):
        """Проверка создания заказа с цветом BLACK"""
        color = ["BLACK"]
        
        with allure.step(f'Создать заказ с цветом: {color}'):
            response = create_order(color)
        
        with allure.step('Проверить ответ сервера'):
            assert response.status_code == 201, (
                f"Ожидался код 201, получен {response.status_code}"
            )
            
            response_json = response.json()
            assert "track" in response_json, "В ответе должен быть track номер"
            
            track_number = response_json["track"]
            assert isinstance(track_number, int), f"Track должен быть числом, получен {type(track_number)}"
            assert track_number > 0, f"Track должен быть положительным числом, получен {track_number}"
    
    @allure.title('Создание заказа с серым цветом')
    def test_create_order_with_grey_color(self):
        """Проверка создания заказа с цветом GREY"""
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
        """Проверка создания заказа с обоими цветами"""
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
        """Проверка создания заказа без указания цвета"""
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
        """Проверка создания заказа с пустым списком цветов"""
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
    
    @allure.title('Получение списка заказов')
    def test_get_orders_list(self):
        """Проверка получения списка заказов"""
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
            
            if len(orders_list) > 0:
                first_order = orders_list[0]
                assert "id" in first_order, "Заказ должен содержать id"
                assert "track" in first_order, "Заказ должен содержать track"