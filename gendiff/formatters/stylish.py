def format_value(value, depth):
    """
    Преобразует значение в строку с учетом отступов.
    """
    if isinstance(value, dict):
        indent = "    " * (depth + 1)
        lines = [
            f"{indent}{key}: "
            f"{format_value(val, depth + 1)}" for key, val in value.items()
        ]
        return "{\n" + "\n".join(lines) + f"\n{'    ' * depth}}}"
    return str(value).lower() if isinstance(
        value, bool) else str(value) if value is not None else "null"


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

        handler = {
            "nested": handle_nested,
            "added": handle_added,
            "removed": handle_removed,
            "changed": handle_changed,
            "unchanged": handle_unchanged,
        }.get(type_)

        if handler:
            result.extend(handler(node, key, indent, current_indent, depth))

    result.append(indent + "}")
    return "\n".join(result)


# Вспомогательные функции для обработки каждого типа узлов
def handle_nested(node, key, indent, current_indent, depth):
    """
    Обрабатывает узел с типом 'nested'.
    """
    children = format_stylish(node["children"], depth + 1)
    return [f"{current_indent}{key}: {children}"]


def handle_added(node, key, indent, current_indent, depth):
    """
    Обрабатывает узел с типом 'added'.
    """
    return [
        f"{indent}  + {key}: {format_value(node['value'], depth + 1)}"
    ]


def handle_removed(node, key, indent, current_indent, depth):
    """
    Обрабатывает узел с типом 'removed'.
    """
    return [
        f"{indent}  - {key}: {format_value(node['value'], depth + 1)}"
    ]


def handle_changed(node, key, indent, current_indent, depth):
    """
    Обрабатывает узел с типом 'changed'.
    """
    return [
        f"{indent}  - {key}: {format_value(node['value_before'], depth + 1)}",
        f"{indent}  + {key}: {format_value(node['value_after'], depth + 1)}",
    ]


def handle_unchanged(node, key, indent, current_indent, depth):
    """
    Обрабатывает узел с типом 'unchanged'.
    """
    return [
        f"{current_indent}{key}: {format_value(node['value'], depth + 1)}"
    ]
