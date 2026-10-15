import allure


@allure.feature("Личный кабинет")
class TestPersonalAccount:

    @allure.title("Клик по «Личный кабинет» открывает профиль авторизованного пользователя")
    @allure.description(
        """
        1. Создаём нового пользователя через API;
        2. Открываем главную страницу и авторизуемся;
        3. Нажимаем кнопку «Личный кабинет»;
        4. Проверяем переход на страницу профиля.
        """
    )
    def test_personal_account_link_opens_profile(self, logged_in_main_page, profile_page):
        logged_in_main_page.click_personal_account()

        assert profile_page.is_profile_page_opened()

    @allure.title("Переход в «История заказов» показывает созданный заказ")
    @allure.description(
        """
        1. Создаём нового пользователя через API;
        2. Создаём заказ через API;
        3. Открываем главную страницу и авторизуемся;
        4. Нажимаем кнопку «Личный кабинет»;
        5. Нажимаем ссылку «История заказов»;
        6. Проверяем переход на страницу истории заказов;
        7. Проверяем, что номер созданного заказа отображается в истории.
        """
    )
    def test_order_history_shows_user_order(
        self, logged_in_main_page, profile_page, create_order
    ):
        logged_in_main_page.click_personal_account()
        profile_page.click_order_history()

        assert profile_page.is_order_history_page_opened()
        assert profile_page.is_order_in_history(create_order["order"]["number"])

    @allure.title("Выход из аккаунта возвращает на страницу входа")
    @allure.description(
        """
        1. Создаём нового пользователя через API;
        2. Открываем главную страницу и авторизуемся;
        3. Переходим в личный кабинет;
        4. Нажимаем кнопку «Выход»;
        5. Проверяем переход на страницу авторизации;
        6. Проверяем отображение заголовка «Вход».
        """
    )
    def test_logout_opens_login_page(
        self, logged_in_main_page, profile_page, auth_page
    ):
        logged_in_main_page.click_personal_account()
        profile_page.click_logout()

        assert auth_page.is_login_page_opened()
        assert auth_page.is_login_title_displayed()
