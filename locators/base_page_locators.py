from selenium.webdriver.common.by import By


# локаторы элементов, которые есть на всех страницах
class BasePageLocators:

    # ссылка «Личный кабинет» в шапке
    PERSONAL_ACCOUNT_LINK = (By.XPATH, "//a[@href='/account']")

    # ссылка «Конструктор» в шапке
    CONSTRUCTOR_LINK = (By.XPATH, "//a[@href='/']")

    # ссылка «Лента заказов» в шапке
    ORDERS_FEED_LINK = (By.XPATH, "//a[@href='/feed']")

    # оверлей модального окна
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")
