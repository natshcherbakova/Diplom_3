from faker import Faker


class UserData:

    # генерация данных нового пользователя
    @staticmethod
    def generate_user_data():
        faker = Faker('ru_RU')
        data = {
            "name": faker.first_name(),
            "email": faker.email(),
            "password": faker.password()
        }
        return data


class RecoveryData:

    # email для проверки восстановления пароля
    EMAIL = "test@yandex.ru"


class IngredientNames:

    # названия ингредиентов, с которыми работают тесты конструктора
    BUN = "Краторная булка N-200i"
    FILLING = "Говяжий метеорит (отбивная)"


class Ingredients:

    # актуальные ID ингредиентов для создания заказа через API
    correct_ingredients_data = {
        "ingredients": [
            "6acef97852135b001b21a32b",  # Краторная булка N-200i
            "6acef97852135b001b21a32f"   # Говяжий метеорит (отбивная)
        ]
    }
