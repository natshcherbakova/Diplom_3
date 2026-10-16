from selenium.webdriver.common.by import By


# локаторы ленты заказов
class OrdersFeedPageLocators:

    # заголовок страницы «Лента заказов»
    ORDERS_FEED_TITLE = (By.XPATH, "//h1[text()='Лента заказов']")

    # карточки заказов в ленте
    ORDER_CARDS = (
        By.XPATH,
        "//ul[contains(@class, 'OrderFeed_list')]"
        "/li[contains(@class, 'OrderHistory_listItem')]"
    )

    # ссылка на заказ в ленте (открывает окно с деталями)
    ORDER_LINK = (
        By.XPATH,
        "//li[contains(@class, 'OrderHistory_listItem')]"
        "//a[contains(@class, 'OrderHistory_link')]"
    )

    # всплывающее окно с деталями заказа
    ORDER_DETAILS_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_orderBox__')]")

    # надпись «Все текущие заказы готовы!» в колонке «В работе»: пока она видна, новый заказ ещё не попал в колонку
    ALL_CURRENT_ORDERS_READY = (By.XPATH, "//li[text()='Все текущие заказы готовы!']")

    # номера заказов только из колонки «В работе:» (не из «Готовы:»)
    # ВНИМАНИЕ: построен по догадке о разметке, нужно сверить с DevTools
    ORDERS_IN_PROGRESS = (By.XPATH, "//p[text()='В работе:']/following-sibling::ul/li")

    # счётчик «Выполнено за все время»
    ALL_TIME_ORDERS_COUNTER = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")

    # счётчик «Выполнено за сегодня»
    TODAY_ORDERS_COUNTER = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
