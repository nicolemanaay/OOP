import sqlite3
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("CRUD Application")
root.geometry("700x700")
root.config(bg = "maroon")

# Database Connection
conn = sqlite3.connect('E:/python/1db.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS INPUT (
    event TEXT,
    event_address TEXT,
    timeanddate TEXT,
    costumer_name TEXT,
    contact_number INTEGER
)""")

conn.commit()

# Function to add a record
def sm():
    try:
        # Check if fields are empty
        if not (event.get() and event_address.get() and timeanddate.get() and costumer_name.get() and contact_number.get()):
            raise ValueError("Please fill all the fields")

        # Insert data into the database
        conn = sqlite3.connect('E:/python/1db.db')
        c = conn.cursor()

        c.execute("INSERT INTO INPUT VALUES (:event, :event_address, :timeanddate, :costumer_name, :contact_number)", {
            'event': event.get(),
            'event_address': event_address.get(),
            'timeanddate': timeanddate.get(),
            'costumer_name': costumer_name.get(),
            'contact_number': contact_number.get(),
        })

        conn.commit()
        conn.close()

        # Clear fields after insert
        event.delete(0, END)
        event_address.delete(0, END)
        timeanddate.delete(0, END)
        costumer_name.delete(0, END)
        contact_number.delete(0, END)
        
        messagebox.showinfo("Success", "Record added successfully!")

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to edit a record
def e():
    editor = Tk()
    editor.title('Update Record from Database')
    editor.geometry("700x700")
    editor.config(bg = "maroon")

    try:
        conn = sqlite3.connect('E:/python/1db.db')
        c = conn.cursor()
        record_id = delete_box.get()

        if not record_id.isdigit():
            raise ValueError("Please enter a valid ID number.")
        
        c.execute("SELECT * FROM INPUT WHERE oid=?", (record_id,))
        record = c.fetchone()

        if not record:
            raise ValueError("Record not found!")

        # Editor UI setup
        event_editor = Entry(editor, width=30)
        event_editor.grid(row=0, column=1, pady=(10, 0))
        event_editor.insert(0, record[0])

        event_label = Label(editor, text="Type of Event", bg = "Maroon", fg = "white", font =("Ariel", 12, "bold"))
        event_label.grid(row=0, column=0, padx=10, pady=(10, 0))

        event_address_editor = Entry(editor, width=30)
        event_address_editor.grid(row=1, column=1, pady=(10, 0))
        event_address_editor.insert(0, record[1])

        event_address_label = Label(editor, text="Event Address", bg = "Maroon", fg = "white", font =("Ariel", 12, "bold"))
        event_address_label.grid(row=1, column=0, padx=10, pady=(10, 0))

        timeanddate_editor = Entry(editor, width=30)
        timeanddate_editor.grid(row=2, column=1, pady=(10, 0))
        timeanddate_editor.insert(0, record[2])

        timeanddate_label = Label(editor, text="Time & Date", bg = "Maroon", fg = "white", font =("Ariel", 12, "bold"))
        timeanddate_label.grid(row=2, column=0, padx=10, pady=(10, 0))

        costumer_name_editor = Entry(editor, width=30)
        costumer_name_editor.grid(row=3, column=1, pady=(10, 0))
        costumer_name_editor.insert(0, record[3])

        costumer_name_label = Label(editor, text="Costumer Name", bg = "Maroon", fg = "white", font =("Ariel", 12, "bold"))
        costumer_name_label.grid(row=3, column=0, padx=10, pady=(10, 0))

        contact_number_editor = Entry(editor, width=30)
        contact_number_editor.grid(row=4, column=1, pady=(10, 0))
        contact_number_editor.insert(0, record[4])

        contact_number_label = Label(editor, text="Contact Number", bg = "Maroon", fg = "white", font =("Ariel", 12, "bold"))
        contact_number_label.grid(row=4, column=0, padx=10, pady=(10, 0))

        def save_update():
            updated_event = event_editor.get()
            updated_event_address = event_address_editor.get()
            updated_timeanddate = timeanddate_editor.get()
            updated_costumer_name = costumer_name_editor.get()
            updated_contact_number = contact_number_editor.get()

            # Update the record in the database
            c.execute('''UPDATE INPUT SET
                        event = ?, event_address = ?, timeanddate = ?, costumer_name = ?, contact_number = ?
                        WHERE oid = ?''',
                        (updated_event, updated_event_address, updated_timeanddate, updated_costumer_name, updated_contact_number, record_id))

            conn.commit()
            conn.close()

            editor.destroy()
            messagebox.showinfo("Success", "Record updated successfully!")
            q()

        save_btn = Button(editor, text="Save Changes", command=save_update, bg = "Grey", fg = "white",font =("Ariel", 12, "bold"))
        save_btn.grid(row=5, column=0, columnspan=2, pady=20, padx=10, ipadx=104)

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    editor.mainloop()

# Function to delete a record
def d():
    try:
        conn = sqlite3.connect('E:/python/1db.db')
        c = conn.cursor()
        record_id = delete_box.get()

        if not record_id.isdigit():
            raise ValueError("Please enter a valid ID number.")

        c.execute("DELETE from INPUT WHERE oid=?", (record_id,))
        conn.commit()
        conn.close()

        delete_box.delete(0, END)
        messagebox.showinfo("Success", "Record deleted successfully!")

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to display all records
def q():
    try:
        conn = sqlite3.connect('E:/python/1db.db')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM INPUT")
        records = c.fetchall()

        # Clear previous records from the text widget
        records_text.delete(1.0, END)

        # Append records to the text widget
        for record in records:
            records_text.insert(END, f"ID: {record[5]} | Event: {record[0]} | Address: {record[1]} | Date/Time: {record[2]} | Customer: {record[3]} | Contact: {record[4]}\n")

        conn.commit()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# UI elements
event = Entry(root, width=30)
event.grid(row=0, column=1, padx=20)
event_address = Entry(root, width=30)
event_address.grid(row=1, column=1, padx=50)
timeanddate = Entry(root, width=30)
timeanddate.grid(row=2, column=1, padx=20)
costumer_name = Entry(root, width=30)
costumer_name.grid(row=3, column=1, padx=20)
contact_number = Entry(root, width=30)
contact_number.grid(row=4, column=1, padx=20)
delete_box = Entry(root, width=30)
delete_box.grid(row=10, column=1, padx=20)

# Labels
event_label = Label(root, text="Type of Event", bg = "Maroon", fg = "white", font =("Ariel", 12, "bold"))
event_label.grid(row=0, column=0)
event_address_label = Label(root, text="Event Address", bg = "Maroon", fg = "white", font =("Ariel", 12, "bold"))
event_address_label.grid(row=1, column=0)
timeanddate_label = Label(root, text="Time and Date", bg = "Maroon", fg = "white", font =("Ariel", 12, "bold"))
timeanddate_label.grid(row=2, column=0)
costumer_name_label = Label(root, text="Customer Name", bg = "Maroon", fg = "white", font =("Ariel", 12, "bold"))
costumer_name_label.grid(row=3, column=0)
contact_number_label = Label(root, text="Contact Number", bg = "Maroon", fg = "white", font =("Ariel", 12, "bold"))
contact_number_label.grid(row=4, column=0)
delete_box_label = Label(root, text="Enter ID to delete", bg = "Maroon", fg = "white", font =("Ariel", 12, "bold"))
delete_box_label.grid(row=10, column=0)

# Buttons
sb = Button(root, text="Add Record", command=sm, bg = "Grey", fg = "white", font =("Ariel", 12, "bold"))
sb.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

qdr = Button(root, text="Delete Record", command=d, bg = "Grey", fg = "white", font =("Ariel", 12, "bold"))
qdr.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

qsr = Button(root, text="Show Records", command=q, bg = "Grey", fg = "white",font =("Ariel", 12, "bold"))
qsr.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

eb = Button(root, text="Edit Record", command=e, bg = "Grey", fg = "white",font =("Ariel", 12, "bold"))
eb.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Text widget for displaying records
records_text = Text(root, width=93, height=15)
records_text.grid(row=13, column=0, columnspan=2, padx=20, pady=10)

root.mainloop()
