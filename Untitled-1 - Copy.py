import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Root window setup
root = Tk()
root.title("Event Scheduling System")
root.geometry("1000x1000")
root.config(bg="maroon")

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
        if not (event_type.get() and event_address.get() and timeanddate.get() and costumer_name.get() and contact_number.get()):
            raise ValueError("Please fill all the fields")

        # Insert data into the database
        conn = sqlite3.connect('E:/python/1db.db')
        c = conn.cursor()

        c.execute("INSERT INTO INPUT VALUES (:event, :event_address, :timeanddate, :costumer_name, :contact_number)", {
            'event': event_type.get(),
            'event_address': event_address.get(),
            'timeanddate': timeanddate.get(),
            'costumer_name': costumer_name.get(),
            'contact_number': contact_number.get(),
        })

        conn.commit()
        conn.close()

        # Clear fields after insert
        event_type.set('')
        event_address.delete(0, END)
        timeanddate.delete(0, END)
        costumer_name.delete(0, END)
        contact_number.delete(0, END)

        messagebox.showinfo("Success", "Event successfully added!")

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to edit a record
def e():
    editor = Tk()
    editor.title('Update Event')
    editor.geometry("1000x1000")
    editor.config(bg="maroon")



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
        event_editor = ttk.Combobox(editor, values=["Wedding", "Birthday", "Conference", "Party"], width=30)
        event_editor.grid(row=0, column=1, pady=10)
        event_editor.set(record[0])

        event_label = Label(editor, text="Event Type", bg="Maroon", fg="white", font=("Ariel", 12, "bold"))
        event_label.grid(row=0, column=0, padx=10, pady=10)

        event_address_editor = ttk.Entry(editor, width=30)
        event_address_editor.grid(row=1, column=1, pady=10)
        event_address_editor.insert(0, record[1])

        event_address_label = Label(editor, text="Event Address", bg="Maroon", fg="white", font=("Ariel", 12, "bold"))
        event_address_label.grid(row=1, column=0, padx=10, pady=10)

        timeanddate_editor = ttk.Entry(editor, width=30)
        timeanddate_editor.grid(row=2, column=1, pady=10)
        timeanddate_editor.insert(0, record[2])

        timeanddate_label = Label(editor, text="Date & Time", bg="Maroon", fg="white", font=("Ariel", 12, "bold"))
        timeanddate_label.grid(row=2, column=0, padx=10, pady=10)

        costumer_name_editor = ttk.Entry(editor, width=30)
        costumer_name_editor.grid(row=3, column=1, pady=10)
        costumer_name_editor.insert(0, record[3])

        costumer_name_label = Label(editor, text="Customer Name", bg="Maroon", fg="white", font=("Ariel", 12, "bold"))
        costumer_name_label.grid(row=3, column=0, padx=10, pady=10)

        contact_number_editor = ttk.Entry(editor, width=30)
        contact_number_editor.grid(row=4, column=1, pady=10)
        contact_number_editor.insert(0, record[4])

        contact_number_label = Label(editor, text="Contact Number", bg="Maroon", fg="white", font=("Ariel", 12, "bold"))
        contact_number_label.grid(row=4, column=0, padx=10, pady=10)

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
            messagebox.showinfo("Success", "Event updated successfully!")
            q()

        save_btn = ttk.Button(editor, text="Save Changes", command=save_update)
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
        messagebox.showinfo("Success", "Event deleted successfully!")

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

        # Clear the Treeview
        for row in treeview.get_children():
            treeview.delete(row)

        # Insert records into the Treeview
        for record in records:
            treeview.insert("", "end", values=(record[0], record[1], record[2], record[3], record[4], record[5]))

        conn.commit()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# UI elements
event_label = Label(root, text="Event Type", bg="Maroon", fg="white", font=("Ariel", 12, "bold"))
event_label.grid(row=0, column=0, padx=20, pady=5, sticky=E)

# Dropdown for event type
event_type = ttk.Combobox(root, values=["Wedding", "Birthday", "Conference", "Party"], width=30)
event_type.grid(row=0, column=1, padx=20, pady=5)

event_address_label = Label(root, text="Event Address", bg="Maroon", fg="white", font=("Ariel", 12, "bold"))
event_address_label.grid(row=1, column=0, padx=20, pady=5, sticky=E)

event_address = ttk.Entry(root, width=30)
event_address.grid(row=1, column=1, padx=20, pady=5)

timeanddate_label = Label(root, text="Date & Time", bg="Maroon", fg="white", font=("Ariel", 12, "bold"))
timeanddate_label.grid(row=2, column=0, padx=20, pady=5, sticky=E)

timeanddate = ttk.Entry(root, width=30)
timeanddate.grid(row=2, column=1, padx=20, pady=5)

costumer_name_label = Label(root, text="Customer Name", bg="Maroon", fg="white", font=("Ariel", 12, "bold"))
costumer_name_label.grid(row=3, column=0, padx=20, pady=5, sticky=E)

costumer_name = ttk.Entry(root, width=30)
costumer_name.grid(row=3, column=1, padx=20, pady=5)

contact_number_label = Label(root, text="Contact Number", bg="Maroon", fg="white", font=("Ariel", 12, "bold"))
contact_number_label.grid(row=4, column=0, padx=20, pady=5, sticky=E)

contact_number = ttk.Entry(root, width=30)
contact_number.grid(row=4, column=1, padx=20, pady=5)

delete_box_label = Label(root, text="Enter ID to Delete", bg="Maroon", fg="white", font=("Ariel", 12, "bold"))
delete_box_label.grid(row=5, column=0, padx=20, pady=5, sticky=E)

delete_box = ttk.Entry(root, width=30)
delete_box.grid(row=5, column=1, padx=20, pady=5)

# Buttons
sb = ttk.Button(root, text="Add Event", command=sm)
sb.grid(row=6, column=0, columnspan=2, pady=10, padx=20, ipadx=100)

qdr = ttk.Button(root, text="Delete Event", command=d)
qdr.grid(row=7, column=0, columnspan=2, pady=10, padx=20, ipadx=100)

qsr = ttk.Button(root, text="Show Events", command=q)
qsr.grid(row=8, column=0, columnspan=2, pady=10, padx=20, ipadx=100)

eb = ttk.Button(root, text="Edit Event", command=e)
eb.grid(row=9, column=0, columnspan=2, pady=10, padx=20, ipadx=100)

# Treeview for displaying records
columns = ("Event", "Address", "Date/Time", "Customer", "Contact", "ID")
treeview = ttk.Treeview(root, columns=columns, show="headings", height=15)

# Define headings
for col in columns:
    treeview.heading(col, text=col)

# Make treeview fill the available space
treeview.grid(row=10, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

root.grid_rowconfigure(10, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
