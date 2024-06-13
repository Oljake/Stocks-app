import customtkinter as ctk
from typing import Dict

class CryptoApp:
    def __init__(self, root):
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

        # Add and Remove Buttons
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

        # Create settings button
        self.settings_button = ctk.CTkButton(master=root, text="Settings", command=self.open_settings_window)
        self.settings_button.grid(row=2, column=0, pady=10, padx=10)

        self.settings_window = None  # Placeholder for settings window reference
        self.settings_changed = False  # Track if settings have been changed

        self.update_holdings_display()

    def open_settings_window(self):
        if self.settings_window:
            self.settings_window.deiconify()  # Bring window to front if already exists
            return

        self.settings_window = ctk.CTk()
        self.settings_window.title("Settings")

        # Display Options
        ctk.CTkLabel(master=self.settings_window, text="Display Options").pack(pady=5)

        self.show_volume_var = ctk.BooleanVar()
        volume_cb = ctk.CTkCheckBox(master=self.settings_window, text="24-hour trading volume",
                                    variable=self.show_volume_var)
        volume_cb.pack(anchor='w')

        self.show_price_var = ctk.BooleanVar()
        price_cb = ctk.CTkCheckBox(master=self.settings_window, text="Price", variable=self.show_price_var)
        price_cb.pack(anchor='w')

        self.show_d1_var = ctk.BooleanVar()
        d1_cb = ctk.CTkCheckBox(master=self.settings_window, text="24h", variable=self.show_d1_var)
        d1_cb.pack(anchor='w')

        self.show_d7_var = ctk.BooleanVar()
        d7_cb = ctk.CTkCheckBox(master=self.settings_window, text="7d", variable=self.show_d7_var)
        d7_cb.pack(anchor='w')

        self.show_d30_var = ctk.BooleanVar()
        d30_cb = ctk.CTkCheckBox(master=self.settings_window, text="30d", variable=self.show_d30_var)
        d30_cb.pack(anchor='w')

        # OK and Apply Buttons
        self.ok_button = ctk.CTkButton(master=self.settings_window, text="OK", command=self.close_settings_window)
        self.ok_button.pack(side=ctk.LEFT, padx=10, pady=10)
        self.ok_button.configure(state='disabled')

        apply_button = ctk.CTkButton(master=self.settings_window, text="Apply", command=self.apply_settings)
        apply_button.pack(side=ctk.RIGHT, padx=10, pady=10)

    def close_settings_window(self):
        if self.settings_window:
            self.settings_window.withdraw()  # Hide the settings window

    def apply_settings(self):
        # Update holdings display according to settings
        self.update_holdings_display()

        # Check if any setting is changed
        if (self.show_volume_var.get() or self.show_price_var.get() or
            self.show_d1_var.get() or self.show_d7_var.get() or self.show_d30_var.get()):
            self.ok_button.configure(state='normal')
        else:
            self.ok_button.configure(state='disabled')




    def add_crypto(self):
        name = self.name_entry.get().strip()
        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            self.log_transaction("Invalid amount for adding.")
            return

        if name and amount > 0:
            if name in self.holdings:
                self.holdings[name]['amount'] += amount
            else:
                self.holdings[name] = {'amount': amount, 'volume': 'N/A', 'price': 'N/A', 'd1': 'N/A', 'd7': 'N/A', 'd30': 'N/A'}
            self.log_transaction(f"Added {amount} of {name}.")
            self.update_holdings_display()
        else:
            self.log_transaction("Invalid name or amount for adding.")

    def remove_crypto(self):
        name = self.name_entry.get().strip()
        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            self.log_transaction("Invalid amount for removing.")
            return

        if name in self.holdings and amount > 0:
            if self.holdings[name]['amount'] >= amount:
                self.holdings[name]['amount'] -= amount
                self.log_transaction(f"Removed {amount} of {name}.")
                if self.holdings[name]['amount'] == 0:
                    del self.holdings[name]
                self.update_holdings_display()
            else:
                self.log_transaction(f"Not enough {name} to remove {amount}.")
        else:
            self.log_transaction("Invalid name or amount for removing.")

    def log_transaction(self, message: str):
        self.log.append(message)
        self.log_text.configure(state='normal')  # Enable editing
        self.log_text.insert(ctk.END, message + "\n")
        self.log_text.configure(state='disabled')  # Disable editing

    def update_holdings_display(self):
        self.holdings_text.configure(state='normal')  # Enable editing
        self.holdings_text.delete("1.0", ctk.END)
        for name, data in self.holdings.items():
            display_text = f"{name} {data['amount']}:\n"
            if self.show_volume_var.get():
                if data['volume'] == 'N/A':
                    display_text += f"  24-hour trading volume: N/A\n"
                else:
                    display_text += f"  24-hour trading volume: ${data['volume']} USD\n"
            if self.show_price_var.get():
                if data['price'] == 'N/A':
                    display_text += f"  Price: N/A\n"
                else:
                    display_text += f"  Price: ${data['price']} USD\n"
            if self.show_d1_var.get():
                if data['d1'] == 'N/A':
                    display_text += f"  24h: N/A\n"
                else:
                    display_text += f"  24h: {round(float(data['d1']), 2)}%\n"
            if self.show_d7_var.get():
                if data['d7'] == 'N/A':
                    display_text += f"  7d: N/A\n"
                else:
                    display_text += f"  7d: {round(float(data['d7']), 2)}%\n"
            if self.show_d30_var.get():
                if data['d30'] == 'N/A':
                    display_text += f"  30d: N/A\n"
                else:
                    display_text += f"  30d: {round(float(data['d30']), 2)}%\n"

            self.holdings_text.insert(ctk.END, display_text + "\n")
        self.holdings_text.configure(state='disabled')  # Disable editing


if __name__ == "__main__":
    root = ctk.CTk()
    app = CryptoApp(root)
    root.mainloop()
