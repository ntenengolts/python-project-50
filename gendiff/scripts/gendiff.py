import argparse
import json
import yaml

from gendiff.parser import read_file
from gendiff.formatters.stylish import format_stylish
from gendiff.formatters.plain import format_plain
from gendiff.formatters.json import format_json


def format_value(value, depth=0):
    """
    Форматирует значение для отображения.
    """
    if isinstance(value, dict):
        indent = "    " * (depth + 1)
        lines = ["{"]
        for key, val in value.items():
            lines.append(f"{indent}{key}: {format_value(val, depth + 1)}")
        lines.append("    " * depth + "}")
        return "\n".join(lines)
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return "null"
    else:
        return str(value)

#  Далее изначальная структура функции (до шага 7)

#    if isinstance(value, bool):
#        return str(value).lower()
#    return value


def build_diff(data1, data2):
    """
    Построение дерева различий между двумя структурами.
    """
    keys = sorted(set(data1.keys()).union(data2.keys()))
    diff = []

    for key in keys:
        if key in data1 and key in data2:
            if isinstance(data1[key], dict) and isinstance(data2[key], dict):
                # Рекурсивно строим diff для вложенных структур
                children = build_diff(data1[key], data2[key])
                diff.append({"key": key, "type": "nested", "children": children})
            elif data1[key] == data2[key]:
                diff.append({"key": key, "type": "unchanged", "value": data1[key]})
            else:
                diff.append({
                    "key": key,
                    "type": "changed",
                    "value_before": data1[key],
                    "value_after": data2[key],
                })
        elif key in data1:
            diff.append({"key": key, "type": "removed", "value": data1[key]})
        elif key in data2:
            diff.append({"key": key, "type": "added", "value": data2[key]})

    return diff


def generate_diff(file_path1, file_path2, format_name='stylish'):
    # Чтение данных из JSON или YAML файлов
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)

    # Построение дерева различий (шаг 7)
    diff = build_diff(data1, data2)
#    print(f"DEBUG: diff = {diff}")

    # Форматирование результата (шаг 7)
    if format_name == 'stylish':
        return format_stylish(diff)
    elif format_name == 'plain':
        result = format_plain(diff)
#        print(f"DEBUG: result = {result}")
        return result
    elif format_name == 'json':
        return format_json(diff)
    else:
        raise ValueError(f"Неизвестный форматер: {format_name}")

# Далее изначальная структура функции (до шага 7)

#    all_keys = sorted(set(data1.keys()).union(data2.keys()))

#    result = ["{"]

#    for key in all_keys:

#        if key in data1 and key in data2:
#            if data1[key] == data2[key]:
#                result.append(f"    {key}: {format_value(data1[key])}")
#            else:
#                result.append(f"  - {key}: {format_value(data1[key])}")
#                result.append(f"  + {key}: {data2[key]}")

#        elif key in data1:
#            result.append(f"  - {key}: {format_value(data1[key])}")

#        elif key in data2:
#            result.append(f"  + {key}: {format_value(data2[key])}")

#    result.append("}")

#    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser(
        prog="gendiff",
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file", help="The first file to compare")
    parser.add_argument("second_file", help="The second file to compare")

    # Добавляем опцию --format для выбора формата вывода
    parser.add_argument(
        "-f", "--format",
        choices=["stylish", "plain", "json"],  # доступные форматы
        default="stylish",  # формат по умолчанию
        help="set format of output"
    )

    # Парсим аргументы
    args = parser.parse_args()

    diff = generate_diff(args.first_file, args.second_file, format_name=args.format)
    print(diff)


if __name__ == "__main__":
    main()
