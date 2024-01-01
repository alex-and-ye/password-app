from tkinter import *
from tkinter import messagebox
import random
from pyperclip import copy
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list_1 = []
    for char in range(nr_letters):
        choice = random.choice([True, False])
        if choice:
            password_list_1.append(chr(random.randint(ord("A"), ord("Z"))))
        else:
            password_list_1.append(chr(random.randint(ord("a"), ord("z"))))

    password_list_2 = [chr(random.randint(ord("0"), ord("9"))) for _ in range(nr_numbers)]
    password_list_3 = [chr(random.randint(ord("!"), ord("+"))) for _ in range(nr_symbols)]
    password_list = password_list_1+password_list_2+password_list_3
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(END, password)
    copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    global renew_password, new_entry
    renew_password = False
    new_entry = False
    new_data = {
        website_entry.get(): {
            "email": email_entry.get(),
            "password": password_entry.get()
        }
    }
    if len(email_entry.get()) == 0 or len(website_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showwarning(title="Warning", message="Please don't leave any fields empty.")
    else:
        try:
            with open("passwords.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            data = {}
        if website_entry.get() in data.keys():
            renew_password = messagebox.askokcancel(title=website_entry.get(), message=f"This website already exists: "
                                                                  f"\n\nEmail: {data[website_entry.get()]["email"]} \n"
                                                                  f"Password: {data[website_entry.get()]["password"]} "
                                                                  f"\n\nDo you want to reset email/password?")
        else:
            new_entry = messagebox.askokcancel(title=website_entry.get(), message=f"These are the details entered: "
                                                                  f"\n\nEmail: {email_entry.get()} \n"
                                                                  f"Password: {password_entry.get()} "
                                                                  f"\n\nIs it okay to save?")
        if renew_password or new_entry:
            try:
                with open("passwords.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("passwords.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("passwords.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    try:
        with open("passwords.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    else:
        if website_entry.get() in data.keys():
            messagebox.showinfo(title=website_entry.get(), message=f'Email: {data[website_entry.get()]["email"]} \n\n'
                                                                f'Password: {data[website_entry.get()]["password"]}')
        else:
            messagebox.showerror(title="Error", message="No Details For The Website Exist")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

website = Label(text="Website:")
website.focus()
website.grid(row=1, column=0)

email = Label(text="Email/Username:")
email.grid(row=2, column=0)

password_name = Label(text="Password:")
password_name.grid(row=3, column=0)

website_entry = Entry(width=33)
website_entry.grid(row=1, column=1, pady=5)

search_button = Button(text="Search", command=find_password, width=15)
search_button.grid(row=1, column=2, padx=5)

email_entry = Entry(width=53)
email_entry.insert(END, "alex_and_ye@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2, pady=10)

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1, pady=5)

generate_password = Button(text="Generate Password", command=password_generator)
generate_password.grid(row=3, column=2, padx=5)

add = Button(text="Add", width=43, command=save)
add.grid(row=4, column=1, columnspan=2, pady=5)


window.mainloop()