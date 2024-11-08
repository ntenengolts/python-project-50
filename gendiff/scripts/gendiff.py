import argparse

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

if __name__ == "__main__":
    main()
