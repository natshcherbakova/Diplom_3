from selenium.webdriver.common.by import By


# локаторы личного кабинета
class ProfilePageLocators:

    # ссылка «История заказов»
    ORDER_HISTORY_LINK = (By.XPATH, "//a[@href='/account/order-history']")

    # заказ в истории: блок с номером и датой создания
    ORDER_HISTORY_ITEM = (By.XPATH, "//div[contains(@class, 'OrderHistory_textBox')]")

    # кнопка «Выход»
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
