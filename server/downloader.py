
import requests
import time
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

    def __init__(self, url: str, file_name: str) -> None:
        self.url = url
        self.file_name = file_name

    def exec(self) -> None:
        self._download_data_from_sdot()
        self._load_data_into_database()
        self._print_tables()

    def _download_data_from_sdot(self) -> None:
        download(self.url, self.file_name)

    def _load_data_into_database(self) -> None:
        pass

    def _print_tables(self) -> None:
        pass


def download(url: str, file_name: Path) -> None:
    sleep_time = 15
    while True:
        print("making request ... ", end="", flush=True)
        response = requests.get(url)
        status = HTTPStatus(response.status_code)

        if status == HTTPStatus.ACCEPTED:
            server_status = response.json()["status"]
            print(f"request ACCEPTED; server says: {server_status}; sleep {sleep_time}")
            time.sleep(sleep_time)
            sleep_time += 5
            continue

        if status == HTTPStatus.OK:
            print(f"request OK; downloading file to {file_name=}")
            download_from_response(response, file_name)
            return

        raise RuntimeError(f"Unexpected status: {status.value} {status.phrase}")


def download_from_response(response: requests.Response, file_name: Path):
    DATA_DIR.mkdir(exist_ok=True)
    file_name = DATA_DIR / file_name

    assert response.status_code == HTTPStatus.OK
    total_size = int(response.headers.get('content-length', 0))
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    with tqdm(total=total_size, unit='B', unit_scale=True) as progress_bar:
        with open(file_name, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                progress_bar.update(len(data))
                file.write(data)


if __name__ == "__main__":
    main()
