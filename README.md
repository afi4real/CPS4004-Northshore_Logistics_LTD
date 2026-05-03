*** Northshore Logistics Management System ***
---This is a simple Python desktop application I built for my BSc Computer Science Database Systems module.
The project was to create a centralised logistics management system where staffs can manage shipment, customer, inventory, vehicle, and driver.
The project's focus was mainly on understanding Python, Tkinter, and SQLite.---

***Features***
---Shipments---
Add new shipment records
Update shipment status, driver, vehicle, route, and delivery date
Record incidents (delay, damage, failed delivery, route change)
View shipment summaries and reports

---Inventory---
Add new inventory items
Update stock quantities
View inventory across warehouses

---Fleet & Drivers---
Add vehicles (registration, capacity, maintenance date)
Update vehicle status
Add drivers (name, license, phone, shift)
View all drivers and vehicles

---Customers---
Add new customers
View customer list

---Users & Security---
Login system with hashed passwords
Admin can register new users
Audit log records every action (login, logout, updates, additions)

---Reports---
Shipment summary report
Status counts (delivered, in transit, delayed, returned)

---Technologies Used---
Python 3.11
Tkinter for the GUI
SQLite as the database
hashlib for password hashing
logging for audit logs
datetime for timestamps
PyCharm as the IDE

***Project Structure***
---Code---
NORTHSHORE_LOGISTICS/

Code
   ├── auth.py              → Login,logout, user registration  
   ├── database.py          → Database creation, hashing, audit logging  
   ├── shipments.py         → Shipment management  
   ├── inventory.py         → Inventory management  
   ├── fleet.py             → Vehicles & drivers  
   ├── main.py              → Entry point (login + main window)  
   ├── northshore.db        → SQLite database (auto generated)  
   ├── northshore.log       → Audit log file  
   ├── schema.sql           → SQL schema  
   └── README.md            → Project brief  

***How to Run the Project***
Make sure you have Python 3.11 or above installed.
Open the project folder in PyCharm (or any IDE).
Ensure all .py files are in the same directory.
Run the main.py file.
The login window should open automatically.

*Default admin login:  
 Username: admin  
 Password: admin123

***Future Improvements (Can be done later)***
Improve the UI layout and styling
Add encryption for sensitive customer data
Add search filters for shipments and inventory
Add automatic low‑stock alerts
Add PDF export for reports

ERD Diagram
(docs/northshore_erd_diagram.png)