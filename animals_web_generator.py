import data_fetcher


def ask_animal_name():
    """Gets animal name from user input
    :return: string
    """
    while True:
        search_key = input('Enter animal name: ')
        if isinstance(search_key, str) and len(search_key) > 1:
            return search_key
        else:
            print('Expected a string with at least 2 characters')


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
    print('Html file was generated successfully')


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


def ask_user_for_skin_type(animals):
    """Generates a list of available skin types, prints the list,
    gets desirable skin type from user
    :param animals: list of animals
    :return: string
    """
    skin_types = []
    for animal in animals:
        try:
            skin_types.append(animal['characteristics']['skin_type'])
        except KeyError:
            skin_types.append('Not specified')
    skin_types = sorted(set(skin_types))
    while True:
        print("List of possible skin types:")
        print("\t" + "\n\t".join(skin_types))
        user_input = input('Enter a skin type, that you want to filter animals by '
                           '(leave blank to generate html without filter): ')
        user_input = user_input.strip().lower().capitalize()
        if user_input in skin_types or not user_input:
            return user_input
        print(f'There is no skin type "{user_input}".\n')


def filter_animals_by_characteristic(animals, characteristic_type, value):
    """Filters animals and returns a new list with animals,
    whose characteristic_type is equal to value.
    If value is empty returns original animals
    :param animals: list
    :param characteristic_type: characteristic key as a string
    :param value: characteristic value as a string
    :return: list
    """
    new_animals_list = []
    if not value:
        return animals
    if value == "Not specified":
        [new_animals_list.append(animal) for animal in animals
         if characteristic_type not in animal['characteristics']]
    else:
        for animal in animals:
            try:
                if animal['characteristics'][characteristic_type] == value:
                    new_animals_list.append(animal)
            except KeyError:
                pass
    return new_animals_list


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


def main():
    """Loads data from API, reads html template file,
    applies user filter (if any) to animals,
    generates html-formatted string with animals info,
    replaces placeholder from template with actual info, writes new html file
    :return: None
    """
    # data = data_fetcher.load_data_from_file("animals_data.json")
    animal_search = ask_animal_name()
    data = data_fetcher.load_data_api(animal_search)
    if not data:
        animals_info_string = f"<h2>The animal \"{animal_search}\" doesn't exist.</h2>"
    else:
        animal_characteristics = get_all_animals_characteristics(data)
        user_skin_type = ask_user_for_skin_type(data)
        data = filter_animals_by_characteristic(data,
                                                'skin_type',
                                                user_skin_type)
        animals_info_string = get_all_animals_info(data, animal_characteristics)
    html_template = read_html_template('animals_template.html')
    new_html = html_template.replace("__REPLACE_ANIMALS_INFO__", animals_info_string)
    write_html_file('animals.html', new_html)


if __name__ == "__main__":
    main()
