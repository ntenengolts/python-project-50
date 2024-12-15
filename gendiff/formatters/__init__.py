from gendiff.formatters.json import format_json
from gendiff.formatters.plain import format_plain
from gendiff.formatters.stylish import format_stylish


def choice_format(diff, format_name):
    # Форматирование результата
    if format_name == 'stylish':
        return format_stylish(diff)
    elif format_name == 'plain':
        result = format_plain(diff)
        return result
    elif format_name == 'json':
        return format_json(diff)
    else:
        raise ValueError(f"Неизвестный форматер: {format_name}")
