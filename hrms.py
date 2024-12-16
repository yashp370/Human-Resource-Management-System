#Human Resource Management System


import mysql.connector
from datetime import date
from decimal import Decimal

# Connect to MySQL database
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='yp'  
)
cursor = db.cursor()

# Tax calculation function
def calculate_tax(annual_salary):
    if annual_salary <= 250000:
        tax = 0
    elif annual_salary <= 500000:
        tax = (annual_salary - 250000) * 0.05
    elif annual_salary <= 1000000:
        tax = 250000 * 0.05 + (annual_salary - 500000) * 0.20
    else:
        tax = 250000 * 0.05 + 500000 * 0.20 + (annual_salary - 1000000) * 0.30
    return tax

# Insert employee details
def add_employee(name, department, designation, join_date, salary):
    cursor.execute("INSERT INTO employee (name, department, designation, join_date, salary) VALUES (%s, %s, %s, %s, %s)", (name, department, designation, join_date, salary))
    db.commit()
    print(f"Employee {name} added successfully!")

# Mark attendance
def mark_attendance(employee_id, attendance_date, status):
    cursor.execute("INSERT INTO attendance (employee_id, attendance_date, status) VALUES (%s, %s, %s)", (employee_id, attendance_date, status))
    db.commit()
    print("Attendance marked successfully!")

# Record salary payment manually
def record_salary_payment(employee_id, payment_date, amount):
    cursor.execute("INSERT INTO salary_payment (employee_id, payment_date, amount) VALUES (%s, %s, %s)", (employee_id, payment_date, amount))
    db.commit()
    print("Salary payment recorded successfully!")

# Record salary payment with tax calculation
def record_salary_payment_auto(employee_id, payment_date):
    cursor.execute("SELECT salary FROM employee WHERE id = %s", (employee_id,))
    result = cursor.fetchone()
    
    if result:
        annual_salary = Decimal(result[0])  # Convert to Decimal
        print(f"Annual Salary: {annual_salary}")  # Debugging print
        
        # Calculate monthly salary as Decimal
        monthly_salary = annual_salary / Decimal(12)
        print(f"Monthly Salary: {monthly_salary}")  # Debugging print

        # Calculate annual tax
        annual_tax = Decimal(calculate_tax(float(annual_salary)))  # Convert to float for tax calculation
        print(f"Annual Tax: {annual_tax}")  # Debugging print

        # Monthly tax deduction
        monthly_tax = annual_tax / Decimal(12)
        print(f"Monthly Tax: {monthly_tax}")  # Debugging print

        # Net monthly salary after tax deduction
        net_monthly_salary = monthly_salary - monthly_tax
        print(f"Net Monthly Salary: {net_monthly_salary}")  # Debugging print

        # Insert the net monthly salary into salary_payment
        cursor.execute("INSERT INTO salary_payment (employee_id, payment_date, amount) VALUES (%s, %s, %s)", 
                       (employee_id, payment_date, net_monthly_salary))
        db.commit()
        print(f"Net salary payment of {net_monthly_salary:.2f} (after {monthly_tax:.2f} tax) recorded successfully for Employee ID {employee_id}!")
    else:
        print(f"Employee ID {employee_id} not found.")


# Apply for leave
def apply_leave(employee_id, from_date,To_date ,reason):
    cursor.execute("INSERT INTO leave_request (employee_id, from_date,To_date, reason, status) VALUES (%s, %s, %s,%s, 'Pending')", (employee_id, from_date,To_date,reason))
    db.commit()
    print("Leave request submitted successfully!")

# Manage leave requests
def manage_leave_requests(status, request_id):
    cursor.execute("UPDATE leave_request SET status = %s WHERE id = %s", (status, request_id))
    db.commit()
    print("Leave request updated successfully!")

# View employee details
def view_employee_details():
    cursor.execute("SELECT * FROM employee")
    for row in cursor.fetchall():
        print(row)

# View attendance report
def view_attendance_report():
    employee_id = int(input("Enter employee ID: "))
    cursor.execute("SELECT * FROM attendance WHERE employee_id = %s", (employee_id,))
    for row in cursor.fetchall():
        print(row)

# View salary report
def view_salary_report():
    employee_id = int(input("Enter employee ID: "))
    cursor.execute("SELECT * FROM salary_payment WHERE employee_id = %s", (employee_id,))
    for row in cursor.fetchall():
        print(row)

