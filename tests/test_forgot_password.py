import allure

from data import RecoveryData


@allure.feature("Восстановление пароля")
class TestForgotPassword:

    @allure.title("Переход на страницу восстановления пароля по ссылке «Восстановить пароль»")
    @allure.description(
        """
        1. Открываем главную страницу Stellar Burgers;
        2. Переходим в личный кабинет (страница авторизации);
        3. Нажимаем ссылку «Восстановить пароль»;
        4. Проверяем переход на страницу восстановления пароля.
        """
    )
    def test_forgot_password_link_opens_recovery_page(
        self, main_page, auth_page, forgot_password_page
    ):
        main_page.open()
        main_page.click_personal_account()
        auth_page.click_forgot_password()

        assert forgot_password_page.is_forgot_password_page_opened()

    @allure.title("Ввод email и клик «Восстановить» открывает страницу сброса пароля")
    @allure.description(
        """
        1. Открываем главную страницу Stellar Burgers;
        2. Переходим в личный кабинет;
        3. Нажимаем ссылку «Восстановить пароль»;
        4. Вводим email;
        5. Нажимаем кнопку «Восстановить»;
        6. Проверяем переход на страницу сброса пароля;
        7. Проверяем отображение заголовка формы.
        """
    )
    def test_restore_button_opens_reset_password_page(
        self, main_page, auth_page, forgot_password_page
    ):
        main_page.open()
        main_page.click_personal_account()
        auth_page.click_forgot_password()
        forgot_password_page.enter_email(RecoveryData.EMAIL)
        forgot_password_page.click_restore_button()

        assert forgot_password_page.is_reset_password_page_opened()
        assert forgot_password_page.is_reset_password_title_displayed()

    @allure.title("Клик по иконке показать/скрыть пароль подсвечивает поле")
    @allure.description(
        """
        1. Открываем главную страницу Stellar Burgers;
        2. Переходим в личный кабинет;
        3. Нажимаем ссылку «Восстановить пароль»;
        4. Вводим email и нажимаем кнопку «Восстановить»;
        5. Ожидаем перехода на страницу сброса пароля;
        6. Проверяем, что поле пароля изначально не подсвечено;
        7. Нажимаем на иконку показать/скрыть пароль;
        8. Проверяем, что поле пароля стало активным (подсвечено).
        """
    )
    def test_show_password_icon_highlights_password_input(self, reset_password_page):
        assert not reset_password_page.is_password_input_active_now()

        reset_password_page.click_show_password()

        assert reset_password_page.is_password_input_active()
