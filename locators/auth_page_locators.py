from selenium.webdriver.common.by import By


# локаторы страницы авторизации
class AuthPageLocators:

    # заголовок формы «Вход»
    LOGIN_TITLE = (By.XPATH, "//h2[text()='Вход']")

    # поле для ввода email
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::input")

    # поле для ввода пароля
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")

    # кнопка «Войти»
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")

    # ссылка «Восстановить пароль»
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[@href='/forgot-password']")
