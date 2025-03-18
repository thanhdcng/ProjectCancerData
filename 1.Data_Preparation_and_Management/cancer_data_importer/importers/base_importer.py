import csv
import time
from tqdm import tqdm
from abc import ABC, abstractmethod
import psycopg2

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
        """
        Should return a tuple of values in the correct column order
        (or None if the row is invalid).
        """
        pass

    @abstractmethod
    def bulk_insert(self, data):
        """
        Should accept a list of tuples (rows) and perform a bulk insert.
        """
        pass

    def import_data_bulk(self, file_path, batch_size=10000):
        """
        NEW bulk insert method with progress reporting.
        Reads CSV, processes rows, and calls `bulk_insert` in batches.
        Shows a progress bar with percentage completed and elapsed time.
        """
        start_time = time.time()
        total_rows = 0
        successful_imports = 0
        buffer = []

        # First, get the total number of rows for progress estimation.
        # (We skip the header row.)
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            total_rows = sum(1 for _ in csv_file) - 1

        self.connect()
        self.create_table()

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            # Wrap the reader with tqdm for progress bar
            for row in tqdm(csv_reader, total=total_rows, desc="Processing rows", unit="row"):
                processed_tuple = self.process_row(row)
                if processed_tuple:
                    buffer.append(processed_tuple)

                # When we reach the batch size, insert the batch
                if len(buffer) >= batch_size:
                    self.bulk_insert(buffer)
                    successful_imports += len(buffer)
                    buffer.clear()

            # Insert any remaining rows
            if buffer:
                self.bulk_insert(buffer)
                successful_imports += len(buffer)

        elapsed_time = time.time() - start_time

        print(f"\nBulk import completed:")
        print(f"  Total rows read: {total_rows}")
        print(f"  Successfully inserted: {successful_imports} rows")
        print(f"  Failed/skipped: {total_rows - successful_imports} rows")
        print(f"  Elapsed time: {elapsed_time:.2f} seconds")

        self.disconnect()
