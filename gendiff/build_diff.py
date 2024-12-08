def build_diff(data1, data2):
    """
    Построение дерева различий между двумя структурами.
    """
    keys = sorted(set(data1.keys()).union(data2.keys()))
    diff = []

    for key in keys:
        if key in data1 and key in data2:
            diff.append(handle_common_keys(data1, data2, key))
        elif key in data1:
            diff.append(handle_removed_key(data1, key))
        elif key in data2:
            diff.append(handle_added_key(data2, key))

    return diff


# Вспомогательные функции для обработки различных случаев
def handle_common_keys(data1, data2, key):
    """
    Обрабатывает ключи, присутствующие в обеих структурах.
    """
    if isinstance(data1[key], dict) and isinstance(data2[key], dict):
        # Если значения — вложенные словари, строим diff рекурсивно
        children = build_diff(data1[key], data2[key])
        return {"key": key, "type": "nested", "children": children}
    elif data1[key] == data2[key]:
        # Значения совпадают, добавляем как 'unchanged'
        return {"key": key, "type": "unchanged", "value": data1[key]}
    else:
        # Значения отличаются, добавляем как 'changed'
        return {
            "key": key,
            "type": "changed",
            "value_before": data1[key],
            "value_after": data2[key],
        }


def handle_removed_key(data1, key):
    """
    Обрабатывает ключи, которые есть только в первой структуре (удалённые).
    """
    return {"key": key, "type": "removed", "value": data1[key]}


def handle_added_key(data2, key):
    """
    Обрабатывает ключи, которые есть только во второй структуре (добавленные).
    """
    return {"key": key, "type": "added", "value": data2[key]}
