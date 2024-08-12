import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
API_KEY = os.getenv('API_KEY')


def load_data_api(search_key):
    """Gets data about animals from api based on user input
    :return: list
    """
    url = "https://api.api-ninjas.com/v1/animals"
    params = "?name=" + search_key
    header_api = {"x-api-key": API_KEY}
    result = requests.get(url + params, headers=header_api).json()
    return result


def load_data_from_file(file_path):
    """Loads data from a JSON file
    :param file_path: path to a JSON file
    :return: list
    """
    with open(file_path, "r") as file_obj:
        return json.loads(file_obj.read())


def main():
    pass


if __name__ == "__main__":
    main()
