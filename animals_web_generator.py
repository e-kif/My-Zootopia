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


def wrap_into_html_tag(input_string, html_tag, tag_class="", tag_id=""):
    """Wraps a string into given html tag, assigns class and id if provided
    :param input_string: string for wrapping
    :param html_tag: html tag
    :param tag_class: class for wrapping tag
    :param tag_id: id for wrapping tag
    :return: string
    """
    if tag_class:
        tag_class = f' class="{tag_class}"'
    if tag_id:
        tag_id = f' id="{tag_id}"'
    opening_tag = f'<{html_tag}{tag_id}{tag_class}>'
    closing_tag = f'</{html_tag}>'
    return opening_tag + input_string + closing_tag


def get_one_animal_info(animal):
    """Converts dictionary into html-formatted string
    :param animal: dictionary
    :return: string
    """
    animal_info = {
        'name': animal['name'],
        'diet': animal['characteristics']['diet'],
        'location': animal['locations'][0]
    }
    try:
        animal_info['type'] = animal['characteristics']['type']
        animal_type = f'{wrap_into_html_tag("Type:", "strong")} {animal_info["type"]}<br/>\n'
    except KeyError:
        animal_type = ""
    animal_name = wrap_into_html_tag(animal_info['name'], "div", "card__title") + "\n"
    animal_location = f'{wrap_into_html_tag("Location:", "strong")} {animal_info["location"]}<br/>\n'
    animal_diet = f'{wrap_into_html_tag("Diet:", "strong")} {animal_info["diet"]}<br/>\n'
    animal_info = wrap_into_html_tag(animal_location + animal_type + animal_diet, "p", "card__text")
    return animal_name + animal_info + "\n"


def get_all_animals_info(animals_data):
    all_animals_info = ""
    for animal in animals_data:
        all_animals_info += wrap_into_html_tag(get_one_animal_info(animal), "li", "cards__item")
    return all_animals_info


def main():
    data = load_data("animals_data.json")
    html_template = read_html_template('animals_template.html')
    animals_info_string = get_all_animals_info(data)
    new_html = html_template.replace("__REPLACE_ANIMALS_INFO__", animals_info_string)
    write_html_file('animals.html', new_html)


if __name__ == "__main__":
    main()
