# Ainult vajalikud funcid
from re import search
from time import sleep
from bs4 import BeautifulSoup
from requests import Response, get

from typing import Tuple, Union  # Type hints
from new_coin import read_from_json  # Loeb json failist crypto listi

def get_crypto_data(currency_url: Response) -> Union[Tuple[str, str, str, str, str], str]:
    """
    Extract'ib' crypto-currency data antud URL'ist.

    :param currency_url: Response object mis sisaldab HTML content'i crypto-currency veebilehel.
    :return: Tuple[price, volume, percentChange24h, percentChange7d, percentChange30d],
             või kui data't ei leitud siis "N/A"
    """
    try:
        soup: BeautifulSoup = BeautifulSoup(currency_url.content, "html.parser")
        description_tag: BeautifulSoup = soup.find("meta", {"name": "description"})
        description: str = description_tag["content"]

        # Extract'ib' järgneva: price, 24-hour trading volume, percentChange24h, percentChange7d, percentChange30d
        price_match = search(r"The live [\w\s]+ price today is \$([\d,]+\.\d+) USD", description)
        volume_match = search(r"24-hour trading volume of \$([\d,]+(?:,[\d]+)*(?:\.\d+)?) USD", description)
        percentChange24h_match = search(r"percentChange24h\":([\d,-]+\.\d+)", currency_url.text)
        percentChange7d_match = search(r"percentChange7d\":([\d,-]+\.\d+)", currency_url.text)
        percentChange30d_match = search(r"percentChange30d\":([\d,-]+\.\d+)", currency_url.text)

        # Kui ei leia crypto-currency data osa siis return'ib "N/A"
        price: str = "N/A"
        volume: str = "N/A"
        percentChange24h: str = "N/A"
        percentChange7d: str = "N/A"
        percentChange30d: str = "N/A"

        # Kui leiab crypto-currency data osa
        if price_match:
            price = price_match.group(1)
        if volume_match:
            volume = volume_match.group(1)
        if percentChange24h_match:
            percentChange24h = percentChange24h_match.group(1)
        if percentChange7d_match:
            percentChange7d = percentChange7d_match.group(1)
        if percentChange30d_match:
            percentChange30d = percentChange30d_match.group(1)

        return price, volume, percentChange24h, percentChange7d, percentChange30d


    except TypeError or UnboundLocalError as e:
        print("Most likely incorrect link.")
        print(f"get_data -> get_crypto_data:\n   {e}.\n\n")

        return "N/A", "N/A", "N/A", "N/A", "N/A"

# Example usage
if __name__ == "__main__":
    count: int = 0

    while True:
        print(f"Tries: {count}")
        for currency in read_from_json("crypto_names.json"):
            url: str = f"https://coinmarketcap.com/currencies/{currency}/"

            price, volume, d1, d7, d30 = get_crypto_data(get(url))

            print(
                f"{currency}:\n"
                f"  24-hour trading volume: {'N/A' if volume == 'N/A' else f'${volume} USD'}\n"
                f"  Price: {'N/A' if price == 'N/A' else f'${price} USD'}\n"
                f"  24h: {'N/A' if d1 == 'N/A' else f'{round(float(d1), 2)}%'}\n"
                f"  7d: {'N/A' if d7 == 'N/A' else f'{round(float(d7), 2)}%'}\n"
                f"  30d: {'N/A' if d30 == 'N/A' else f'{round(float(d30), 2)}%'}\n"
            )

        sleep(200)
        count += 1
