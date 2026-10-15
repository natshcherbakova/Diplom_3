import allure

from locators.auth_page_locators import AuthPageLocators
from page_objects.base_page import BasePage
from urls import Urls


class AuthPage(BasePage):

    URL = Urls.LOGIN_URL

    # вводит email в поле на странице входа
    @allure.step("Вводим email")
    def enter_email(self, email):
        self.add_text_to_element(AuthPageLocators.EMAIL_INPUT, email)

    # вводит пароль в поле на странице входа
    @allure.step("Вводим пароль")
    def enter_password(self, password):
        self.add_text_to_element(AuthPageLocators.PASSWORD_INPUT, password)

    # нажимает кнопку «Войти»
    @allure.step("Нажимаем кнопку «Войти»")
    def click_login_button(self):
        self.click_to_element(AuthPageLocators.LOGIN_BUTTON)

    # вводит email и пароль, нажимает «Войти» и ждёт, пока форма входа исчезнет и закроется оверлей
    @allure.step("Выполняем авторизацию и ожидаем выхода со страницы входа")
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        self.wait_until_invisible(AuthPageLocators.LOGIN_BUTTON)
        # оверлей может ещё закрываться и перехватывать следующий клик
        self.wait_for_modal_to_close()

    # нажимает ссылку «Восстановить пароль»
    @allure.step("Переходим к восстановлению пароля")
    def click_forgot_password(self):
        self.click_to_element(AuthPageLocators.FORGOT_PASSWORD_LINK)

    # проверяет, что открыта страница авторизации (по URL)
    @allure.step("Проверяем, что открыта страница авторизации")
    def is_login_page_opened(self):
        return self.is_url_opened(Urls.LOGIN_URL)

    # проверяет, что на странице виден заголовок «Вход»
    @allure.step("Проверяем отображение заголовка «Вход»")
    def is_login_title_displayed(self):
        return self.is_element_visible(AuthPageLocators.LOGIN_TITLE)
