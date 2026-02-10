import sqlite3
from datetime import datetime

# Connect to Database
conn = sqlite3.connect("caretrack.db")
cursor = conn.cursor()


# Create Tables
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        bp TEXT,
        sugar TEXT,
        weight REAL,
        date TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        name TEXT,
        time TEXT,
        duration TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    """)

    conn.commit()


# Add Patient
def add_patient():
    name = input("Enter Name: ")
    age = input("Enter Age: ")
    gender = input("Enter Gender: ")

    cursor.execute("""
    INSERT INTO patients(name, age, gender)
    VALUES(?,?,?)
    """, (name, age, gender))

    conn.commit()
    print("Patient Added Successfully ✅")


# View Patients
def view_patients():
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()

    if not data:
        print("No Patients Found ❌")
        return

    print("\nPatients List:")
    for p in data:
        print(f"ID:{p[0]} | Name:{p[1]} | Age:{p[2]} | Gender:{p[3]}")


# Add Health Record
def add_record():
    pid = input("Enter Patient ID: ")

    bp = input("Enter BP: ")
    sugar = input("Enter Sugar Level: ")
    weight = input("Enter Weight: ")

    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    INSERT INTO records(patient_id,bp,sugar,weight,date)
    VALUES(?,?,?,?,?)
    """, (pid, bp, sugar, weight, date))

    conn.commit()
    print("Health Record Added ✅")


# View Health Records
def view_records():
    pid = input("Enter Patient ID: ")

    cursor.execute("""
    SELECT * FROM records WHERE patient_id=?
    """, (pid,))

    data = cursor.fetchall()

    if not data:
        print("No Records Found ❌")
        return

    print("\nHealth Records:")
    for r in data:
        print(f"Date:{r[5]} | BP:{r[2]} | Sugar:{r[3]} | Weight:{r[4]}")


# Add Medicine
def add_medicine():
    pid = input("Enter Patient ID: ")

    name = input("Medicine Name: ")
    time = input("Time (Morning/Evening): ")
    duration = input("Duration (Days): ")

    cursor.execute("""
    INSERT INTO medicines(patient_id,name,time,duration)
    VALUES(?,?,?,?)
    """, (pid, name, time, duration))

    conn.commit()
    print("Medicine Added ✅")


# View Medicines
def view_medicines():
    pid = input("Enter Patient ID: ")

    cursor.execute("""
    SELECT * FROM medicines WHERE patient_id=?
    """, (pid,))

    data = cursor.fetchall()

    if not data:
        print("No Medicines Found ❌")
        return

    print("\nMedicine Schedule:")
    for m in data:
        print(f"Name:{m[2]} | Time:{m[3]} | Duration:{m[4]} days")


# Health Report (Average Weight)
def health_report():
    cursor.execute("""
    SELECT p.name, AVG(r.weight)
    FROM patients p
    JOIN records r
    ON p.id = r.patient_id
    GROUP BY p.id
    """)

    data = cursor.fetchall()

    if not data:
        print("No Report Available ❌")
        return

    print("\nHealth Summary Report:")

    for row in data:
        print(f"Name:{row[0]} | Avg Weight:{round(row[1],2)} kg")


# Delete Patient
def delete_patient():
    pid = input("Enter Patient ID to Delete: ")

    cursor.execute("DELETE FROM records WHERE patient_id=?", (pid,))
    cursor.execute("DELETE FROM medicines WHERE patient_id=?", (pid,))
    cursor.execute("DELETE FROM patients WHERE id=?", (pid,))

    conn.commit()

    print("Patient Deleted Successfully ✅")


# Main Menu
def main_menu():

    create_tables()

    while True:

        print("\n====== CARETRACK – Health Manager ======")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Add Health Record")
        print("4. View Health Records")
        print("5. Add Medicine")
        print("6. View Medicines")
        print("7. Health Report")
        print("8. Delete Patient")
        print("9. Exit")

        choice = input("Choose (1-9): ")

        if choice == "1":
            add_patient()

        elif choice == "2":
            view_patients()

        elif choice == "3":
            add_record()

        elif choice == "4":
            view_records()

        elif choice == "5":
            add_medicine()

        elif choice == "6":
            view_medicines()

        elif choice == "7":
            health_report()

        elif choice == "8":
            delete_patient()

        elif choice == "9":
            print("Thank You for Using CARETRACK ❤️")
            break

        else:
            print("Invalid Choice ❌ Try Again")


# Start Program
if __name__ == "__main__":
    main_menu()
