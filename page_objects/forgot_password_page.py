import allure

from locators.forgot_password_page_locators import ForgotPasswordPageLocators
from page_objects.base_page import BasePage
from urls import Urls


class ForgotPasswordPage(BasePage):

    URL = Urls.FORGOT_PASSWORD_URL

    # класс контейнера, который означает «поле активно / подсвечено»
    ACTIVE_CLASS = "input_status_active"

    # вводит email в поле на странице восстановления пароля
    @allure.step("Вводим email для восстановления пароля")
    def enter_email(self, email):
        self.add_text_to_element(ForgotPasswordPageLocators.EMAIL_INPUT, email)

    # нажимает кнопку «Восстановить»
    @allure.step("Нажимаем кнопку «Восстановить»")
    def click_restore_button(self):
        self.click_to_element(ForgotPasswordPageLocators.RESTORE_BUTTON)

    # нажимает иконку показать/скрыть пароль в поле пароля
    @allure.step("Нажимаем иконку показать/скрыть пароль")
    def click_show_password(self):
        self.click_to_element(ForgotPasswordPageLocators.SHOW_PASSWORD_BUTTON)

    # ждёт перехода на страницу сброса пароля; при таймауте падает с исключением
    @allure.step("Ожидаем перехода на страницу сброса пароля")
    def wait_for_reset_password_page(self):
        self.wait.until(lambda driver: driver.current_url == Urls.RESET_PASSWORD_URL)

    # проверяет, что открыта страница восстановления пароля (по URL)
    @allure.step("Проверяем, что открыта страница восстановления пароля")
    def is_forgot_password_page_opened(self):
        return self.is_url_opened(Urls.FORGOT_PASSWORD_URL)

    # проверяет, что открыта страница сброса пароля (по URL)
    @allure.step("Проверяем, что открыта страница сброса пароля")
    def is_reset_password_page_opened(self):
        return self.is_url_opened(Urls.RESET_PASSWORD_URL)

    # проверяет, что на странице виден заголовок «Восстановление пароля»
    @allure.step("Проверяем отображение заголовка страницы сброса пароля")
    def is_reset_password_title_displayed(self):
        return self.is_element_visible(ForgotPasswordPageLocators.RESET_PASSWORD_TITLE)

    # сразу (без ожидания) проверяет, подсвечено ли поле пароля, по классу контейнера
    @allure.step("Проверяем текущее состояние поля пароля (без ожидания)")
    def is_password_input_active_now(self):
        container = self.find_element(ForgotPasswordPageLocators.PASSWORD_INPUT_CONTAINER)
        return self.ACTIVE_CLASS in container.get_attribute("class")

    # ждёт, пока поле пароля станет подсвеченным: True, если стало, иначе False
    @allure.step("Ожидаем, что поле пароля станет активным")
    def is_password_input_active(self):
        return self.wait_until_true(lambda driver: self.is_password_input_active_now())
