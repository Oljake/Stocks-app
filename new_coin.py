import json
from typing import List  # Type hints


def add_to_json(coin_names: List[str], filename: str) -> None:
    """
    Lisab uued crypto-currency'd JSON-faili, kui neid seal veel pole.

    :param coin_names: List mis sisaldab uute crypto-currency'te nimesi.
    :param filename: JSON file'i nimi mida tuleb uuendada.
    :return: None
    """
    try:
        # Avab JSON-faili ja salvestab olemasolevad data
        with open(filename, "r") as f:
            existing_coins = set(json.load(f))
    except FileNotFoundError:
        existing_coins = set()

    # Uuendab crypto-currency listi - kombineerib olemasolevad uutega nii, et duplikaate ei tule
    existing_coins.update(coin_names)

    # Kirjutab uuendatud listi tagasi faili
    with open(filename, "w") as f:
        json.dump(list(existing_coins), f, indent=4)


def read_from_json(filename: str) -> list:
    """
    Loeb JSON-failist andmed ja return'ib need.

    :param filename: JSON file mida soovid lugeda.
    :return: Crypto-currency'te nimede listi
    """
    with open(filename, "r") as f:
        coin_names = json.load(f)

        return coin_names

# Example usage
if __name__ == "__main__":
    new_coin = ["xrp"]

    add_to_json(new_coin, "crypto_names.json")

    for name in read_from_json("crypto_names.json"):
        print(name)
