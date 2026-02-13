import pytest
import allure
from helpers import create_order, get_orders_list


@allure.feature('Создание заказа')
class TestOrderCreation:
    
    @allure.title('Создание заказа с цветом BLACK')
    def test_create_order_with_black_color(self):
        response = create_order(["BLACK"])
        
        assert response.status_code == 201
        assert "track" in response.json()
    
    @allure.title('Создание заказа с цветом GREY')
    def test_create_order_with_grey_color(self):
        response = create_order(["GREY"])
        
        assert response.status_code == 201
        assert "track" in response.json()
    
    @allure.title('Создание заказа с обоими цветами')
    def test_create_order_with_both_colors(self):
        response = create_order(["BLACK", "GREY"])
        
        assert response.status_code == 201
        assert "track" in response.json()
    
    @allure.title('Создание заказа без указания цвета')
    def test_create_order_without_color(self):
        response = create_order(None)
        
        assert response.status_code == 201
        assert "track" in response.json()
    
    @allure.title('Создание заказа с пустым списком цветов')
    def test_create_order_with_empty_color_list(self):
        response = create_order([])
        
        assert response.status_code == 201
        assert "track" in response.json()


@allure.feature('Список заказов')
class TestOrdersList:
    
    @allure.title('Получение списка заказов возвращает 200 и список orders')
    def test_get_orders_list_returns_correct_structure(self):
        response = get_orders_list()
        
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)