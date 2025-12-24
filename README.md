Pharmacy Inventory & Management System
A desktop-based application built with Python and SQLite to streamline pharmacy operations, track drug inventory, and manage customer records.

*Key Features
Inventory CRUD: Full functionality to Add, View, Edit, and Delete drug records.

Smart Expiration Alerts: A built-in logic that automatically scans the database and highlights drugs expiring within the next 14 days in red.

Jalali Calendar Integration: User-friendly Persian date picker for managing expiration dates accurately.

Search Functionality: High-speed search engine to find medicines by name within the local database.

Data Export: Ability to save the current inventory list into a .txt file for reporting.

*Technical Stack
Frontend: Tkinter (Python GUI)

Backend: Python 3.13

Database: SQLite3 (Relational Database)

Libraries: jdatetime (for Persian calendar), tkinter.messagebox

**Strategic Value (Product Manager Insights)
This project demonstrates a complete product lifecycle:

User Centric Design: Tailored for Persian-speaking pharmacists with RTL support and Jalali dates.

Business Logic: Prevents financial loss by identifying expiring stock before it's too late.

Data Integrity: Implements a robust database schema to ensure customer and drug information is never lost.

***Installation
Clone the repository.

Install the required library:

Bash

pip install jdatetime
Run the application:

Bash

python final.py
