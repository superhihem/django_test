from .models import Trade, Author


class JsonValidationResult():
    errors = {}
    def is_valid(self):
        return len(self.errors) == 0

# Самодельная валидация JSON. На момент написания так было проще.
# можно подумать над реализацией общего класса для валидации JSON для любых моделей или найти уже готовое решение
def ValidateTradeJson(json_dict) -> JsonValidationResult:
    validation_result = JsonValidationResult()

    required_fields = {
        "author_id": "автор",
        "title": "заголовок",
        "text": "текст объявления",
        "status": "статус",
    }

    for field_code in required_fields:
        if field_code not in json_dict:
            validation_result.errors[field_code] = {
                "errors": ["missing field"]
            }

    return validation_result

def ValidateEditTradeJson(json_dict) -> JsonValidationResult:
    validation_result = JsonValidationResult()

    non_editable_fields = {
        "author_id": "автор",
        "create_date": "дата создания",
        "update_date": "дата обновления"
    }

    for field_code in non_editable_fields:
        if field_code in json_dict:
            validation_result.errors[field_code] = {
                "errors": ["field is not editable"]
            }

    return validation_result
