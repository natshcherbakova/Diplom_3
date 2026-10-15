from selenium.webdriver.common.by import By


# локаторы главной страницы (конструктор бургеров)
class MainPageLocators:

    # заголовок конструктора
    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")

    # область сборки бургера
    BURGER_BASKET = (By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list')]")

    # карточка ингредиента по названию (шаблон: подставить название через format_locator)
    _INGREDIENT_CARD_XPATH = (
        "//a[contains(@class, 'BurgerIngredient_ingredient')"
        " and .//p[text()='{}']]"
    )
    INGREDIENT_CARD = (By.XPATH, _INGREDIENT_CARD_XPATH)

    # счётчик на карточке ингредиента по названию (шаблон)
    INGREDIENT_COUNTER = (
        By.XPATH,
        _INGREDIENT_CARD_XPATH + "//p[contains(@class, 'counter_counter__num')]"
    )

    # название ингредиента в ОТКРЫТОМ окне «Детали ингредиента» (шаблон: название подставляется
    # через format_locator). Окно открыто, пока у section есть класс Modal_modal_opened
    INGREDIENT_MODAL_NAME = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened')]"
        "//p[contains(@class, 'text_type_main-medium') and contains(@class, 'mb-8')"
        " and text()='{}']"
    )

    # кнопка «Оформить заказ»
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")

    # окно подтверждения заказа
    ORDER_MODAL = (By.XPATH, "//p[text()='Ваш заказ начали готовить']")

    # номер заказа в окне подтверждения
    ORDER_CONFIRMATION_NUMBER = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")

    # крестик закрытия любого модального окна (одинаковый компонент для ингредиента и заказа)
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
