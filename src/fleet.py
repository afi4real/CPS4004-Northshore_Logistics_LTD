import tkinter
from tkinter import ttk, messagebox
import auth
from database import connect, log_audits


##driver tab
def fleet_drivers_tab(notebook):
    frame = tkinter.Frame(notebook)
    notebook.add(frame, text="Fleet & Drivers")

    fields = tkinter.Frame(frame)
    fields.pack(pady=4)

    #vehicles entry
    tkinter.Label(fields, text="Vehicles").grid(row=0, column=0, columnspan=6, pady=3)

    tkinter.Label(fields, text="Reg. ID").grid(row=1, column=0)
    registration_id = tkinter.Entry(fields, width=10)
    registration_id.grid(row=1, column=1, padx=3)

    tkinter.Label(fields, text="Capacity(kg)").grid(row=1, column=2)
    capacity = tkinter.Entry(fields, width=8)
    capacity.grid(row=1, column=3, padx=3)

    tkinter.Label(fields, text="Last Maint").grid(row=1, column=4)
    maintenance = tkinter.Entry(fields, width=10)
    maintenance.grid(row=1, column=5, padx=3)

    def add_vehicle():
        if not registration_id.get():
            messagebox.showwarning("Missing", "Registration required")
            return
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vehicles (registration, capacity_kg, status, last_maintenance) VALUES (?,?,'available',?)",
                  (registration_id.get(), float(capacity.get() or 0), maintenance.get()))
        conn.commit()
        conn.close()
        log_audits(auth.current_user, "added vehicle " + registration_id.get())
        messagebox.showinfo("Done", "Vehicle added")
        load_vehicles()

    tkinter.Button(fields, text="Add Vehicle", command=add_vehicle).grid(row=2, column=2)

    #status_update
    tkinter.Label(fields, text="Vehicle ID").grid(row=3, column=0)
    vehicle_id = tkinter.Entry(fields, width=5)
    vehicle_id.grid(row=3, column=1)

    tkinter.Label(fields, text="V. Status").grid(row=3, column=2)
    vehicle_status = ttk.Combobox(fields, values=["available","on route","maintenance"], width=12, state="readonly")
    vehicle_status.grid(row=3, column=3)

    def update_vehicle_status():
        if not vehicle_id.get() or not vehicle_status.get():
            messagebox.showwarning("Missing", "ID and status required")   #input missing message
            return
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE vehicles SET status=? WHERE vehicle_id=?", (vehicle_status.get(), int(vehicle_id.get())))
        conn.commit()
        conn.close()
        messagebox.showinfo("Done", "Status updated")
        load_vehicles()

    tkinter.Button(fields, text="Update Status", command=update_vehicle_status).grid(row=4, column=2)

    #list columns
    vehicle_columns = ("ID", "Registration", "Capacity kg", "Status", "Last Maintenance")
    vehicle_tree = ttk.Treeview(frame, columns=vehicle_columns, show="headings", height=6)
    for col in vehicle_columns:
        vehicle_tree.heading(col, text=col)
        vehicle_tree.column(col, width=140)
    vehicle_tree.pack(pady=4)

    def load_vehicles():
        for row in vehicle_tree.get_children():
            vehicle_tree.delete(row)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles")
        for r in cursor.fetchall():
            vehicle_tree.insert("", "end", values=r)
        conn.close()

    ##drivers entry
    tkinter.Label(fields, text="Drivers").grid(row=5, column=0, columnspan=6, pady=3)

    tkinter.Label(fields, text="Name").grid(row=6, column=0)
    driver_name = tkinter.Entry(fields, width=14)
    driver_name.grid(row=6, column=1, padx=3)

    tkinter.Label(fields, text="License").grid(row=6, column=2)
    licence_num = tkinter.Entry(fields, width=10)
    licence_num.grid(row=6, column=3, padx=3)

    tkinter.Label(fields, text="Phone").grid(row=6, column=4)
    phone_num = tkinter.Entry(fields, width=12)
    phone_num.grid(row=6, column=5, padx=3)

    tkinter.Label(fields, text="Shift").grid(row=7, column=0)
    shift = ttk.Combobox(fields, values=["morning","afternoon","night"], width=10, state="readonly")
    shift.grid(row=7, column=1, padx=3)

    def add_driver():
        if not driver_name.get() or not licence_num.get():
            messagebox.showwarning("Missing", "Name and license required")
            return
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO drivers (name, license_number, phone, shift) VALUES (?,?,?,?)",
                  (driver_name.get(), licence_num.get(), phone_num.get(), shift.get()))
        conn.commit()
        conn.close()
        log_audits(auth.current_user, "added driver " + driver_name.get())
        messagebox.showinfo("Done", "Driver added")
        load_drivers()

    tkinter.Button(fields, text="Add Driver", command=add_driver).grid(row=8, column=2)

    #updated drivers list
    driver_columns = ("ID", "Name", "License", "Phone", "Shift")
    driver_tree = ttk.Treeview(frame, columns=driver_columns, show="headings", height=6)
    for col in driver_columns:
        driver_tree.heading(col, text=col)
        driver_tree.column(col, width=150)
    driver_tree.pack(pady=4)

    def load_drivers():
        for row in driver_tree.get_children():
            driver_tree.delete(row)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drivers")
        for r in cursor.fetchall():
            driver_tree.insert("", "end", values=r)
        conn.close()


    load_vehicles()
    load_drivers()
