import os
import sys

from gendiff import generate_diff

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
))

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def read_fixture(file_name):
    """
    Читает содержимое файла фикстуры.
    """
    with open(os.path.join(FIXTURES_DIR, file_name), "r") as file:
        return file.read()


def test_identical_files():
    """
    Проверяет, что два идентичных JSON-файла не содержат различий.
    """
    file1 = os.path.join(FIXTURES_DIR, "file1.json")
    diff = generate_diff(file1, file1)
    assert diff == "{\n    age: 30\n    name: Alice\n}"


def test_different_files():
    """
    Проверяет, что различия между файлами корректно отображаются.
    """
    file1 = os.path.join(FIXTURES_DIR, "file1.json")
    file2 = os.path.join(FIXTURES_DIR, "file2.json")
    expected = read_fixture("expected_diff.txt").strip()
    diff = generate_diff(file1, file2)
    assert diff == expected


def test_empty_and_non_empty_files():
    """
    Проверяет работу с пустым файлом и файлом с данными.
    """
    file3 = os.path.join(FIXTURES_DIR, "file3.json")
    file4 = os.path.join(FIXTURES_DIR, "file4.json")
    diff = generate_diff(file3, file4)
    assert diff == "{\n  + city: New York\n}"


def test_empty_files():
    """
    Проверяет корректность сравнения двух пустых файлов.
    """
    file3 = os.path.join(FIXTURES_DIR, "file3.json")
    diff = generate_diff(file3, file3)
    assert diff == "{\n}"


def test_missing_keys():
    """
    Проверяет, что функция корректно обрабатывает файлы
    с отсутствующими ключами.
    """
    file1 = os.path.join(FIXTURES_DIR, "file1.json")
    file4 = os.path.join(FIXTURES_DIR, "file4.json")
    diff = generate_diff(file1, file4)
    expected = "{\n  - age: 30\n  + city: New York\n  - name: Alice\n}"
    assert diff == expected


def test_diff_yaml_files():
    """
    Проверяет, что различия между файлами корректно отображаются.
    """
    file1 = os.path.join(FIXTURES_DIR, "file1.yml")
    file2 = os.path.join(FIXTURES_DIR, "file2.yml")
    expected = read_fixture("expected_diff_yml.txt").strip()
    diff = generate_diff(file1, file2)
    assert diff == expected

