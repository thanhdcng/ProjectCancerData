import os
import importlib
import sys
from config.db_config import DATABASE_CONFIG

print(sys.path, "\n")


def get_available_importers():
    importers = {}
    counter = 1
    importers_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "importers")

    for file in os.listdir(importers_dir):
        if file.endswith('_importer.py') and file != 'base_importer.py':
            module_name = file[:-3]
            class_name = ''.join(word.capitalize() for word in module_name.split('_')[:-1]) + 'Importer'

            print(f"Detected module: {module_name}, \n"
                  f"class: {class_name},\n")
            importers[counter] = (module_name, class_name)
            counter += 1
    return importers


def main():

    importers = get_available_importers()

    print("Available importers: ")
    for num, (module, class_name) in importers.items():
        print(f"{num}: {module}")


    try:
        choice = int(input("\nChoose an importer number: "))
        if choice not in importers:
            raise ValueError("Invalid importer number")

        module_name, class_name = importers[choice]
        module = importlib.import_module(f"importers.{module_name}")
        importer_class = getattr(module, class_name)

        file_path = input("Enter CSV file path: ")
        if not os.path.isfile(file_path):
            raise FileNotFoundError("File not found")

        importer = importer_class(DATABASE_CONFIG)
        importer.import_rows(file_path)

    except ValueError as ve:
        print(f"Invalid input: {ve}")

    except FileNotFoundError as fnf:
        print(f"File error: {fnf}")

    except AttributeError as ae:
        print(f"Importer class not found: {ae}")

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
