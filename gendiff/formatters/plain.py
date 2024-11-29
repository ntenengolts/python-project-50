def format_value(value):
    """
    Преобразует значение в формат, соответствующий plain.
    """
    if isinstance(value, (dict, list)):
        return "[complex value]"
    elif isinstance(value, str):
        return f"'{value}'"
    elif value is None:
        return "null"
    else:
        return str(value).lower()


def added(key, changes, path):
    value = format_value(changes.get("value"))
    return f"Property '{path}' was added with value: {value}"


def removed(key, changes, path):
    return f"Property '{path}' was removed"


def updated(key, changes, path):
    old_value = format_value(changes.get("value_before"))
    new_value = format_value(changes.get("value_after"))
    return (
        f"Property '{path}' was updated. "
        f"From {old_value} to {new_value}"
    )


def walk(node, path=""):
    lines = []
    for changes in node:
        key = changes["key"]
        current_path = f"{path}.{key}" if path else key
        type = changes["type"]

        if type == "added":
            lines.append(added(key, changes, current_path))

        elif type == "removed":
            lines.append(removed(key, changes, current_path))

        elif type in {"updated", "changed"}:
            lines.append(updated(key, changes, current_path))

        elif type == "nested":
            lines.extend(walk(changes.get("children", []), current_path))
    return lines


def format_plain(diff):
    """
    Форматирует дерево различий в плоский текстовый вид (plain).
    """
    return "\n".join(walk(diff))
