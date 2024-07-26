
import requests
import time
from typing import Optional
from tqdm import tqdm
from pathlib import Path
from http import HTTPStatus

BASE_URL = "https://data-seattlecitygis.opendata.arcgis.com/api/download/v1/items/{item}/{filetype}?layers=0"
URL_CSV_COLLISIONS = BASE_URL.format(item="504838adcb124cf4a434e33bf420c4ad", filetype="csv")
URL_CSV_PERSONS    = BASE_URL.format(item="f3e9dd827e934649972cd7469474598a", filetype="csv")
URL_CSV_VEHICLES   = BASE_URL.format(item="90a68d4709b54327a6bc1dfa1b900f8d", filetype="csv")

DATA_DIR = Path("data")

def main():
    LoadDatabaseCmd(URL_CSV_PERSONS, "persons.csv").exec()
    LoadDatabaseCmd(URL_CSV_COLLISIONS, "collisions.csv").exec()


class LoadDatabaseCmd():
    url: str  # The url to fetch the data from.
    file_name: str  # Where to put the downloaded data.

    response: Optional[requests.Response] = None

    def __init__(self, url: str, file_name: str) -> None:
        self.url = url
        self.file_name = file_name

    def exec(self) -> None:
        self._download_data_from_sdot()
        self._load_data_into_database()
        self._print_tables()

    def _download_data_from_sdot(self) -> None:
        self._poll_for_ok_response()
        self._download_from_response()

    def _poll_for_ok_response(self) -> requests.Response:
        assert self.response is None
        sleep_time = 15
        while True:
            print("making request ... ", end="", flush=True)
            response = requests.get(self.url)
            status = HTTPStatus(response.status_code)

            if status == HTTPStatus.ACCEPTED:
                server_status = response.json()["status"]
                print(f"request ACCEPTED; server says: {server_status}; sleep {sleep_time}")
                time.sleep(sleep_time)
                sleep_time += 5
                continue

            if status == HTTPStatus.OK:
                self.response = response
                return

            raise RuntimeError(f"Unexpected status: {status.value} {status.phrase}")

    def _download_from_response(self):
        assert self.response is not None
        assert self.response.status_code == HTTPStatus.OK

        print(f"request OK; downloading file to {self.file_name=}")
        DATA_DIR.mkdir(exist_ok=True)
        file_name = DATA_DIR / self.file_name
        total_size = int(self.response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

        with tqdm(total=total_size, unit='B', unit_scale=True) as progress_bar:
            with open(file_name, 'wb') as file:
                for data in self.response.iter_content(chunk_size=1024):
                    progress_bar.update(len(data))
                    file.write(data)

    def _load_data_into_database(self) -> None:
        pass

    def _print_tables(self) -> None:
        pass


if __name__ == "__main__":
    main()
