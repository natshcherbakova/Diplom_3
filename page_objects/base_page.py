import allure

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators.base_page_locators import BasePageLocators
from urls import Urls


class BasePage:

    # адрес страницы; в наследниках переопределяется
    URL = Urls.MAIN_URL

    # единый таймаут всех ожиданий
    TIMEOUT = 20

    # сохраняет драйвер и создаёт объект явного ожидания с общим таймаутом
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, self.TIMEOUT)

    # ---------- технические методы (без Allure-шагов, чтобы не раздувать отчёт) ----------

    # ждёт, пока условие выполнится: возвращает True, а при таймауте False (без исключения)
    def wait_until_true(self, condition):
        # возвращает True/False вместо исключения: удобно для assert в тестах
        try:
            self.wait.until(condition)
            return True
        except TimeoutException:
            return False

    # ждёт, пока элемент исчезнет или станет невидимым; при таймауте падает с исключением
    def wait_until_invisible(self, locator):
        self.wait.until(EC.invisibility_of_element_located(locator))

    # ждёт, пока элемент станет видимым, и возвращает его
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    # возвращает True, если элемент стал видимым за время ожидания, иначе False
    def is_element_visible(self, locator):
        return self.wait_until_true(EC.visibility_of_element_located(locator))

    # возвращает True, если текущий URL стал равен ожидаемому за время ожидания, иначе False
    def is_url_opened(self, url):
        return self.wait_until_true(EC.url_to_be(url))

    # ждёт, пока элемент станет кликабельным, и кликает по нему
    def click_to_element(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    # очищает поле ввода и вводит в него текст
    def add_text_to_element(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    # ждёт видимости элемента и возвращает его текст
    def get_text_from_element(self, locator):
        return self.find_element(locator).text

    # подставляет значение вместо {} в шаблоне локатора и возвращает готовый локатор
    @staticmethod
    def format_locator(locator, value):
        by, path = locator
        return by, path.format(value)

    # приводит номер заказа к виду, как он показан в ленте и истории (с ведущим нулём)
    @staticmethod
    def to_feed_order_number(number):
        # в ленте и истории номер заказа отображается с ведущим нулём: 12345 -> 012345
        return f"0{number}"

    # ---------- действия, общие для всех страниц ----------

    # открывает страницу по адресу из атрибута URL и ждёт, пока уйдёт оверлей загрузки,
    # иначе он может перехватить первый клик (особенно в Chrome при первой загрузке)
    @allure.step("Открываем страницу")
    def open(self):
        self.driver.get(self.URL)
        self.wait_for_modal_to_close()

    # кликает по ссылке «Личный кабинет» в шапке сайта
    @allure.step("Переходим в личный кабинет")
    def click_personal_account(self):
        self.click_to_element(BasePageLocators.PERSONAL_ACCOUNT_LINK)

    # кликает по ссылке «Конструктор» в шапке сайта
    @allure.step("Переходим в конструктор")
    def click_constructor(self):
        self.click_to_element(BasePageLocators.CONSTRUCTOR_LINK)

    # кликает по ссылке «Лента заказов» в шапке сайта
    @allure.step("Переходим в ленту заказов")
    def click_orders_feed(self):
        self.click_to_element(BasePageLocators.ORDERS_FEED_LINK)

    # ждёт, пока на странице не останется ни одного видимого оверлея модального окна
    # (чтобы он не перехватил следующий клик)
    @allure.step("Ожидаем закрытия модального окна")
    def wait_for_modal_to_close(self):
        def no_visible_overlay(driver):
            try:
                overlays = driver.find_elements(*BasePageLocators.MODAL_OVERLAY)
                return not any(overlay.is_displayed() for overlay in overlays)
            except StaleElementReferenceException:
                # элемент успел исчезнуть во время проверки: пробуем ещё раз
                return False

        self.wait.until(no_visible_overlay)
