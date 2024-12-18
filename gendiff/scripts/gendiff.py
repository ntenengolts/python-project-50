from gendiff.cli import parse_arguments
from gendiff.core import generate_diff


def main():

    # Получаем  аргументы
    args = parse_arguments()

    result = generate_diff(
        args.first_file, args.second_file, format_name=args.format
    )
    print(result)


if __name__ == "__main__":
    main()
