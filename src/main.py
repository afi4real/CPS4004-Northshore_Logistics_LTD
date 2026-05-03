from database import connect
import tkinter
from tkinter import ttk, messagebox
import auth, shipments, inventory, fleet

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

    # registration function
    def open_register_window():
        reg_window = tkinter.Toplevel(login_window)
        reg_window.title("Register New User")
        reg_window.geometry("300x180")

        tkinter.Label(reg_window, text="New Username").grid(row=0, column=0, pady=5)
        new_user = tkinter.Entry(reg_window)
        new_user.grid(row=0, column=1)

        tkinter.Label(reg_window, text="New Password").grid(row=1, column=0, pady=5)
        new_pass = tkinter.Entry(reg_window, show="*")
        new_pass.grid(row=1, column=1)

        tkinter.Label(reg_window, text="Role").grid(row=2, column=0, pady=5)
        new_role = tkinter.Entry(reg_window)
        new_role.grid(row=2, column=1)

        def register_now():
            if auth.register_user(new_user.get(), new_pass.get(), new_role.get()):
                messagebox.showinfo("Success", "User registered successfully")
                reg_window.destroy()
            else:
                messagebox.showerror("Error", "Registration failed! Try again!")

        tkinter.Button(reg_window, text="Register", command=register_now).grid(row=3, column=1, pady=10)

    # login function
    def login_authorize():
        if auth.login(username_input.get(), password_input.get()):
            login_window.destroy()
            main()
        else:
            error_show.config(text="Invalid username or password")

    # login button
    tkinter.Button(login_window, text="Login", command=login_authorize).grid(row=4, column=1, pady=3)

    # register button
    tkinter.Button(login_window, text="Register", command=open_register_window).grid(row=5, column=1, pady=3)

    # main loop MUST be last
    login_window.mainloop()



##main window
def main():
    main_window = tkinter.Tk()
    main_window.title("Northshore Logistics Ltd")
    main_window.geometry("950x600")

    #user info
    tkinter.Label(main_window, text="User: " + auth.current_user + "  Role: " + auth.current_role).pack(side="left", padx=4)

    #log out function
    def logout():
        auth.logout()
        main_window.destroy()
        login()

    #log out button
    tkinter.Button(main_window, text="Logout", command=logout).pack(side="right", pady=4)

    #notebook for tabs
    notebook = ttk.Notebook(main_window)
    notebook.pack(fill="both", expand=True, pady=4)

    #tab list
    tabs = [
        shipments.shipment_tab,
        inventory.inventory_tab,
        fleet.fleet_drivers_tab,
        customers_tab,
        show_reports
    ]

    if auth.current_role == "admin":
        tabs.append(show_users)
        tabs.append(audits)

    #load tabs
    for tab in tabs:
        tab(notebook)

    main_window.mainloop()


##customers tab
def customers_tab(notebook):
    frame = tkinter.Frame(notebook)
    notebook.add(frame, text="Customers")

    #form to add customers
    input_frame = tkinter.Frame(frame)
    input_frame.pack(pady= 4)

    tkinter.Label(input_frame, text="Name").grid(row=0, column=0)
    customer_name = tkinter.Entry(input_frame, width=14)
    customer_name.grid(row=0, column=1, padx=3)

    tkinter.Label(input_frame, text="Phone").grid(row=0, column=2)
    customer_phone = tkinter.Entry(input_frame, width=12)
    customer_phone.grid(row=0, column=3, padx=3)

    tkinter.Label(input_frame, text="Address").grid(row=0, column=4)
    customer_address = tkinter.Entry(input_frame, width=20)
    customer_address.grid(row=0, column=5, padx=3)

    #function for adding customers
    def add_customer():
        if not customer_name.get() or not customer_address.get():
            messagebox.showwarning("Missing", "Name and address required")
            return
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES (?,?,?)",
                  (customer_name.get(), customer_phone.get(), customer_address.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Done", "Customer added")
        load()

    #button for adding customers
    tkinter.Button(input_frame, text="Add Customer", command=add_customer).grid(row=0, column=6, padx=4)

    #tree view to show customers
    columns = ("ID", "Name", "Phone", "Address")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200)
    tree.pack(padx=4)

    #load data function
    def load():
        for row in tree.get_children():
            tree.delete(row)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        for r in cursor.fetchall():
            tree.insert("", "end", values=r)
        conn.close()

    tkinter.Button(frame, text="Refresh", command=load).pack(pady=3)
    load()


##reports tab
def show_reports(notebook):
    frame = tkinter.Frame(notebook)
    notebook.add(frame, text="Reports")

    text_box = tkinter.Text(frame, width=90, height=30, font=("Courier", 10))
    text_box.pack(padx=8, pady=5)

    def show_shipments():
        text_box.delete("1.0", "end")
        text_box.insert("end", "===SHIPMENT REPORT===\n\n")
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM shipments GROUP BY status")
        for r in cursor.fetchall():
            text_box.insert("end", r[0].upper() + " : " + str(r[1]))
        text_box.insert("end", "\n")
        cursor.execute("""SELECT s.shipment_id, s.order_number, s.item_description, s.status, c1.name, s.transport_cost
                     FROM shipments s LEFT JOIN customers c1 ON s.sender_id=c1.customer_id""")
        for r in cursor.fetchall():
            text_box.insert("end", str(r))
        conn.close()



    frame_button = tkinter.Frame(frame)
    frame_button.pack()
    tkinter.Button(frame_button, text="Shipment Report", command=show_shipments).grid(row=0, column=0, padx=8, pady=5)


##users tab
def show_users(nb):
    frame = tkinter.Frame(nb)
    nb.add(frame, text="Users")

    frame_button = tkinter.Frame(frame)
    frame_button.pack(pady=10)

    tkinter.Label(frame_button, text="Username").grid(row=0, column=0)
    user_name_input = tkinter.Entry(frame_button, width=14)
    user_name_input.grid(row=0, column=1, padx=3)

    tkinter.Label(frame_button, text="Password").grid(row=0, column=2)
    user_password_input = tkinter.Entry(frame_button, show="*", width=14)
    user_password_input.grid(row=0, column=3, padx=3)

    tkinter.Label(frame_button, text="Role").grid(row=0, column=4)
    user_role = tkinter.Entry(frame_button, width=14)
    user_role.grid(row=0, column=5, padx=3)

    #register user
    def register():
        if not user_name_input.get() or not user_password_input.get() or not user_role.get():
            messagebox.showwarning("Missing", "All fields required")
            return
        if auth.register_user(user_name_input.get(), user_password_input.get(), user_role.get()):
            messagebox.showinfo("Done, Succesfully registered user!")

        else:
            messagebox.showerror("Error !")

    tkinter.Button(frame_button, text="Register", command=register).grid(row=0, column=6, padx=4)


##audit log tab to see who is logging in and logging out.
def audits(notebook):
    frame = tkinter.Frame(notebook)
    notebook.add(frame, text="Audit Log")

    columns = ("ID", "Username", "Action")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=24)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200)
    tree.pack(padx=5, pady=5)

    def load():
        for row in tree.get_children():
            tree.delete(row)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audit_log ORDER BY log_id DESC")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    load()

##start the login function
login()
