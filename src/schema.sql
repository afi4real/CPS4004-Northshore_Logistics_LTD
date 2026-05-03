CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
);

CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    address TEXT
);

CREATE TABLE IF NOT EXISTS drivers (
    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    license_number TEXT,
    phone TEXT,
    shift TEXT
);

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration TEXT,
    capacity_kg REAL,
    status TEXT,
    last_maintenance TEXT
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_id INTEGER,
    item_name TEXT,
    quantity INTEGER,
    reorder_level INTEGER
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT,
    sender_id INTEGER,
    receiver_id INTEGER,
    item_description TEXT,
    driver_id INTEGER,
    vehicle_id INTEGER,
    warehouse_id INTEGER,
    status TEXT,
    route_details TEXT,
    delivery_date TEXT,
    transport_cost REAL,
    payment_status TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS incidents (
    incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INTEGER,
    incident_type TEXT,
    description TEXT,
    reported_at TEXT
);

CREATE TABLE IF NOT EXISTS audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    action TEXT,
    timestamp TEXT
);
