from selenium.webdriver.common.by import By


# локаторы страниц восстановления и сброса пароля
class ForgotPasswordPageLocators:

    # поле для ввода email
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::input")

    # кнопка «Восстановить»
    RESTORE_BUTTON = (By.XPATH, "//button[text()='Восстановить']")

    # заголовок страницы сброса «Восстановление пароля»
    RESET_PASSWORD_TITLE = (By.XPATH, "//h2[text()='Восстановление пароля']")

    # контейнер поля «Введите новый пароль»: на нём появляется класс активного состояния
    PASSWORD_INPUT_CONTAINER = (By.XPATH, "//input[@name='Введите новый пароль']/parent::div")

    # иконка показать/скрыть пароль
    SHOW_PASSWORD_BUTTON = (
        By.XPATH,
        "//input[@name='Введите новый пароль']"
        "/following-sibling::div[contains(@class, 'input__icon-action')]"
    )
