
class API_KEY:
    __debug_mode = True
    __KEY = None

    @staticmethod
    def get_api_key():
        if API_KEY.__debug_mode:
            return 1
        else:
            return API_KEY.__KEY if API_KEY.__KEY else 1

    @staticmethod
    def to_string():
        return str(API_KEY.get_api_key())


class API_URL:
    @staticmethod
    def get_categories():
        return "https://www.themealdb.com/api/json/v1/" + API_KEY.to_string() + "/categories.php"

    @staticmethod
    def get_meals_by_category(category_name="Beef"):
        return "https://www.themealdb.com/api/json/v1/" + API_KEY.to_string() + "/filter.php?c=" + category_name

    @staticmethod
    def get_meal_details_by_id(meal_id):
        return "https://www.themealdb.com/api/json/v1/" + API_KEY.to_string() + "/lookup.php?i=" + str(meal_id)
