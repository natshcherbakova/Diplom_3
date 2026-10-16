import allure
import pytest

from data import IngredientNames


@allure.feature("Конструктор")
class TestConstructor:

    @allure.title("Переход в «Конструктор» из ленты заказов")
    @allure.description(
        """
        1. Открываем главную страницу Stellar Burgers;
        2. Нажимаем ссылку «Лента заказов»;
        3. Нажимаем ссылку «Конструктор»;
        4. Проверяем, что открыта главная страница;
        5. Проверяем отображение заголовка «Соберите бургер».
        """
    )
    def test_constructor_link_opens_main_page(self, main_page):
        main_page.open()
        main_page.click_orders_feed()
        main_page.click_constructor()

        assert main_page.is_main_page_opened()
        assert main_page.is_constructor_title_displayed()

    @allure.title("Переход в «Ленту заказов»")
    @allure.description(
        """
        1. Открываем главную страницу Stellar Burgers;
        2. Нажимаем ссылку «Лента заказов»;
        3. Проверяем URL страницы;
        4. Проверяем отображение заголовка «Лента заказов».
        """
    )
    def test_orders_feed_link_opens_orders_feed(self, main_page, orders_feed_page):
        main_page.open()
        main_page.click_orders_feed()

        assert orders_feed_page.is_orders_feed_page_opened()
        assert orders_feed_page.is_orders_feed_title_displayed()

    @allure.title("Клик по ингредиенту открывает окно с его деталями")
    @allure.description(
        """
        1. Открываем главную страницу Stellar Burgers;
        2. Нажимаем на ингредиент (булку или начинку);
        3. Проверяем, что открылось окно «Детали ингредиента»;
        4. Проверяем, что в окне показано название именно этого ингредиента.
        """
    )
    @pytest.mark.parametrize(
        "ingredient_name",
        [
            pytest.param(IngredientNames.BUN, id="bun"),
            pytest.param(IngredientNames.FILLING, id="filling"),
        ]
    )
    def test_click_ingredient_opens_details_modal(self, main_page, ingredient_name):
        main_page.open()
        main_page.click_ingredient(ingredient_name)

        assert main_page.is_ingredient_details_opened(ingredient_name)

    @allure.title("Клик по крестику закрывает окно с деталями ингредиента")
    @allure.description(
        """
        1. Открываем главную страницу Stellar Burgers;
        2. Нажимаем на ингредиент;
        3. Нажимаем на крестик в окне с деталями;
        4. Проверяем, что окно закрылось.
        """
    )
    def test_close_button_closes_ingredient_details_modal(self, main_page):
        main_page.open()
        main_page.click_ingredient(IngredientNames.FILLING)
        main_page.close_ingredient_modal()

        assert main_page.is_ingredient_details_closed(IngredientNames.FILLING)

    @pytest.mark.parametrize(
        "ingredient_name, expected_increase",
        [
            pytest.param(IngredientNames.FILLING, 1, id="ingredient-counter"),
            pytest.param(IngredientNames.BUN, 2, id="bun-counter"),
        ]
    )
    @allure.title("Счётчик ингредиентов увеличивается после добавления в заказ")
    @allure.description(
        """
        1. Открываем главную страницу Stellar Burgers;
        2. Запоминаем начальное значение счётчика;
        3. Добавляем ингредиент в область сборки бургера;
        4. Проверяем увеличение счётчика на ожидаемое значение.
        """
    )
    def test_counter_increases_after_adding(
        self, main_page, ingredient_name, expected_increase
    ):
        main_page.open()
        counter_before = main_page.get_ingredient_counter(ingredient_name)
        main_page.add_ingredient_to_order(ingredient_name)

        assert main_page.is_ingredient_counter_equal_to(
            ingredient_name, counter_before + expected_increase
        )

    @allure.title("Авторизованный пользователь может оформить заказ")
    @allure.description(
        """
        1. Создаём тестового пользователя через API;
        2. Открываем главную страницу и авторизуемся;
        3. Собираем бургер из булки и начинки;
        4. Нажимаем кнопку «Оформить заказ»;
        5. Проверяем отображение окна подтверждения заказа;
        6. Проверяем, что в окне показан настоящий номер заказа.
        """
    )
    def test_logged_in_user_can_place_order(self, logged_in_main_page):
        logged_in_main_page.create_burger()
        logged_in_main_page.click_order_button()

        assert logged_in_main_page.is_order_confirmation_displayed()
        assert logged_in_main_page.is_real_order_number_displayed()
