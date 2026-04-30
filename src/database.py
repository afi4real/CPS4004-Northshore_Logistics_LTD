import sqlite3
import hashlib
import logging
from datetime import datetime

logging.basicConfig(filename="northshore.log", level=logging.INFO)

#connecting with norhshore database
def connect():
    return sqlite3.connect("northshore.db")

#connecting with hashlib library
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def log_audits(user, action):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO audit_log (username, action, timestamp) VALUES (?,?,?)",
              (user, action, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    logging.info(user + " - " + action)

def database():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, role TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS warehouses (warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, location TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS customers (customer_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, address TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS drivers (driver_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, license_number TEXT, phone TEXT, shift TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS vehicles (vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT, registration TEXT, capacity_kg REAL, status TEXT, last_maintenance TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS inventory (inventory_id INTEGER PRIMARY KEY AUTOINCREMENT, warehouse_id INTEGER, item_name TEXT, quantity INTEGER, reorder_level INTEGER)")
    cursor.execute("""CREATE TABLE IF NOT EXISTS shipments (
        shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT,
        sender_id INTEGER,
        receiver_id INTEGER,
        item_description TEXT,
        driver_id INTEGER, vehicle_id INTEGER,
        warehouse_id INTEGER, status TEXT, route_details TEXT,
        delivery_date TEXT, transport_cost REAL, payment_status TEXT, created_at TEXT)""")
    cursor.execute("CREATE TABLE IF NOT EXISTS incidents (incident_id INTEGER PRIMARY KEY AUTOINCREMENT, shipment_id INTEGER, incident_type TEXT, description TEXT, reported_at TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS audit_log (log_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, action TEXT, timestamp TEXT)")

    conn.commit()

    #admin account
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
                  ("admin", hash_password("admin123"), "admin")) #default admin and admin's password
        conn.commit()

    # sample data
    cursor.execute("SELECT COUNT(*) FROM warehouses")
    if cursor.fetchone()[0] == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO warehouses (name, location) VALUES ('London Hub', 'London')")
        cursor.execute("INSERT INTO warehouses (name, location) VALUES ('Manchester Hub', 'Manchester')")
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES ('Alice Brown', '07700900001', '12 Baker St, London')")
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES ('Bob Smith',   '07700900002', '45 Oxford Rd, Manchester')")
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES ('Carol Jones', '07700900003', '78 High St, Bristol')")
        cursor.execute("INSERT INTO drivers (name, license_number, phone, shift) VALUES ('James Wilson', 'DL-001', '07800000001', 'morning')")
        cursor.execute("INSERT INTO drivers (name, license_number, phone, shift) VALUES ('Sarah Taylor', 'DL-002', '07800000002', 'afternoon')")
        cursor.execute("INSERT INTO vehicles (registration, capacity_kg, status, last_maintenance) VALUES ('LN21 ABC', 5000, 'available', '2025-01-10')")
        cursor.execute("INSERT INTO vehicles (registration, capacity_kg, status, last_maintenance) VALUES ('MN22 XYZ', 3000, 'available', '2025-03-15')")
        cursor.execute("INSERT INTO inventory (warehouse_id, item_name, quantity, reorder_level) VALUES (1, 'Cardboard Boxes', 200, 50)")
        cursor.execute("INSERT INTO inventory (warehouse_id, item_name, quantity, reorder_level) VALUES (2, 'Packing Tape', 15, 30)")
        cursor.execute("INSERT INTO shipments (order_number, sender_id, receiver_id, item_description, driver_id, vehicle_id, warehouse_id, status, route_details, transport_cost, payment_status, created_at) VALUES ('ORD-001',1,2,'Electronics',1,1,1,'in_transit','M1 Motorway',120.0,'unpaid',?)", (now,))
        cursor.execute("INSERT INTO shipments (order_number, sender_id, receiver_id, item_description, driver_id, vehicle_id, warehouse_id, status, route_details, delivery_date, transport_cost, payment_status, created_at) VALUES ('ORD-002',2,3,'Furniture',2,2,2,'delivered','A34 Road','2025-04-01',250.0,'paid',?)", (now,))
        conn.commit()

    conn.close()

database()
