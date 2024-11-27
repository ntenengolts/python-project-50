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


def format_plain(diff):
    """
    Форматирует дерево различий в плоский текстовый вид (plain).
    """
    def walk(node, path=""):
        lines = []
        for changes in node:
            key = changes["key"]
            current_path = f"{path}.{key}" if path else key
            type = changes["type"]

            if type == "added":
                value = format_value(changes.get("value"))
                lines.append(
                    f"Property '{current_path}' was added with value: {value}"
                )
            elif type == "removed":
                lines.append(f"Property '{current_path}' was removed")
            elif type in {"updated", "changed"}:
                old_value = format_value(changes.get("value_before"))
                new_value = format_value(changes.get("value_after"))
                lines.append(
                    f"Property '{current_path}' was updated. "
                    f"From {old_value} to {new_value}"
                )
            elif type == "nested":
                lines.extend(walk(changes.get("children", []), current_path))
        return lines

    return "\n".join(walk(diff))
