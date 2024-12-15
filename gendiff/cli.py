import argparse


def parse_arguments():
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
    return parser.parse_args()
