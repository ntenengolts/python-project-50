def format_value(value, depth):
    """
    Преобразует значение в строку с учетом отступов.
    """
    if isinstance(value, dict):
        indent = "    " * (depth + 1)
        lines = [f"{indent}{key}: {format_value(val, depth + 1)}" for key, val in value.items()]
        return "{\n" + "\n".join(lines) + f"\n{'    ' * depth}}}"
    return str(value).lower() if isinstance(value, bool) else str(value) if value is not None else "null"


def format_stylish(diff, depth=0):
    """
    Форматирует внутреннее дерево различий в стиль 'stylish'.
    """
    indent = "    " * depth  # Базовый отступ для текущей глубины
    result = ["{"]

    for node in diff:
        key = node["key"]
        type_ = node["type"]
        current_indent = indent + "    "  # Отступ для текущего уровня

        if type_ == "nested":
            # Рекурсивно обрабатываем дочерние элементы
            children = format_stylish(node["children"], depth + 1)
            result.append(f"{current_indent}{key}: {children}")
        elif type_ == "added":
            result.append(f"{indent}  + {key}: {format_value(node['value'], depth + 1)}")
        elif type_ == "removed":
            result.append(f"{indent}  - {key}: {format_value(node['value'], depth + 1)}")
        elif type_ == "changed":
            result.append(f"{indent}  - {key}: {format_value(node['value_before'], depth + 1)}")
            result.append(f"{indent}  + {key}: {format_value(node['value_after'], depth + 1)}")
        elif type_ == "unchanged":
            result.append(f"{current_indent}{key}: {format_value(node['value'], depth + 1)}")

    result.append(indent + "}")
    return "\n".join(result)
