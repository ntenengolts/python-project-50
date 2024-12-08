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
            "{\n    age: 30\n    name: Alice\n}"
        ),
        ("file1.json", "file2.json", "stylish", "expected_diff.txt"),
        ("file3.json", "file4.json", "stylish", "{\n  + city: New York\n}"),
        ("file3.json", "file3.json", "stylish", "{\n}"),
        (
            "file1.json", "file4.json", "stylish",
            "{\n  - age: 30\n  + city: New York\n  - name: Alice\n}"
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

    if expected_fixture.endswith(".txt"):
        expected = read_fixture(expected_fixture)
    else:
        expected = expected_fixture

    diff = generate_diff(file1_path, file2_path, format_name=format_name)
    assert diff == expected
