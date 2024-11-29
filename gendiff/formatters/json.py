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


def added_value(changes):
    """Возвращает форматированное добавленное значение."""
    return {"type": "added", "value": format_value(changes.get("value"))}


def removed_value():
    """Возвращает форматированное значение для удаления."""
    return {"type": "removed"}


def updated_value(changes):
    """Возвращает форматированное обновленное значение."""
    return {
        "type": "updated",
        "value_before": format_value(changes.get("value_before")),
        "value_after": format_value(changes.get("value_after"))
    }


def walk(node):
    result = {}
    for changes in node:
        key = changes["key"]
        type = changes["type"]

        if type == "added":
            result[key] = added_value(changes)
        elif type == "removed":
            result[key] = removed_value()
        elif type == "changed":
            result[key] = updated_value(changes)
        elif type == "nested":
            result[key] = walk(changes.get("children", []))

    return result


def format_json(diff):
    """
    Форматирует дерево различий в JSON-вывод,
    соответствующий ожидаемому формату.
    """
    return json.dumps(walk(diff), indent=4)
