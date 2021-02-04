from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():  # Generates the password
    password_entry.delete(0, END)
    # Possible password characters
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ["!", "@", "#", "$", "%", "&", "(", ")", "*", "+", "-", "\\",
               "/", "\"", "^", "?", ":", "{", "}", "[", "]", "_", "."]

    # Asks user if there is a limit on the characters
    limit = messagebox.askyesno(title="Character Limit", message="Is there a character limit?")

    # Sets up password
    if limit:
        n_l_total = int(askstring(title="coca", prompt="How many letters?"))
        n_l_upper = int(askstring(title="coca", prompt="How many uppercase letters?"))
        n_symbols = int(askstring(title="coca", prompt="How many symbols?"))
        n_numbers = int(askstring(title="coca", prompt="How many numbers?"))
    else:
        n_l_total = randint(8, 10)
        n_l_upper = n_l_total - randint(0, n_l_total)
        n_symbols = randint(2, 4)
        n_numbers = randint(2, 4)

    # Makes password
    password_letters = [choice(letters) for _ in range(0, n_l_total - n_l_upper)] + \
                       [choice(letters).upper() for _ in range(0, n_l_upper)]
    password_symbols = [choice(symbols) for _ in range(0, n_symbols)]
    password_numbers = [choice(numbers) for _ in range(0, n_numbers)]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)  # The join method puts all items in an iterable into a list
    password_entry.insert(0, string=password)
    pyperclip.copy(password)  # This copies the password on to your clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():  # Saves the password into the json file
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:

        try:  # This can fail
            with open("data.json", mode="r") as data:  # This closes the file automatically later on
                # Reading old data if the file is already there
                data_file = json.load(data)
        except FileNotFoundError:  # This deals with any failures
            with open("data.json", mode="w") as data:
                json.dump(new_data, data, indent=4)
        else:  # This runs if there are no issues
            # Updating old data with new data
            data_file.update(new_data)
            with open("data.json", mode="w") as data:
                # Saving updated data
                json.dump(data_file, data, indent=4)
        finally:  # This runs regardless of the errors or not
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():  # Checks to see if the website is already in the json file
    website = website_entry.get()
    try:  # Tries this first
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:  # If the password is not found
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message="No details for this website exists.")


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=0, column=0)
email_label = Label(text="Info/Username:")
email_label.grid(row=1, column=0)
password_label = Label(text="Password:")
password_label.grid(row=2, column=0)

# Entries
website_entry = Entry(width=24, highlightthickness=0)
website_entry.grid(row=0, column=1, columnspan=2, sticky=W)
website_entry.focus()  # This will put the cursor here at the beginning
email_entry = Entry(width=30, highlightthickness=0)
email_entry.grid(row=1, column=1, columnspan=2)
email_entry.insert(0, string="YourEmail@email.com")  # Enter your email if you use it often
password_entry = Entry(width=15, highlightthickness=0)
password_entry.grid(row=2, column=1)

# Buttons
search_button = Button(text="Search", highlightthickness=0, width=5, command=find_password)
search_button.grid(row=0, column=2, sticky=E)
password_button = Button(text="Generate Password", highlightthickness=0, width=14, command=generate_password)
password_button.grid(row=2, column=2)
add_button = Button(text="Add to Password Manager", highlightthickness=0, width=30, command=save)
add_button.grid(row=3, column=1, columnspan=2)

window.mainloop()
