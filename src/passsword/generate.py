import secrets
import string


def generate_password(size: int = 16, uppercase: bool = True, lowercase: bool = True, number: bool = True, symbol: bool = True) -> str:

    if size <= 0:
        raise ValueError("The size of password cannot be zero or negative")

    character_list = []

    if uppercase:
        character_list.append(string.ascii_uppercase)
    if lowercase:
        character_list.append(string.ascii_lowercase)
    if number:
        character_list.append(string.digits)
    if symbol:
        character_list.append(string.punctuation)

    if len(character_list) == 0:
        raise ValueError("You have to choose at least one filter")
    if size < len(character_list):
        raise ValueError("The size must be equal the number of filters you choose")

    required_character = []

    for character in character_list:
        required_character.append(secrets.choice(character))

    all_caracter = "".join(character_list)
    res_size = size - len(required_character)
    remaining_password = [secrets.choice(all_caracter) for _ in range(res_size)]

    password = required_character + remaining_password

    secrets.SystemRandom().shuffle(password)

    return ''.join(password)
