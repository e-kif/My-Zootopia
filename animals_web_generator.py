import json


def load_data(file_path):
    """Loads data from a JSON file
    :param file_path: path to a JSON file
    :return: list
    """
    with open(file_path, "r") as file_obj:
        return json.loads(file_obj.read())


def read_html_template(file_path):
    """Loads content of html template
    :param file_path: path to a html file
    :return: string
    """
    with open(file_path, "r") as file:
        return file.read()


def write_html_file(file_path, html_content):
    """Writes given html_content to a file
    :param file_path: html file to be written
    :param html_content: string
    :return: None
    """
    with open(file_path, "w") as file:
        file.write(html_content)


def get_one_animal_info(animal):
    output_string = ""
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
        output_string += f'{info.capitalize()}: {animal_info[info]}<br>'
    return output_string


def get_all_animals_info(animals_data):
    all_animals_info = ""
    opening_tag = '<li class="cards__item">'
    closing_tag = '</li>'
    for animal in animals_data:
        all_animals_info += opening_tag + get_one_animal_info(animal) + closing_tag
    return all_animals_info


def main():
    data = load_data("animals_data.json")
    html_template = read_html_template('animals_template.html')
    animals_info_string = get_all_animals_info(data)
    new_html = html_template.replace("__REPLACE_ANIMALS_INFO__", animals_info_string)
    write_html_file('animals.html', new_html)


if __name__ == "__main__":
    main()
