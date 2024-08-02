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


def get_all_animals_characteristics(animals):
    """Returns a list of all animals' characteristics
    :param animals: list of animals
    :return: list of strings
    """
    char_list = []
    for animal in animals:
        char_list += animal['characteristics'].keys()
    return sorted(set(char_list))


def get_animal_characteristic(animal, characteristic):
    """Returns tuple of animal characteristic name and value or empty string
    :param animal: dictionary
    :param characteristic: string
    :return: tuple or string (if there's no characteristic in animal's dictionary)
    """
    animal_key = characteristic.capitalize().replace("_", " ")
    try:
        animal_value = animal['characteristics'][characteristic]
        return animal_key, animal_value
    except KeyError:
        return ""


def serialize_animal(animal, characteristics):
    """Converts dictionary into html-formatted string
    :param animal: dictionary
    :param characteristics: list of characteristics
    :return: string
    """
    animal_chars = []
    for characteristic in characteristics:
        if characteristic:
            animal_chars.append(get_animal_characteristic(animal, characteristic))
    animal_name = wrap_into_html_tag(animal['name'], "div", "card__title") + "\n"
    location_text = f'{wrap_into_html_tag("Location", "strong")}: {animal["locations"][0]}' + "\n"
    animal_info = wrap_into_html_tag(location_text, "li", "animal_characteristic") + "\n"
    for animal_char in animal_chars:
        if animal_char:
            list_item = f'{wrap_into_html_tag(animal_char[0], "strong")}: {animal_char[1]}'
            list_item = wrap_into_html_tag(list_item, "li", "animal_characteristic") + "\n"
            animal_info += list_item
    animal_info = wrap_into_html_tag(animal_info, "ul", "card__info") + "\n"
    characteristics_output = wrap_into_html_tag(animal_info,
                                                "p",
                                                "card__text") + "\n"
    serialized_animal = wrap_into_html_tag(animal_name + characteristics_output,
                                           "li",
                                           "cards__item") + "\n"
    return serialized_animal


def get_all_animals_info(animals_data, characteristics):
    """Combines cards of all animals in one html-formatted string
    :param animals_data: list of animals
    :param characteristics: list of characteristics
    :return: string
    """
    all_animals_info = ""
    for animal in animals_data:
        all_animals_info += serialize_animal(animal, characteristics)
    return all_animals_info


def main():
    """Loads data from external JSON file, reads html template file,
    generates html-formatted string with animals info,
    replaces placeholder from template with actual info, writes new html file
    :return: None
    """
    data = load_data("animals_data.json")
    animal_characteristics = get_all_animals_characteristics(data)
    html_template = read_html_template('animals_template.html')
    animals_info_string = get_all_animals_info(data, animal_characteristics)
    new_html = html_template.replace("__REPLACE_ANIMALS_INFO__", animals_info_string)
    write_html_file('animals.html', new_html)


if __name__ == "__main__":
    main()
