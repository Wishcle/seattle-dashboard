
import sched
import sqlite3
import time
from dataclasses import dataclass
from http import HTTPStatus
from pathlib import Path
from typing import List, Optional

import pandas
import requests
from tqdm import tqdm

DATABASE_ROOT = Path("db")
DATABASE_FILE = DATABASE_ROOT / Path("seattle.db")
DATABASE_CACHE = DATABASE_ROOT / Path("cache")

BASE_URL = "https://data-seattlecitygis.opendata.arcgis.com/api/download/v1/items/{item}/{filetype}?layers=0"
URL_CSV_COLLISIONS = BASE_URL.format(item="504838adcb124cf4a434e33bf420c4ad", filetype="csv")
URL_CSV_PERSONS    = BASE_URL.format(item="f3e9dd827e934649972cd7469474598a", filetype="csv")
URL_CSV_VEHICLES   = BASE_URL.format(item="90a68d4709b54327a6bc1dfa1b900f8d", filetype="csv")

@dataclass
class Table():
    name: str
    url: str  # To fetch the data from.
    url_fetch_delay: int = 0
    url_response: Optional[requests.Response] = None
    file_path: Optional[Path] = None


def main():
    tables = [
        Table("collisions", URL_CSV_COLLISIONS),
        Table("persons", URL_CSV_PERSONS)]
    LoadDatabaseCmd(tables).exec()


class LoadDatabaseCmd():
    tables: List[Table]
    scheduler: Optional[sched.scheduler] = None

    def __init__(self, tables: List[Table]) -> None:
        self.tables = tables

    def exec(self) -> None:
        self._init_folders()
        self._download_data_from_sdot()
        self._load_data_into_database()
        self._print_tables()

    def _init_folders(self) -> None:
        DATABASE_ROOT.mkdir(exist_ok=True)
        DATABASE_CACHE.mkdir(exist_ok=True)
        DATABASE_FILE.unlink(missing_ok=True)

    def _download_data_from_sdot(self) -> None:
        print("Downloading data...")
        self.scheduler = sched.scheduler()
        for table in self.tables:
            self.scheduler.enter(0, 0, self._poll_for_ok_response, [table])
        self.scheduler.run()
        print("...finished.\n")

    def _poll_for_ok_response(self, table: Table) -> None:
        print(f"[{table.name}] making request ... ", flush=True)
        response = requests.get(table.url)
        status = HTTPStatus(response.status_code)

        # If ACCEPTED, reschedule the poll with linear back-off.
        # We can't download anything until the site says OK.
        if status == HTTPStatus.ACCEPTED:
            table.url_fetch_delay += 3
            server_status = response.json()["status"]
            print(f"[{table.name}] ... request ACCEPTED; server says: {server_status}; sleep {table.url_fetch_delay}", flush=True)
            self.scheduler.enter(table.url_fetch_delay, 0, self._poll_for_ok_response, [table])
            return

        if status == HTTPStatus.OK:
            table.url_response = response
            self._download_from_response(table)
            return

        raise RuntimeError(f"Unexpected status: {status.value} {status.phrase}")

    def _download_from_response(self, table: Table) -> None:
        assert table.url_response is not None
        assert DATABASE_CACHE.exists()

        table.file_path = DATABASE_CACHE / f"{table.name}.csv"
        total_size = int(table.url_response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, leave=False)

        print(f"[{table.name}] ... request OK; downloading file to {table.file_path=}", flush=True)
        with tqdm(total=total_size, unit='B', unit_scale=True) as progress_bar:
            with open(table.file_path, 'wb') as file:
                for data in table.url_response.iter_content(chunk_size=1024):
                    progress_bar.update(len(data))
                    file.write(data)

    def _load_data_into_database(self) -> None:
        with sqlite3.connect(DATABASE_FILE) as conn:
            for table in self.tables:
                with open(table.file_path) as csv_file:
                    df = pandas.read_csv(csv_file)
                    df.to_sql(table.name, conn, if_exists='append', index=False)
                    print(f"table '{table.name}' created.")

    def _print_tables(self) -> None:
        print(f"Here are the tables in {DATABASE_FILE}:")
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            print(cursor.fetchall())


if __name__ == "__main__":
    main()
