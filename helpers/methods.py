import allure
import requests

from urls import Urls
from helpers.endpoints import Endpoints


class UserMethods:

    @staticmethod
    @allure.step("Создание пользователя")
    def create_user(user_data):
        response = requests.post(
            Urls.MAIN_URL + Endpoints.create_user,
            json=user_data
        )

        return response

    @staticmethod
    @allure.step("Удаление пользователя")
    def delete_user(access_token):
        response = requests.delete(
            Urls.MAIN_URL + Endpoints.delete_user,
            headers={"Authorization": access_token}
        )

        return response


class OrderMethods:

    @staticmethod
    @allure.step("Создание заказа через API")
    def create_order(order_data, access_token):
        response = requests.post(
            Urls.MAIN_URL + Endpoints.create_order,
            json=order_data,
            headers={"Authorization": access_token}
        )

        return response
    