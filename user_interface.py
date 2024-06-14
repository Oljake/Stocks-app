from decimal import Decimal, ROUND_HALF_UP
from customtkinter import CTkButton
from typing import Dict

import customtkinter as ctk
import requests
import json

from get_data import get_crypto_data
from new_coin import add_to_json

class CryptoApp:

    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Crypto Portfolio Manager")

        self.holdings: Dict[str, Dict[str, float]] = {}
        self.log = []

        # Crypto-Currency Entry Widgets
        self.entry_frame = ctk.CTkFrame(master=root)
        self.entry_frame.grid(row=0, column=0, pady=10, padx=10, sticky='n')

        self.entry_label = ctk.CTkLabel(master=self.entry_frame, text="Crypto-Currency")
        self.entry_label.pack(pady=5)

        self.name_entry = ctk.CTkEntry(master=self.entry_frame)
        self.name_entry.pack(pady=5)

        self.amount_entry = ctk.CTkEntry(master=self.entry_frame)
        self.amount_entry.pack(pady=5)

        # Add / Remove Buttons
        self.button_frame = ctk.CTkFrame(master=self.entry_frame)
        self.button_frame.pack(pady=10)

        self.add_button = ctk.CTkButton(master=self.button_frame, text="Add", command=self.add_crypto)
        self.add_button.pack(side=ctk.LEFT, padx=10)

        self.remove_button = ctk.CTkButton(master=self.button_frame, text="Remove", command=self.remove_crypto)
        self.remove_button.pack(side=ctk.LEFT, padx=10)

        # Log Widgets
        self.log_frame = ctk.CTkFrame(master=root)
        self.log_frame.grid(row=1, column=0, pady=10, padx=10, sticky='n')

        self.log_label = ctk.CTkLabel(master=self.log_frame, text="Transaction Log")
        self.log_label.pack(pady=5)

        self.log_text = ctk.CTkTextbox(master=self.log_frame, height=200, width=400)
        self.log_text.pack(pady=5)
        self.log_text.configure(state='disabled')

        # Holdings Display
        self.holdings_frame = ctk.CTkFrame(master=root)
        self.holdings_frame.grid(row=0, column=1, rowspan=2, pady=10, padx=10, sticky='n')

        self.holdings_label = ctk.CTkLabel(master=self.holdings_frame, text="Current Holdings")
        self.holdings_label.pack(pady=5)

        self.holdings_text = ctk.CTkTextbox(master=self.holdings_frame, height=400, width=400)
        self.holdings_text.pack(pady=5)
        self.holdings_text.configure(state='disabled')

        # Current holdings
        with open('current_holdings.json', 'r') as file:
            self.holdings = json.load(file)

        # Settings
        self.settings_button = ctk.CTkButton(master=root, text="Settings", command=self.open_settings_window)
        self.settings_button.grid(row=2, column=0, pady=10, padx=10)

        self.settings_window = None

        with open('settings.json', 'r') as file:
            self.settings = json.load(file)

        self.open_settings_window()
        self.load_settings()

        self.unsaved_settings = set()

        # Loadib User'i crypto-currency
        self.load_current_holdings()


        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def close_app(self) -> None:
        """Sulgeb äpi ilma erroriteta."""

        # Sulgeb settingud
        if self.settings_window:
            self.settings_window.destroy()

        # Kui settingud on suletud siis sulgeb main api
        if self.root:
            self.root.destroy()

    def load_current_holdings(self) -> None:
        """Laeb User'i hetkesed crypto-currency andmed Log'i."""

        for currency, data in self.holdings.items():
            amount: float = data['amount']
            if amount == 0:
                continue

            url: str = f"https://coinmarketcap.com/currencies/{currency}/"

            try:
                response = requests.get(url)
                if response.status_code == 200:

                    # Extract'ib data
                    price, volume, percentChange24h, percentChange7d, percentChange30d = get_crypto_data(response)

                    if currency and amount > 0:

                        # Võtab õige koguse ja muudab teised andmeid vastavalt Web'ile
                        if currency in self.holdings:
                            self.holdings[currency]['amount'] = amount
                            self.holdings[currency]['price'] = price
                            self.holdings[currency]['volume'] = volume
                            self.holdings[currency]['d1'] = percentChange24h
                            self.holdings[currency]['d7'] = percentChange7d
                            self.holdings[currency]['d30'] = percentChange30d
                        else:
                            self.holdings[currency] = {'amount': amount,
                                                       'volume': volume,
                                                       'price': price,
                                                       'd1': percentChange24h,
                                                       'd7': percentChange7d,
                                                       'd30': percentChange30d}

                        # Log transaction ja andmete värskendamine
                        self.log_transaction(f"Added {amount} of {currency}.")
                        self.update_holdings_display()

                        # Laeb uuendatud andmed JSON file'i
                        self.save_to_json("current_holdings.json", self.holdings)

                    else:
                        self.log_transaction(f"Failed to fetch data from {url}. Status code: {response.status_code}")
                else:
                    self.log_transaction(f"Crypto-currency not found or incorrect name. "
                                         f"Make sure it's listed \non the web: "
                                         f"https://coinmarketcap.com/currencies/")
            except requests.exceptions.RequestException as e:
                self.log_transaction(f"Error fetching data from {url}: {str(e)}")

    def load_settings(self) -> None:
        """Laeb hetkesed api setting'ud"""

        for name, state in self.settings.items():

            if name == "volume_cb":
                button = self.volume_cb

            elif name == "price_cb":
                button = self.price_cb

            elif name == "d1_cb":
                button = self.d1_cb

            elif name == "d7_cb":
                button = self.d7_cb

            elif name == "d30_cb":
                button = self.d30_cb

            if name and state == "off":
                button.deselect()
            else:
                button.select()

    def open_settings_window(self) -> None:
        """Avab settings menu ja laeb vajalikud Widgets'id"""

        if self.settings_window:
            self.settings_window.deiconify()  # Toob window'i esile, kui see eksisteerib
            return

        self.settings_window = ctk.CTk()
        self.settings_window.title("Settings")
        self.settings_window.overrideredirect(True)  # Peidab window'i TitleBar'i ja Border'id

        self.settings_window.geometry("489x168")  # Default - 479x158

        # OK ja Apply Button'id
        self.ok_button = ctk.CTkButton(master=self.settings_window, text="OK", command=self.close_settings_window)
        self.ok_button.pack(side=ctk.LEFT, padx=10, pady=10)
        self.ok_button.configure(state='disabled')

        self.apply_button = ctk.CTkButton(master=self.settings_window, text="Apply", command=self.apply_settings)
        self.apply_button.pack(side=ctk.RIGHT, padx=10, pady=10)

        # Display Options
        ctk.CTkLabel(master=self.settings_window, text="Display Options").pack(pady=5)

        self.volume_cb = ctk.CTkCheckBox(master=self.settings_window, text="24-hour trading volume",
                                         command=lambda: self.disable_ok(self.volume_cb))
        self.volume_cb.pack(anchor='w')

        self.price_cb = ctk.CTkCheckBox(master=self.settings_window, text="Price",
                                        command=lambda: self.disable_ok(self.price_cb))
        self.price_cb.pack(anchor='w')

        self.d1_cb = ctk.CTkCheckBox(master=self.settings_window, text="24h",
                                     command=lambda: self.disable_ok(self.d1_cb))
        self.d1_cb.pack(anchor='w')

        self.d7_cb = ctk.CTkCheckBox(master=self.settings_window, text="7d",
                                     command=lambda: self.disable_ok(self.d7_cb))
        self.d7_cb.pack(anchor='w')

        self.d30_cb = ctk.CTkCheckBox(master=self.settings_window, text="30d",
                                      command=lambda: self.disable_ok(self.d30_cb))
        self.d30_cb.pack(anchor='w')

    def disable_ok(self, checkbox) -> None:
        """Ei lase Ok Button'it vajutada"""

        self.ok_button.configure(state='disabled')
        self.unsaved_settings.add(checkbox)

    def close_settings_window(self) -> None:
        """Peidab settings menu"""

        if self.settings_window:
            self.settings_window.withdraw()

    def apply_settings(self) -> None:
        """
        Salvestab muudetud settings'ud ja salvestab need JSON file'i.
        Muudab Ok Button'i click'itavaks
        """

        for checkbox in self.unsaved_settings:
            settings_name = str
            settings_status = str

            status = checkbox.get()
            name = checkbox.cget('text')

            if name == "24-hour trading volume":
                settings_name = "volume_cb"

            elif name == "Price":
                settings_name = "price_cb"

            elif name == "24h":
                settings_name = "d1_cb"

            elif name == "7d":
                settings_name = "d7_cb"

            elif name == "30d":
                settings_name = "d30_cb"

            if status == 0:
                settings_status = "off"
            else:
                settings_status = "on"

            self.settings[settings_name] = settings_status

        self.save_to_json("settings.json", self.settings)
        self.unsaved_settings.clear()
        self.ok_button.configure(state='normal')

        # Muudab Log'i andmeid setting'ute järgi
        self.update_holdings_display()

    def save_to_json(self, json_file: str, data: str) -> None:
        """
        Kustutab faili sisu ära ning lisab antud info.

        Parameters:
        - json_file (str): Fail mida soovid muuta.
        - data (str): Info mida soovid faili sisestada
        Returns:
        - None
        """

        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)

    def add_crypto(self) -> None:
        """
        Lisab uued crypto-currency andmed, kui sisestatud andmed
        sobivad ja ka antud crypto-currency on web'is olemas.
        """


        currency = (self.name_entry.get()).lower().strip()
        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            self.log_transaction("Invalid amount for adding.")
            return

        url: str = f"https://coinmarketcap.com/currencies/{currency}/"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                price, volume, percentChange24h, percentChange7d, percentChange30d = get_crypto_data(response)
                if currency and amount > 0:

                    # Lisab uue koguse ja muudab teised andmeid vastavalt Web'ile
                    if currency in self.holdings:
                        self.holdings[currency]['amount'] += amount
                        self.holdings[currency]['price'] = price
                        self.holdings[currency]['volume'] = volume
                        self.holdings[currency]['d1'] = percentChange24h
                        self.holdings[currency]['d7'] = percentChange7d
                        self.holdings[currency]['d30'] = percentChange30d
                    else:
                        self.holdings[currency] = {'amount': amount,
                                                   'volume': volume,
                                                   'price': price,
                                                   'd1': percentChange24h,
                                                   'd7': percentChange7d,
                                                   'd30': percentChange30d}

                        # Log transaction ja andmete värskendamine
                        self.log_transaction(f"Added {amount} of {currency}.")
                        self.update_holdings_display()

                        # Laeb uuendatud andmed JSON file'i
                        self.save_to_json("current_holdings.json", self.holdings)

                        add_to_json([currency], "crypto_names.json")

                else:
                    self.log_transaction("Invalid name or amount for adding.")

            # if response.status_code == 404:  # Kui tuleb 404 siis on link vale

            else:
                self.log_transaction(f"crypto-currency not found or incorrect name. "
                                     f"Make sure it's listed \non the web: "
                                     f"https://coinmarketcap.com/currencies/")
                
        except requests.exceptions.RequestException as e:
            self.log_transaction(f"Error fetching data from {url}: {str(e)}")

    def remove_crypto(self) -> None:
        """
        Eemaldab sisestatud crypto-currency'lt sisestatud
        koguse, kui see on User'i crypto-currency's
        """

        currency = (self.name_entry.get()).lower().strip()
        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            self.log_transaction("Invalid amount for removing.")
            return

        if currency in self.holdings and amount > 0:
            if self.holdings[currency]['amount'] >= amount:
                self.holdings[currency]['amount'] -= amount
                self.log_transaction(f"Removed {amount} of {currency}.")

                self.update_holdings_display()
                self.save_to_json("current_holdings.json", self.holdings)

            else:
                self.log_transaction(f"Not enough {currency} to remove {amount}.")
        else:
            self.log_transaction("Invalid name or amount for removing.")

    def log_transaction(self, message: str) -> None:
        """
        Muudab Log'i korraks muudetavaks, ning
        sel hetel lisab sinna antud sõnumi
        """

        self.log.append(message)
        self.log_text.configure(state='normal')
        self.log_text.insert(ctk.END, message + "\n")
        self.log_text.configure(state='disabled')

    def update_holdings_display(self) -> None:
        """
        Muudab Holdings Display'd vastavalt User'i
        crypto-currency koguse ja andmetele
        """

        self.holdings_text.configure(state='normal')
        self.holdings_text.delete("1.0", ctk.END)
        for name, data in self.holdings.items():

            if data["amount"] == 0:
                continue

            display_text = ""
            if data['price'] != "N/A":
                amount = Decimal(str(data['amount']).replace(',', ''))
                price = Decimal(str(data['price']).replace(',', ''))
                worth = amount * price

                # Ümardab kui väärtus on 1 või rohkem
                if worth >= 1:
                    formatted_worth = f"${worth:.2f} USD"
                else:
                    formatted_worth = f"${worth} USD"

                display_text = f"{name.capitalize()}:\n" \
                               f"  Amount: {amount}\n" \
                               f"  Worth: {formatted_worth}\n\n"

            else:
                display_text = \
                    f"{name}:\n" \
                    f"Current holdings:\n    N/A\n     {data['amount']}\n"

            if self.settings["volume_cb"] == "on":
                if data['volume'] == 'N/A':
                    display_text += f"  24-hour trading volume: N/A\n"
                else:
                    display_text += f"  24-hour trading volume: ${data['volume']} USD\n"

            if self.settings["price_cb"] == "on":
                if data['price'] == 'N/A':
                    display_text += f"  Price: N/A\n"
                else:
                    display_text += f"  Price: ${data['price']} USD\n"

            if self.settings["d1_cb"] == "on":
                if data['d1'] == 'N/A':
                    display_text += f"  24h: N/A\n"
                else:
                    display_text += f"  24h: {round(float(data['d1']), 2)}%\n"

            if self.settings["d7_cb"] == "on":
                if data['d7'] == 'N/A':
                    display_text += f"  7d: N/A\n"
                else:
                    display_text += f"  7d: {round(float(data['d7']), 2)}%\n"

            if self.settings["d30_cb"] == "on":
                if data['d30'] == 'N/A':
                    display_text += f"  30d: N/A\n"
                else:
                    display_text += f"  30d: {round(float(data['d30']), 2)}%\n"

            self.holdings_text.insert(ctk.END, display_text + "\n")
        self.holdings_text.configure(state='disabled')


if __name__ == "__main__":
    root = ctk.CTk()
    app = CryptoApp(root)
    root.mainloop()
