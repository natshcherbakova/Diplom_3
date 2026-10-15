class Urls:

    # главная страница (конструктор)
    MAIN_URL = "https://qa-stellarburgers.education-services.ru/"

    # остальные страницы: полные адреса, чтобы не склеивать строки в тестах
    ORDER_FEED_URL = MAIN_URL + "feed"
    LOGIN_URL = MAIN_URL + "login"
    PROFILE_URL = MAIN_URL + "account/profile"
    ORDER_HISTORY_URL = MAIN_URL + "account/order-history"
    FORGOT_PASSWORD_URL = MAIN_URL + "forgot-password"
    RESET_PASSWORD_URL = MAIN_URL + "reset-password"
