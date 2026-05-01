import tkinter
from tkinter import ttk, messagebox
import auth

##login window
def login():
    login_window = tkinter.Tk()
    login_window.title("Northshore Logistics - Login")
    login_window.geometry("300x180")

    # username and password labels
    tkinter.Label(login_window, text="Northshore Logistics").grid(row=0, column=1, padx=10, pady=4)
    tkinter.Label(login_window, text="Username").grid(row=1, column=0, padx=10, pady=4)
    tkinter.Label(login_window, text="Password").grid(row=2, column=0, padx=10, pady=4)

    # username and password entries
    username_input = tkinter.Entry(login_window)
    username_input.grid(row=1, column=1)
    password_input = tkinter.Entry(login_window, show="*")
    password_input.grid(row=2, column=1)

    # error message
    error_show = tkinter.Label(login_window, text="")
    error_show.grid(row=3, column=0, columnspan=2)

    # login function
    def login_authorize():
        if auth.login(username_input.get(), password_input.get()):
            login_window.destroy()
            main()
        else:
            error_show.config(text="Invalid username or password")

    # login button
    tkinter.Button(login_window, text="Login", command=login_authorize).grid(row=4, column=1, pady=3)

    # main loop
    login_window.mainloop()



##main window
def main():
    main_window = tkinter.Tk()
    main_window.title("Northshore Logistics Ltd")
    main_window.geometry("950x600")

    #notebook for tabs
    notebook = ttk.Notebook(main_window)
    notebook.pack(fill="both", expand=True, pady=4)

    main_window.mainloop()


##start the login function
login()
