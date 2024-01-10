"""
This file contains the code for a graphical user interface (GUI) for a clustering application.
The GUI allows users to input data and perform clustering operations.
"""
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox


class UserInputGUI:
    """
    This class creates a graphical user interface for collecting user input data.
    It uses the Tkinter library and the ttk theme engine to
    create a GUI with labels, entries, and buttons.
    The class also includes functions for validating
    user input and submitting the data to the main program.

    Attributes:
        root (tk.Tk): The main window of the GUI.
        entries (dict): A dictionary of the input widgets.
        user_data (dict): A dictionary of the user input data.
        months (list): A list of the months in the year.
    """

    def __init__(self, root):
        """
        Initialize the GUI elements and set up the main window.

        Args:
            root (tk.Tk): The main window of the GUI.
        """
        self.entries = None
        self.user_data = None
        self.root = root
        root.title("User Data Input")
        self.months = ['January', 'February', 'March', 'April',
                       'May', 'June', 'July', 'August', 'September',
                       'October', 'November', 'December']
        self.create_widgets()

    def create_widgets(self):
        """
        Create the input widgets for the user input form.

        Returns:
            None
        """
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(row=0, column=0, sticky="nsew")

        labels = ["Device ID:", "Street Name:", "Street Number:",
                  "Postal Code:", "City:", "Year:"]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(input_frame, text=label).grid(
                row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(input_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            self.entries[label.split(':')[0].lower().replace(" ", "_")] = entry

        ttk.Label(input_frame, text="Month:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        month_combobox = ttk.Combobox(input_frame, values=self.months, state="readonly")
        month_combobox.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
        month_combobox.current(0)
        self.entries['month'] = month_combobox

        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.grid(row=7, column=0, sticky="ew")
        button_frame.columnconfigure(0, weight=1)

        ttk.Button(button_frame, text="Exit",
                   command=self.root.destroy).grid(
            row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Button(button_frame, text="Clear",
                   command=self.clear_fields).grid(
            row=0, column=1, sticky="e", padx=5, pady=5)
        ttk.Button(button_frame, text="Submit",
                   command=self.submit_data).grid(
            row=0, column=2, sticky="w", padx=5, pady=5)

    def clear_fields(self):
        """
        Clear the contents of all input fields.
        """
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def submit_data(self):
        """
        Submit the user input data to the main program.

        Raises:
            ValueError: If any of the fields are empty or
            if the year is not a 4-digit number or is in the future.
        """
        try:
            for key, value in self.entries.items():
                if not value.get().strip():
                    raise ValueError(f"{key.capitalize()} cannot be empty.")

            current_year = datetime.now().year
            month_name_to_number = {month: i + 1 for i, month in enumerate(self.months)}
            self.user_data = {}
            for key, value in self.entries.items():
                input_value = value.get()
                if key == 'year':
                    if not input_value.isdigit() or int(input_value) > current_year:
                        raise ValueError("Year must be a number and cannot be in the future.")
                    self.user_data[key] = int(input_value)
                elif key == 'postal_code':
                    if not input_value.isdigit() or len(input_value) != 4:
                        raise ValueError("Postal code must have exactly 4 digits.")
                    self.user_data[key] = int(input_value)
                elif key == 'city':
                    if input_value.isdigit():
                        raise ValueError("City name cannot be a number.")
                    self.user_data[key] = input_value.lower()
                elif key == 'month':
                    self.user_data[key] = month_name_to_number[input_value]
                else:
                    self.user_data[key] = input_value
            messagebox.showinfo("Data Submitted", "Data successfully submitted!")
            self.root.quit()
        except ValueError as value_error:
            messagebox.showerror("Invalid Input", str(value_error))


def get_user_input():
    """
    Opens a GUI window for user input of street address information.

    Returns:
        A dictionary containing the user input data.
    """
    root = tk.Tk()
    root.withdraw()
    gui = UserInputGUI(root)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
    root.destroy()
    return gui.user_data


if __name__ == "__main__":
    user_data = get_user_input()

# %%
