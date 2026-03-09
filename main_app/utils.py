import requests

def resolve_eve_character_id(character_name):
    if not character_name:
        return None
    try:
        url = "https://esi.evetech.net/latest/universe/ids/"
        response = requests.post(url, json=[character_name], timeout=10)
        response.raise_for_status()
        data = response.json()
        characters = data.get('characters', [])
        if not characters:
            return None
        return characters[0]['id']
    except requests.RequestException:
        return None