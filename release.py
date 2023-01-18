# curl -v --user 'admin:admin123' --upload-file ./test.png http://localhost:8081/repository/documentation/test.png
import os

import requests


class Nexus:

    def __init__(self, directory: str, repo_name: str = "raw-hosted"):
        self._directory = directory
        self._repo_name = repo_name

    def upload(self, file_path: str):
        auth = (
            "d.gorkhover",
            "j9iuS9mhx%bU4w52vy#GpN*3ipXu@8W7",
        )
        repo_path = file_path.removeprefix(self._directory)
        repo_path = repo_path.removeprefix("/")

        url = f"https://nexus.fozzy.lan/repository/{self._repo_name}/{repo_path}"
        print(f"{file_path} --> {url}")

        resp = requests.put(
            url,
            auth=auth,
            files={'file': open(file_path, 'rb')},
            verify=False,
        )

        if resp.status_code >= 400:
            raise Exception(resp.status_code)

        return None


def traverse_upload(nexus: Nexus, directory: str):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                nexus.upload(os.path.join(root, file))


def main():
    directory = os.getcwd()
    nexus = Nexus(directory=directory)
    traverse_upload(nexus=nexus, directory=directory)


if __name__ == "__main__":
    main()
