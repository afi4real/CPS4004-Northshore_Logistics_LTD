import tkinter
from tkinter import ttk, messagebox
from datetime import datetime
import auth
from database import connect, log_audits


def shipment_tab(notebook):
    frame = tkinter.Frame(notebook)
    notebook.add(frame, text="Shipments")

    ##input fields container
    fields = tkinter.Frame(frame)
    fields.pack(pady=4)

    #row 0
    tkinter.Label(fields, text="Order No").grid(row=0, column=0)
    order_num_input = tkinter.Entry(fields, width=10)
    order_num_input.grid(row=0, column=1)

    tkinter.Label(fields, text="Item").grid(row=0, column=2)
    item_input = tkinter.Entry(fields, width=14)
    item_input.grid(row=0, column=3)

    tkinter.Label(fields, text="Cost").grid(row=0, column=4)
    cost_input = tkinter.Entry(fields, width=6)
    cost_input.grid(row=0, column=5)

    ##loading dropdown options
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, name FROM customers")
    customers = [f"{r[0]}-{r[1]}" for r in cursor.fetchall()]
    cursor.execute("SELECT warehouse_id, name FROM warehouses")
    warehouses = [f"{r[0]}-{r[1]}" for r in cursor.fetchall()]
    cursor.execute("SELECT driver_id, name FROM drivers")
    drivers = [f"{r[0]}-{r[1]}" for r in cursor.fetchall()]
    cursor.execute("SELECT vehicle_id, registration FROM vehicles")
    vehicles = [f"{r[0]}-{r[1]}" for r in cursor.fetchall()]
    conn.close()

    #row 1
    tkinter.Label(fields, text="Sender").grid(row=1, column=0, pady=2)
    sender = ttk.Combobox(fields, values=customers, width=14, state="readonly")
    sender.grid(row=1, column=1)

    tkinter.Label(fields, text="Receiver").grid(row=1, column=2)
    receiver = ttk.Combobox(fields, values=customers, width=14, state="readonly")
    receiver.grid(row=1, column=3)

    tkinter.Label(fields, text="Warehouse").grid(row=1, column=4)
    warehouse = ttk.Combobox(fields, values=warehouses, width=14, state="readonly")
    warehouse.grid(row=1, column=5)

    #add shipment
    def add_shipment():
        if not order_num_input.get() or not item_input.get() or not sender.get():
            messagebox.showwarning("Missing", "Fill all fields")
            return

        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO shipments
            (order_number, sender_id, receiver_id, item_description,
             transport_cost, warehouse_id, status, payment_status, created_at)
            VALUES (?,?,?,?,?,?,'in_transit','unpaid',?)
        """, (
            order_num_input.get(),
            int(sender.get().split("-")[0]),
            int(receiver.get().split("-")[0]),
            item_input.get(),
            float(cost_input.get() or 0),
            int(warehouse.get().split("-")[0]),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

        log_audits(auth.current_user, f"added shipment {order_num_input.get()}")
        messagebox.showinfo("Done", "Shipment added")
        refresh()

    #row 2
    tkinter.Button(fields, text="Add Shipment", command=add_shipment).grid(row=2, column=3, pady=2)

    ##update section
    #row 3
    tkinter.Label(fields, text="ID").grid(row=3, column=0)
    shipment_id_input = tkinter.Entry(fields, width=6)
    shipment_id_input.grid(row=3, column=1)

    tkinter.Label(fields, text="Status").grid(row=3, column=2)
    status = ttk.Combobox(fields, values=["in_transit","delivered","delayed","returned"], width=10, state="readonly")
    status.grid(row=3, column=3)

    tkinter.Label(fields, text="Pay. Status").grid(row=3, column=4)
    payment_status = ttk.Combobox(fields, values=["paid","unpaid"], width=10, state="readonly")
    payment_status.grid(row=3, column=5)

    #row 4
    tkinter.Label(fields, text="Driver").grid(row=4, column=0)
    driver = ttk.Combobox(fields, values=drivers, width=14, state="readonly")
    driver.grid(row=4, column=1)

    tkinter.Label(fields, text="Vehicle").grid(row=4, column=2)
    vehicle = ttk.Combobox(fields, values=vehicles, width=14, state="readonly")
    vehicle.grid(row=4, column=3)

    tkinter.Label(fields, text="Route").grid(row=4, column=4)
    route = tkinter.Entry(fields, width=14)
    route.grid(row=4, column=5)

    #row 5
    tkinter.Label(fields, text="Del. Date").grid(row=5, column=0)
    delivery_date = tkinter.Entry(fields, width=12)
    delivery_date.grid(row=5, column=1)

    def update_shipment():
        if not shipment_id_input.get():
            messagebox.showwarning("Missing", "Enter shipment ID")
            return

        sid = int(shipment_id_input.get())
        conn = connect()
        cursor = conn.cursor()

        if status.get():
            cursor.execute("UPDATE shipments SET status=? WHERE shipment_id=?",
                           (status.get(), sid))
        if payment_status.get():
            cursor.execute("UPDATE shipments SET payment_status=? WHERE shipment_id=?", 
                           (payment_status.get(), sid))
        if driver.get():
            cursor.execute("UPDATE shipments SET driver_id=? WHERE shipment_id=?", 
                           (int(driver.get().split("-")[0]), sid))
        if vehicle.get():
            cursor.execute("UPDATE shipments SET vehicle_id=? WHERE shipment_id=?", 
                           (int(vehicle.get().split("-")[0]), sid))
        if route.get():
            cursor.execute("UPDATE shipments SET route_details=? WHERE shipment_id=?", 
                           (route.get(), sid))
        if delivery_date.get():
            cursor.execute("UPDATE shipments SET delivery_date=? WHERE shipment_id=?", 
                           (delivery_date.get(), sid))
        conn.commit()
        conn.close()

        log_audits(auth.current_user, f"updated shipment {sid}")
        messagebox.showinfo("Done", "Updated")
        refresh()

    #row 6
    tkinter.Button(fields, text="Update Shipment", command=update_shipment).grid(row=6, column=2, columnspan=2, pady=3)

    ##incident section
    #row 7
    tkinter.Label(fields, text="Shipment ID(Inci.)").grid(row=7, column=0)
    incident_s_id = tkinter.Entry(fields, width=6)
    incident_s_id.grid(row=7, column=1)

    tkinter.Label(fields, text="Incident").grid(row=7, column=2)
    incident = ttk.Combobox(fields, values=["delay","route_change","damaged","failed_delivery"], width=14, state="readonly")
    incident.grid(row=7, column=3)

    tkinter.Label(fields, text="Inci. Des.").grid(row=7, column=4)
    incident_description = tkinter.Entry(fields, width=20)
    incident_description.grid(row=7, column=5, columnspan=2)

    def add_incident():
        if not incident_s_id.get() or not incident.get():
            messagebox.showwarning("Missing", "ID and type required")
            return

        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO incidents (shipment_id, incident_type, description, reported_at)
            VALUES (?,?,?,?)
        """, (
            int(incident_s_id.get()),
            incident.get(),
            incident_description.get(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

        log_audits(auth.current_user, f"incident on shipment {incident_s_id.get()}")
        messagebox.showinfo("Done", "Incident saved")

    #row 8
    tkinter.Button(fields, text="Add Incident", command=add_incident).grid(row=8, column=3, pady=2)

    ##results table
    columns = ("ID","Order","Item","Status","Sender","Receiver","Driver","Vehicle","Date","Cost","Payment")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=85)
    tree.pack(pady=4)

    def refresh():
        for row in tree.get_children():
            tree.delete(row)

        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.shipment_id, s.order_number, s.item_description, s.status,
                   c1.name, c2.name, d.name, v.registration,
                   s.delivery_date, s.transport_cost, s.payment_status
            FROM shipments s
            LEFT JOIN customers c1 ON s.sender_id = c1.customer_id
            LEFT JOIN customers c2 ON s.receiver_id = c2.customer_id
            LEFT JOIN drivers d ON s.driver_id = d.driver_id
            LEFT JOIN vehicles v ON s.vehicle_id = v.vehicle_id
        """)
        for r in cursor.fetchall():
            tree.insert("", "end", values=[x if x else "-" for x in r])

        conn.close()

    refresh()