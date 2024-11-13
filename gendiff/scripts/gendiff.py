import argparse
import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


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

    # Чтение файлов
    file1_data = read_json(args.first_file)
    file2_data = read_json(args.second_file)
    # Вывод данных для проверки
    print("File 1 data:", file1_data)
    print("File 2 data:", file2_data)


if __name__ == "__main__":
    main()
