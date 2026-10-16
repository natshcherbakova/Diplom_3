import allure

from selenium.webdriver.support import expected_conditions as EC

from data import IngredientNames
from locators.main_page_locators import MainPageLocators
from page_objects.base_page import BasePage
from urls import Urls


class MainPage(BasePage):

    URL = Urls.MAIN_URL

    # пока заказ создаётся, в окне показывается заглушка
    PLACEHOLDER_ORDER_NUMBER = "9999"

    # JS-скрипт перетаскивания: сам отправляет события HTML5 drag-and-drop.
    # ActionChains.drag_and_drop в Firefox не вызывает такие события, поэтому
    # перетаскивание через него там не срабатывает. Между событиями пауза 50 мс,
    # чтобы React успел обработать каждый шаг
    DRAG_AND_DROP_SCRIPT = """
        const source = arguments[0];
        const target = arguments[1];
        const done = arguments[arguments.length - 1];
        const dataTransfer = new DataTransfer();

        const fire = (element, type) => {
            const rect = element.getBoundingClientRect();
            element.dispatchEvent(new DragEvent(type, {
                bubbles: true,
                cancelable: true,
                dataTransfer: dataTransfer,
                clientX: rect.left + rect.width / 2,
                clientY: rect.top + rect.height / 2
            }));
        };

        const steps = [
            [source, 'dragstart'],
            [target, 'dragenter'],
            [target, 'dragover'],
            [target, 'drop'],
            [source, 'dragend']
        ];

        let index = 0;
        const next = () => {
            if (index >= steps.length) {
                done();
                return;
            }
            const [element, type] = steps[index++];
            fire(element, type);
            setTimeout(next, 50);
        };
        next();
    """

    # проверяет, что открыта главная страница (по URL)
    @allure.step("Проверяем, что открыта главная страница")
    def is_main_page_opened(self):
        return self.is_url_opened(Urls.MAIN_URL)

    # проверяет, что виден заголовок «Соберите бургер»
    @allure.step("Проверяем отображение заголовка конструктора")
    def is_constructor_title_displayed(self):
        return self.is_element_visible(MainPageLocators.CONSTRUCTOR_TITLE)

    # ---------- окно с деталями ингредиента ----------

    # кликает по карточке ингредиента с указанным названием, чтобы открыть окно с деталями
    @allure.step("Открываем окно с деталями ингредиента")
    def click_ingredient(self, ingredient_name):
        locator = self.format_locator(MainPageLocators.INGREDIENT_CARD, ingredient_name)
        self.click_to_element(locator)

    # проверяет, что открылось окно с деталями именно этого ингредиента (по названию в окне)
    @allure.step("Проверяем, что открыто окно с деталями нужного ингредиента")
    def is_ingredient_details_opened(self, ingredient_name):
        locator = self.format_locator(MainPageLocators.INGREDIENT_MODAL_NAME, ingredient_name)
        return self.is_element_visible(locator)

    # закрывает окно с деталями ингредиента кликом по крестику
    @allure.step("Закрываем окно с деталями ингредиента")
    def close_ingredient_modal(self):
        self.click_to_element(MainPageLocators.MODAL_CLOSE_BUTTON)

    # ждёт исчезновения окна с деталями этого ингредиента: True, если окно закрылось, иначе False
    @allure.step("Проверяем закрытие окна с деталями ингредиента")
    def is_ingredient_details_closed(self, ingredient_name):
        locator = self.format_locator(MainPageLocators.INGREDIENT_MODAL_NAME, ingredient_name)
        return self.wait_until_true(EC.invisibility_of_element_located(locator))

    # ---------- сборка бургера и счётчики ----------

    # перетаскивает карточку ингредиента в область сборки бургера через JS (работает и в Chrome, и в Firefox)
    def _drag_to_basket(self, ingredient_name):
        card = self.find_element(
            self.format_locator(MainPageLocators.INGREDIENT_CARD, ingredient_name)
        )
        basket = self.find_element(MainPageLocators.BURGER_BASKET)
        self.driver.execute_async_script(self.DRAG_AND_DROP_SCRIPT, card, basket)

    # возвращает значение счётчика на карточке ингредиента; если счётчика нет, возвращает 0
    def _get_counter(self, ingredient_name):
        locator = self.format_locator(MainPageLocators.INGREDIENT_COUNTER, ingredient_name)
        counters = self.driver.find_elements(*locator)
        return int(counters[0].text.strip()) if counters else 0

    # перетаскивает ингредиент (булку или начинку) с указанным названием в область сборки бургера
    @allure.step("Добавляем ингредиент в заказ")
    def add_ingredient_to_order(self, ingredient_name):
        self._drag_to_basket(ingredient_name)

    # собирает бургер: добавляет булку и начинку и ждёт, что оба счётчика выросли (иначе сразу падает здесь, а не при оформлении)
    @allure.step("Собираем бургер из булки и начинки")
    def create_burger(self):
        bun_before = self._get_counter(IngredientNames.BUN)
        self.add_ingredient_to_order(IngredientNames.BUN)
        self.wait.until(lambda driver: self._get_counter(IngredientNames.BUN) > bun_before)

        filling_before = self._get_counter(IngredientNames.FILLING)
        self.add_ingredient_to_order(IngredientNames.FILLING)
        self.wait.until(lambda driver: self._get_counter(IngredientNames.FILLING) > filling_before)

    # возвращает текущее значение счётчика ингредиента (булки или начинки) с указанным названием
    @allure.step("Получаем значение счётчика ингредиента")
    def get_ingredient_counter(self, ingredient_name):
        return self._get_counter(ingredient_name)

    # ждёт, пока счётчик ингредиента станет равен value: True, если стал, иначе False
    @allure.step("Ожидаем нужное значение счётчика ингредиента")
    def is_ingredient_counter_equal_to(self, ingredient_name, value):
        return self.wait_until_true(lambda driver: self._get_counter(ingredient_name) == value)

    # ---------- оформление заказа ----------

    # нажимает кнопку «Оформить заказ»
    @allure.step("Нажимаем кнопку «Оформить заказ»")
    def click_order_button(self):
        self.click_to_element(MainPageLocators.ORDER_BUTTON)

    # проверяет, что видно окно «Ваш заказ начали готовить»
    @allure.step("Проверяем отображение окна подтверждения заказа")
    def is_order_confirmation_displayed(self):
        return self.is_element_visible(MainPageLocators.ORDER_MODAL)

    # читает номер заказа из окна; возвращает его, если это не заглушка, иначе False
    def _read_real_order_number(self, driver):
        elements = driver.find_elements(*MainPageLocators.ORDER_CONFIRMATION_NUMBER)
        if elements:
            text = elements[0].text.strip()
            if text and text != self.PLACEHOLDER_ORDER_NUMBER:
                return text
        return False

    # ждёт настоящий номер заказа в окне и возвращает его; при таймауте падает с исключением
    @allure.step("Ожидаем появления настоящего номера заказа и получаем его")
    def get_order_number(self):
        return self.wait.until(self._read_real_order_number)

    # проверяет, что в окне показан настоящий номер заказа, а не заглушка
    @allure.step("Проверяем, что в окне показан настоящий номер заказа")
    def is_real_order_number_displayed(self):
        return self.wait_until_true(self._read_real_order_number)

    # собирает бургер, оформляет заказ и возвращает его номер
    @allure.step("Создаём заказ через конструктор и получаем его номер")
    def create_order_and_get_number(self):
        self.create_burger()
        self.click_order_button()
        return self.get_order_number()

    # закрывает окно подтверждения заказа и ждёт, пока оно исчезнет
    @allure.step("Закрываем окно подтверждения заказа")
    def close_order_modal(self):
        self.click_to_element(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.wait_until_invisible(MainPageLocators.ORDER_MODAL)
