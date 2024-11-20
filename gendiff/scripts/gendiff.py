import argparse
import json
import yaml

from gendiff.parser import read_file


def format_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    return value


def generate_diff(file_path1, file_path2):
    # Чтение данных из JSON или YAML файлов
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)

    all_keys = sorted(set(data1.keys()).union(data2.keys()))

    result = ["{"]

    for key in all_keys:

        if key in data1 and key in data2:
            if data1[key] == data2[key]:
                result.append(f"    {key}: {format_value(data1[key])}")
            else:
                result.append(f"  - {key}: {format_value(data1[key])}")
                result.append(f"  + {key}: {data2[key]}")

        elif key in data1:
            result.append(f"  - {key}: {format_value(data1[key])}")

        elif key in data2:
            result.append(f"  + {key}: {format_value(data2[key])}")

    result.append("}")

    return "\n".join(result)


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
        choices=["plain", "json"],  # доступные форматы
        default="json",  # формат по умолчанию
        help="set format of output"
    )

    # Парсим аргументы
    args = parser.parse_args()

    diff = generate_diff(args.first_file, args.second_file)
    print(diff)


if __name__ == "__main__":
    main()
