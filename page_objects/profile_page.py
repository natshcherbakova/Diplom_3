import allure

from locators.profile_page_locators import ProfilePageLocators
from page_objects.base_page import BasePage
from urls import Urls


class ProfilePage(BasePage):

    URL = Urls.PROFILE_URL

    # нажимает ссылку «История заказов» в личном кабинете
    @allure.step("Переходим к истории заказов")
    def click_order_history(self):
        self.wait_for_modal_to_close()
        self.click_to_element(ProfilePageLocators.ORDER_HISTORY_LINK)

    # нажимает кнопку «Выход»
    @allure.step("Нажимаем кнопку «Выход»")
    def click_logout(self):
        self.click_to_element(ProfilePageLocators.LOGOUT_BUTTON)

    # проверяет, что открыт личный кабинет (по URL)
    @allure.step("Проверяем, что открыт личный кабинет")
    def is_profile_page_opened(self):
        return self.is_url_opened(Urls.PROFILE_URL)

    # проверяет, что открыта история заказов (по URL)
    @allure.step("Проверяем, что открыта история заказов")
    def is_order_history_page_opened(self):
        return self.is_url_opened(Urls.ORDER_HISTORY_URL)

    # ждёт, пока заказ с указанным номером появится в истории: True, если появился, иначе False
    @allure.step("Проверяем наличие заказа в истории")
    def is_order_in_history(self, order_number):
        expected = f"#{self.to_feed_order_number(order_number)}"

        def order_present(driver):
            items = driver.find_elements(*ProfilePageLocators.ORDER_HISTORY_ITEM)
            return any(expected in item.text for item in items)

        return self.wait_until_true(order_present)
