import json


def load_data(file_path):
    """Loads data from a JSON file
    :param file_path: path to a JSON file
    :return: list
    """
    with open(file_path, "r") as file_obj:
        return json.loads(file_obj.read())


def print_animal_info(animals_data):
    for animal in animals_data:
        animal_info = {
            'name': animal['name'],
            'diet': animal['characteristics']['diet'],
            'location': animal['locations'][0]
        }
        try:
            animal_info['type'] = animal['characteristics']['type']
        except KeyError:
            pass

        for info in animal_info.keys():
            print(f'{info.capitalize()}: {animal_info[info]}')
        print()


def main():
    data = load_data("animals_data.json")
    print_animal_info(data)


if __name__ == "__main__":
    main()