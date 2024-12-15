import os
import pytest

from gendiff import generate_diff

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def read_fixture(file_name):
    """
    Читает содержимое файла фикстуры.
    """
    with open(os.path.join(FIXTURES_DIR, file_name), "r") as file:
        return file.read().strip()


@pytest.mark.parametrize(
    "file1, file2, format_name, expected_fixture",
    [
        (
            "file1.json", "file1.json", "stylish",
            "expected_file1_vs_file1.txt"
        ),
        ("file1.json", "file2.json", "stylish", "expected_diff.txt"),
        (
            "file3.json", "file4.json",
            "stylish", "expected_file3_vs_file4.txt"
        ),
        ("file3.json", "file3.json", "stylish", "expected_file3_vs_file3.txt"),
        (
            "file1.json", "file4.json", "stylish",
            "expected_file1_vs_file4.txt"
        ),
        ("file1.yml", "file2.yml", "stylish", "expected_diff_yml.txt"),
        (
            "file1_rec.json", "file2_rec.json",
            "stylish", "expected_diff_rec.txt"
        ),
        ("file1_rec.yml", "file2_rec.yml", "stylish", "expected_diff_rec.txt"),
        (
            "file1_rec.json", "file2_rec.json",
            "plain", "expected_diff_plain.txt"
        ),
        ("file1_rec.json", "file2_rec.json", "json", "expected_diff_json.txt"),
    ],
)
def test_generate_diff(file1, file2, format_name, expected_fixture):
    """
    Параметризованный тест для проверки generate_diff.
    """
    file1_path = os.path.join(FIXTURES_DIR, file1)
    file2_path = os.path.join(FIXTURES_DIR, file2)

    expected = read_fixture(expected_fixture)

    diff = generate_diff(file1_path, file2_path, format_name=format_name)
    assert diff == expected


def test_generate_diff_invalid_format():
    """
    Тест для проверки ошибок при неправильных форматах входных файлов.
    """
    invalid_file1 = os.path.join(FIXTURES_DIR, "invalid_file.json")
    invalid_file2 = os.path.join(FIXTURES_DIR, "invalid_file2.yml")

    # Проверяем, что корректно обрабатывается ошибка FileNotFoundError
    with pytest.raises(FileNotFoundError):
        generate_diff(invalid_file1, invalid_file2, format_name="stylish")


def test_generate_diff_invalid_formatters():
    """
    Проверяем передачу неподдерживаемого форматтера.
    """
    file1 = os.path.join(FIXTURES_DIR, "file1.json")
    file2 = os.path.join(FIXTURES_DIR, "file2.json")

    with pytest.raises(ValueError, match="Неизвестный форматер: invalid"):
        generate_diff(file1, file2, format_name="invalid")
