import allure
import pytest


@allure.feature("Лента заказов")
class TestOrdersFeed:

    @allure.title("Клик по заказу в ленте открывает окно с деталями")
    @allure.description(
        """
        1. Открываем главную страницу Stellar Burgers;
        2. Нажимаем ссылку «Лента заказов»;
        3. Нажимаем на заказ в ленте;
        4. Проверяем отображение всплывающего окна с деталями заказа.
        """
    )
    def test_click_order_opens_details_modal(self, main_page, orders_feed_page):
        main_page.open()
        main_page.click_orders_feed()
        orders_feed_page.click_order()

        assert orders_feed_page.is_order_details_displayed()

    @allure.title("Заказ пользователя из «Истории заказов» отображается в ленте")
    @allure.description(
        """
        1. Создаём нового пользователя через API;
        2. Создаём заказ через API;
        3. Открываем главную страницу и авторизуемся;
        4. Переходим в личный кабинет;
        5. Переходим в раздел «История заказов»;
        6. Открываем раздел «Лента заказов»;
        7. Проверяем отображение созданного заказа в ленте.
        """
    )
    def test_user_order_from_history_appears_in_feed(
        self, logged_in_main_page, profile_page, orders_feed_page, create_order
    ):
        logged_in_main_page.click_personal_account()
        profile_page.click_order_history()
        profile_page.click_orders_feed()

        assert orders_feed_page.is_order_in_feed(create_order["order"]["number"])

    @allure.title("Счётчик «Выполнено» увеличивается после создания заказа")
    @allure.description(
        """
        1. Создаём нового пользователя через API;
        2. Открываем главную страницу и авторизуемся;
        3. Открываем раздел «Лента заказов»;
        4. Запоминаем начальное значение счётчика («за всё время» или «за сегодня»);
        5. Переходим в «Конструктор» и создаём новый заказ;
        6. Закрываем окно подтверждения заказа;
        7. Открываем раздел «Лента заказов»;
        8. Проверяем, что значение счётчика увеличилось.
        """
    )
    @pytest.mark.parametrize("period", ["all_time", "today"])
    def test_orders_counter_increases_after_new_order(
        self, logged_in_main_page, orders_feed_page, period
    ):
        logged_in_main_page.click_orders_feed()
        counter_before = orders_feed_page.get_orders_counter(period)
        orders_feed_page.click_constructor()
        logged_in_main_page.create_order_and_get_number()
        logged_in_main_page.close_order_modal()
        logged_in_main_page.click_orders_feed()

        assert orders_feed_page.is_orders_counter_increased(period, counter_before)

    @allure.title("Номер нового заказа появляется в разделе «В работе»")
    @allure.description(
        """
        1. Создаём нового пользователя через API;
        2. Открываем главную страницу и авторизуемся;
        3. Создаём новый заказ через конструктор и запоминаем его номер;
        4. Закрываем окно подтверждения заказа;
        5. Открываем раздел «Лента заказов»;
        6. Проверяем, что номер заказа появился в разделе «В работе».
        """
    )
    def test_new_order_number_appears_in_progress_section(
        self, logged_in_main_page, orders_feed_page
    ):
        order_number = logged_in_main_page.create_order_and_get_number()
        logged_in_main_page.close_order_modal()
        logged_in_main_page.click_orders_feed()

        assert orders_feed_page.is_order_in_progress(order_number)
