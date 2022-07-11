from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import json
BACKGROUND = "#1894ff"
BUTTON_COLOR = "#1084ef"
ENTRY_COLOR = "#4aadf7"
BLUE_COLOR = '#2597FC'

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbol = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbol + password_numbers

    shuffle(password_list)

    password_gen = "".join(password_list)

    password_entry.insert(0, password_gen)

    pyperclip.copy(password_gen)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if website == "" or email == "" or password == "":
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            data_email = data[website]["email"]
            data_password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {data_email}\nPassword: {data_password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for the {website} exists")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BACKGROUND)

canvas = Canvas(width=170, height=170, bg=BACKGROUND, highlightthickness=0)
logo = PhotoImage(file="my_logo.png")
canvas.create_image(85, 85, image=logo)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", bg=BACKGROUND, fg="white")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:", bg=BACKGROUND, fg="white")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:", bg=BACKGROUND, fg="white")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=21, bg=ENTRY_COLOR, fg="white")
website_entry.grid(row=1, column=1, sticky="EW")
website_entry.focus()
email_entry = Entry(width=35, bg=ENTRY_COLOR, fg="white")
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, "for@example.com")
password_entry = Entry(width=21, bg=ENTRY_COLOR, fg="white")
password_entry.grid(row=3, column=1, sticky="W")

# Buttons
search_button = Button(text="Search", width=13, command=find_password, bg=BUTTON_COLOR, fg=BLUE_COLOR)
search_button.grid(row=1, column=2, sticky="EW")
generate_password_button = Button(text="Generate Password", command=generate_password, bg=BUTTON_COLOR, fg=BLUE_COLOR)
generate_password_button.grid(row=3, column=2, sticky="EW")
add_button = Button(text="Add", width=36, command=save, bg=BUTTON_COLOR, fg=BLUE_COLOR)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
