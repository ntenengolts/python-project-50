import json


def format_value(value):
    """
    Преобразует значение в формат, который подходит для JSON.
    """
    if isinstance(value, (dict, list)):
        return value  # Для JSON вложенные структуры остаются без изменений
    elif value is None:
        return None  # Для JSON None напрямую преобразуется в null
    elif isinstance(value, bool):
        return value  # Булевые значения True/False корректно интерпретируются
    else:
        return value  # Все остальные типы остаются без изменений


def format_json(diff):
    """
    Форматирует дерево различий в JSON-вывод,
    соответствующий ожидаемому формату.
    """
    def walk(node):
        result = {}
        for changes in node:
            key = changes["key"]
            type = changes["type"]

            if type == "added":
                result[key] = {
                    "type": "added",
                    "value": format_value(changes.get("value"))
                }
            elif type == "removed":
                result[key] = {
                    "type": "removed"
                }
            elif type == "changed":  # Обработка изменений
                result[key] = {
                    "type": "updated",
                    "value_before": format_value(changes.get("value_before")),
                    "value_after": format_value(changes.get("value_after"))
                }
            elif type == "nested":
                result[key] = walk(changes.get("children", []))

        return result

    # Возвращаем отформатированный JSON в виде строки
    return json.dumps(walk(diff), indent=4)
