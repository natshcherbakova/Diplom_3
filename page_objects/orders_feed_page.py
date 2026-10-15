import allure

from selenium.webdriver.support import expected_conditions as EC

from locators.orders_feed_page_locators import OrdersFeedPageLocators
from page_objects.base_page import BasePage
from urls import Urls


class OrdersFeedPage(BasePage):

    URL = Urls.ORDER_FEED_URL

    # период счётчика -> локатор
    COUNTERS = {
        "all_time": OrdersFeedPageLocators.ALL_TIME_ORDERS_COUNTER,
        "today": OrdersFeedPageLocators.TODAY_ORDERS_COUNTER,
    }

    # проверяет, что открыта лента заказов (по URL)
    @allure.step("Проверяем, что открыта лента заказов")
    def is_orders_feed_page_opened(self):
        return self.is_url_opened(Urls.ORDER_FEED_URL)

    # проверяет, что виден заголовок «Лента заказов»
    @allure.step("Проверяем отображение заголовка «Лента заказов»")
    def is_orders_feed_title_displayed(self):
        return self.is_element_visible(OrdersFeedPageLocators.ORDERS_FEED_TITLE)

    # кликает по заказу в ленте, чтобы открыть окно с деталями
    @allure.step("Открываем окно с деталями заказа")
    def click_order(self):
        self.click_to_element(OrdersFeedPageLocators.ORDER_LINK)

    # проверяет, что окно с деталями заказа открылось
    @allure.step("Проверяем отображение окна с деталями заказа")
    def is_order_details_displayed(self):
        return self.is_element_visible(OrdersFeedPageLocators.ORDER_DETAILS_MODAL)

    # ждёт, пока заказ с указанным номером появится среди карточек ленты: True, если появился, иначе False
    @allure.step("Проверяем наличие заказа в ленте")
    def is_order_in_feed(self, order_number):
        expected = f"#{self.to_feed_order_number(order_number)}"

        def order_present(driver):
            cards = driver.find_elements(*OrdersFeedPageLocators.ORDER_CARDS)
            return any(expected in card.text for card in cards)

        return self.wait_until_true(order_present)

    # возвращает значение счётчика «Выполнено за всё время» или «за сегодня» (period) как число
    @allure.step("Получаем значение счётчика заказов")
    def get_orders_counter(self, period):
        return int(self.get_text_from_element(self.COUNTERS[period]))

    # ждёт, пока счётчик станет больше начального значения: True, если стал, иначе False
    @allure.step("Ожидаем увеличения счётчика заказов")
    def is_orders_counter_increased(self, period, initial_value):
        return self.wait_until_true(
            lambda driver: self.get_orders_counter(period) > initial_value
        )

    # сначала ждёт, пока исчезнет надпись «Все текущие заказы готовы!» (особенность сайта),
    # затем ждёт, пока номер заказа появится в колонке «В работе»: True, если появился, иначе False
    @allure.step("Проверяем наличие заказа в разделе «В работе»")
    def is_order_in_progress(self, order_number):
        expected = self.to_feed_order_number(order_number)

        self.wait_until_true(
            EC.invisibility_of_element_located(OrdersFeedPageLocators.ALL_CURRENT_ORDERS_READY)
        )

        def order_present(driver):
            items = driver.find_elements(*OrdersFeedPageLocators.ORDERS_IN_PROGRESS)
            return expected in [item.text for item in items]

        return self.wait_until_true(order_present)
