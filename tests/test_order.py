import pytest
import allure
from helpers import create_order, get_orders_list


@allure.feature('Создание заказа')
class TestOrderCreation:
    
    @pytest.mark.parametrize(
        "color",
        [
            pytest.param(["BLACK"], id="BLACK color"),
            pytest.param(["GREY"], id="GREY color"),
            pytest.param(["BLACK", "GREY"], id="both colors"),
            pytest.param(None, id="no color"),
            pytest.param([], id="empty color list")
        ]
    )
    @allure.title('Создание заказа с цветом: {color}')
    def test_create_order_with_various_colors(self, color):
        response = create_order(color)
        
        response_data = response.json()
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "track" in response_data, f"В ответе отсутствует поле 'track'. Ответ: {response_data}"
        assert isinstance(response_data["track"], int), f"Поле 'track' должно быть числом. Получено: {type(response_data['track'])}"


@allure.feature('Список заказов')
class TestOrdersList:
    
    @allure.title('Получение списка заказов возвращает 200 и список orders')
    def test_get_orders_list_returns_correct_structure(self):
        response = get_orders_list()
        
        response_data = response.json()
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert "orders" in response_data, f"В ответе отсутствует поле 'orders'. Ответ: {response_data}"
        assert isinstance(response_data["orders"], list), f"Поле 'orders' должно быть списком. Получено: {type(response_data['orders'])}"
        assert len(response_data["orders"]) > 0, "Список заказов не должен быть пустым"