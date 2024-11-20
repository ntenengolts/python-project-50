import json
import yaml


def read_file(file_path):
    """Читает файл в формате JSON или YAML и возвращает данные."""
    with open(file_path, 'r') as file:
        if file_path.endswith('.json'):
            return json.load(file)
        elif file_path.endswith(('.yml', '.yaml')):
            return yaml.safe_load(file)
        else:
            raise ValueError("Unsupported file format")