# View leave requests
def view_leave_requests():
    employee_id = int(input("Enter employee ID: "))
    cursor.execute("SELECT * FROM leave_requests WHERE employee_id = %s", (employee_id,))
    request = cursor.fetchone()
    if request:
        print("id:",request[0])
        print("employee_id:",request[1])
        print("leave_date:",request[2])
        print("reason:",request[3])
        print("status:",request[4])
    else:
        print("Leave Request Not Fount.")
 
def view_leave_requests():
    cursor.execute("SELECT * FROM leave_request")
    for row in cursor.fetchall():
        print(row)    

# Login function
def login():
    print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username == "admin" and password == "admin@123":
        return "admin"
    elif username == "emp" and password == "emp@123":
        return "employee"
    else:
        print("Invalid credentials! Try again.")
        return None

# Admin menu
def admin_menu():
    while True:
        print("\n--- HRMS Menu ---")
        print("1. Add Employee")
        print("2. Mark Attendance")
        print("3. Record Salary Payment Manually")
        print("4. Apply for Leave")
        print("5. View Employee Details")
        print("6. View Attendance Report")
        print("7. View Salary Report")
        print("8. View Leave Requests")
        print("9. Manage Leave Requests")
        print("10. view all leave request")
        print("11. Exit")

        i = int(input("Enter your choice: "))

        if i == 1:
            name = input("Enter employee name: ")
            department = input("Enter department: ")
            designation = input("Enter designation: ")
            join_date = input("Enter join date (YYYY-MM-DD): ")
            salary = float(input("Enter salary: "))
            add_employee(name, department, designation, join_date, salary)

        elif i == 2:
            employee_id = int(input("Enter employee ID: "))
            attendance_date = input("Enter attendance date (YYYY-MM-DD): ")
            status = input("Enter status (Present, Absent, Leave): ")
            mark_attendance(employee_id, attendance_date, status)

        elif i == 3:
            employee_id = int(input("Enter employee ID: "))
            payment_date = input("Enter payment date (YYYY-MM-DD): ")
    
        # Allow the admin to choose between manual or automatic salary entry
            salary_option = input("Do you want to enter the salary manually? (yes/no): ").strip().lower()
            
            if salary_option == "yes":
                 amount = float(input("Enter amount: "))
                 record_salary_payment(employee_id, payment_date, amount)
            else:
                record_salary_payment_auto(employee_id, payment_date)

        elif i == 4:
            employee_id = int(input("Enter employee ID: "))
            from_date = input("Enter leave date (YYYY-MM-DD): ")
            To_date = input("Enter leave date (YYYY-MM-DD): ")
            reason = input("Enter reason for leave: ")
            apply_leave(employee_id, from_date,To_date ,reason)

        elif i == 5:
            view_employee_details()

        elif i == 6:
            view_attendance_report()

        elif i == 7:
            view_salary_report()

        elif i == 8:
            
            view_leave_requests()

        elif i == 9:
            request_id = int(input("Enter leave request ID: "))
            status = input("Enter new status (Approved, Rejected): ")
            manage_leave_requests(status, request_id)
            
        elif i ==10:
             view_leave_requests()
            

        elif i == 11:
            print("Thank you for using the HRMS. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Employee menu
def employee_menu():
    while True:
        print("\n--- Employee HRMS Menu ---")
        print("1. Mark Attendance")
        print("2. Apply for Leave")
        print("3. View Attendance Report")
        print("4. View Leave Requests")
        print("5. View Employee Details")
        print("6. Exit")

        i = int(input("Enter your choice: "))

        if i == 1:
            employee_id = int(input("Enter your Employee ID: "))
            attendance_date = input("Enter attendance date (YYYY-MM-DD): ")
            status = input("Enter status (Present, Absent, Leave): ")
            mark_attendance(employee_id, attendance_date, status)

        elif i == 2:
            employee_id = int(input("Enter employee ID: "))
            from_date = input("Enter leave date (YYYY-MM-DD): ")
            To_date = input("Enter leave date (YYYY-MM-DD): ")
            reason = input("Enter reason for leave: ")
            apply_leave(employee_id, from_date,To_date ,reason)


        elif i == 3:
            view_attendance_report()

        elif i == 4:
            employee_id = int(input("Enter employee ID:"))
            view_leave_requests(employee_id)

        elif i == 5:
            view_employee_details()
        

        elif i == 6:
            print("Thank you for using the HRMS. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Main menu logic with role-based access
def main_menu():
    role = login()
    if role == "admin":
        admin_menu()
    elif role == "employee":
        employee_menu()
    else:
        print("Login failed. Exiting system.")
        exit()

# Run the application
main_menu()

# Close the cursor and database connection
cursor.close()
db.close()
