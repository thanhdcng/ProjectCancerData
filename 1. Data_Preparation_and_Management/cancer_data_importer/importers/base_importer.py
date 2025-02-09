import psycopg2
from datetime import datetime
import csv
from abc import ABC, abstractmethod

class BaseImporter(ABC):
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = psycopg2.connect(**self.config)
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    @abstractmethod
    def create_table(self):
        pass

    @abstractmethod
    def process_row(self, row):
        pass

    def import_rows(self, file_path):
        total_rows = 0
        successful_imports = 0

        try:
            self.connect()
            self.create_table()

            with open(file_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    total_rows += 1
                    try:
                        processed_row = self.process_row(row)
                        if processed_row:
                            self.cursor.execute(processed_row[0], processed_row[1])
                            successful_imports += 1

                            if successful_imports % 1000 == 0:
                                print(f"Processed {successful_imports} rows")

                    except Exception as e:
                        print(f"Error on row {total_rows}: {e}")
                        continue

            print(f"\nImport completed: {successful_imports} rows")
            print(f"Total rows: {total_rows}")
            print(f"Successful: {successful_imports}")
            print(f"Failed: {total_rows - successful_imports}")

        finally:
            self.disconnect()
