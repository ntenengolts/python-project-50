from gendiff.build_diff import build_diff
from gendiff.formatters import choice_format
from gendiff.parser import read_file


def generate_diff(file_path1, file_path2, format_name='stylish'):
    # Чтение данных из JSON или YAML файлов
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)

    # Построение дерева различий
    diff = build_diff(data1, data2)

    return choice_format(diff, format_name)
