import tkinter
from tkinter import ttk, messagebox
import auth
from database import connect, log_audits


def inventory_tab(notebook):
    frame = tkinter.Frame(notebook)
    notebook.add(frame, text="Inventory")

    fields = tkinter.Frame(frame)
    fields.pack(pady=4)

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT warehouse_id, name FROM warehouses")
    warehouse = [str(r[0]) + "-" + r[1] 
                 for r in cursor.fetchall()]
    conn.close()

    ##add item
    #row 0
    tkinter.Label(fields, text="Warehouse").grid(row=0, column=0)
    warehouse = ttk.Combobox(fields, values=warehouse, width=16, state="readonly")
    warehouse.grid(row=0, column=1, padx=3)

    tkinter.Label(fields, text="Item").grid(row=0, column=2)
    item = tkinter.Entry(fields, width=14)
    item.grid(row=0, column=3, padx=3)

    tkinter.Label(fields, text="Quantity").grid(row=0, column=4)
    quantity = tkinter.Entry(fields, width=6)
    quantity.grid(row=0, column=5, padx=3)

    def add_item():
        if not item.get() or not quantity.get() or not warehouse.get():
            messagebox.showwarning("Missing", "Fill all fields")
            return
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (warehouse_id, item_name, quantity) VALUES (?,?,?)",
                  (int(warehouse.get().split("-")[0]), item.get(), int(quantity.get())or 0))
        conn.commit()
        conn.close()
        log_audits(auth.current_user, "added inventory: " +item.get())
        messagebox.showinfo("Done", "Item added")
        refresh()

    tkinter.Button(fields, text="Add Item", command=add_item).grid(row=1, column=2, padx=4)

    # update stock row
    tkinter.Label(fields, text="Inventory ID").grid(row=2, column=0, pady=2)
    inventory_id = tkinter.Entry(fields, width=6)
    inventory_id.grid(row=2, column=1, padx=3)

    tkinter.Label(fields, text="New Quantity").grid(row=2, column=2)
    new_quantity = tkinter.Entry(fields, width=6)
    new_quantity.grid(row=2, column=3, padx=3)

    def stock_update():
        if not inventory_id.get() or not new_quantity.get():
            messagebox.showwarning("Missing", "Fill both fields")
            return
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET quantity=? WHERE inventory_id=?",
                  (int(new_quantity.get()), int(inventory_id.get())))
        conn.commit()
        conn.close()
        log_audits(auth.current_user, "updated inventory id=" + inventory_id.get())
        messagebox.showinfo("Done", "Stock updated")
        refresh()

    tkinter.Button(fields, text="Update Quantity", command=stock_update).grid(row=3, column=2, padx=4)

    #updated list table
    columns = ("ID", "Warehouse", "Item", "Quantity")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=160)
    tree.pack(padx=4)

    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT i.inventory_id, w.name, i.item_name, i.quantity
                     FROM inventory i JOIN warehouses w ON i.warehouse_id = w.warehouse_id""")
        for r in cursor.fetchall():
            tree.insert("", "end", values=r)
        conn.close()

    refresh()
