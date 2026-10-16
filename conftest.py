import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from data import UserData, Ingredients, RecoveryData
from helpers.methods import UserMethods, OrderMethods

from page_objects.main_page import MainPage
from page_objects.auth_page import AuthPage
from page_objects.forgot_password_page import ForgotPasswordPage
from page_objects.profile_page import ProfilePage
from page_objects.orders_feed_page import OrdersFeedPage


# фабрика драйверов: по названию браузера создаёт драйвер с нужными опциями
class DriverFactory:

    @staticmethod
    def get_driver(browser: str, headless: bool):
        if browser == "chrome":
            options = ChromeOptions()

            if headless:
                options.add_argument("--headless=new")

            options.add_argument("--window-size=1920,1080")

            driver = webdriver.Chrome(options=options)

        elif browser == "firefox":
            options = FirefoxOptions()

            if headless:
                options.add_argument("-headless")

            options.add_argument("--width=1920")
            options.add_argument("--height=1080")

            driver = webdriver.Firefox(options=options)

        else:
            # неизвестный браузер: падаем сразу с понятным сообщением
            raise ValueError(f"Браузер «{browser}» не поддерживается. Доступны: chrome, firefox")

        return driver


# параметры командной строки:
#   --browser chrome | firefox | all  (по умолчанию all: тесты идут в обоих браузерах)
#   --headless                        (запуск браузера без окна)
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="all",
        choices=["chrome", "firefox", "all"],
        help="Браузер для запуска: chrome, firefox или all (оба)",
    )

    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск браузера без окна (headless)",
    )


# подставляет в фикстуру driver браузеры из параметра --browser:
# каждый тест запускается в каждом выбранном браузере
def pytest_generate_tests(metafunc):
    if "driver" in metafunc.fixturenames:
        browser = metafunc.config.getoption("--browser")
        browsers = ["chrome", "firefox"] if browser == "all" else [browser]

        metafunc.parametrize(
            "driver",
            browsers,
            indirect=True,
            ids=[name.capitalize() for name in browsers],
        )


# фикстура браузера: запускает драйвер перед тестом и закрывает его после.
# Название браузера приходит из pytest_generate_tests через request.param
@pytest.fixture
def driver(request):
    headless = request.config.getoption("--headless")
    browser = DriverFactory.get_driver(request.param, headless)
  
    yield browser
    
    browser.quit()


@pytest.fixture
def main_page(driver):
    return MainPage(driver)


# фикстура страницы авторизации: отдаёт тесту готовый объект AuthPage
@pytest.fixture
def auth_page(driver):
    return AuthPage(driver)


# фикстура страницы восстановления пароля: отдаёт тесту готовый объект ForgotPasswordPage
@pytest.fixture
def forgot_password_page(driver):
    return ForgotPasswordPage(driver)


# фикстура личного кабинета: отдаёт тесту готовый объект ProfilePage
@pytest.fixture
def profile_page(driver):
    return ProfilePage(driver)


# фикстура ленты заказов: отдаёт тесту готовый объект OrdersFeedPage
@pytest.fixture
def orders_feed_page(driver):
    return OrdersFeedPage(driver)


# фикстура тестового пользователя: до теста создаёт его через API,
# отдаёт тесту данные (name, email, password, access_token),
# а после теста удаляет пользователя, даже если тест упал
@pytest.fixture
def create_new_user():
    user_data = UserData.generate_user_data()

    response = UserMethods.create_user(user_data)
    access_token = response.json()["accessToken"]
    user_data["access_token"] = access_token

    yield user_data

    UserMethods.delete_user(access_token)


# фикстура заказа: создаёт заказ через API для тестового пользователя
# и отдаёт тесту ответ сервера (номер заказа: ['order']['number'])
@pytest.fixture
def create_order(create_new_user):
    response = OrderMethods.create_order(
        Ingredients.correct_ingredients_data,
        create_new_user["access_token"]
    )

    return response.json()


# фикстура-предусловие: создаёт пользователя через API, открывает главную страницу
# и авторизуется. Тест начинается с уже залогиненного пользователя
@pytest.fixture
def logged_in_main_page(main_page, auth_page, create_new_user):
    main_page.open()
    main_page.click_personal_account()
    auth_page.login(create_new_user["email"], create_new_user["password"])
    return main_page


# фикстура-предусловие: проходит путь до страницы сброса пароля
# (личный кабинет, «Восстановить пароль», ввод email, «Восстановить»)
# и отдаёт тесту страницу, на которой уже можно работать с полем пароля
@pytest.fixture
def reset_password_page(main_page, auth_page, forgot_password_page):
    main_page.open()
    main_page.click_personal_account()
    auth_page.click_forgot_password()
    forgot_password_page.enter_email(RecoveryData.EMAIL)
    forgot_password_page.click_restore_button()
    forgot_password_page.wait_for_reset_password_page()
    return forgot_password_page
