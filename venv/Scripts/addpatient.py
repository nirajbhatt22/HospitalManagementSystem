from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from array import *
import mysql.connector as mysql
import re
from datetime import datetime


class addpatient(object):
    global regex
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    global addPatientWindow, fullNameEntry, emailEntry, specialityEntry, phoneEntry, d_variable, r_variable
    global cursor, db

    def __init__(self, cursor, db, patientview, roomview, addbutton, dischargebutton):
        self.cursor = cursor
        self.db = db
        self.patientview = patientview
        self.roomview = roomview
        self.button = addbutton
        self.dischargebutton = dischargebutton
        self.setup()

    def setup(self):

        addPatientWindow = Tk()
        addPatientWindow.title("Add Patient")
        width = 470
        height = 400
        addPatientWindow.maxsize(width, height)
        addPatientWindow.minsize(width, height)
        x = (addPatientWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (addPatientWindow.winfo_screenheight() // 2) - (height // 2)
        addPatientWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        addPatientWindow.configure(bg='white')

        fullNameLabel = Label(addPatientWindow, text="* Full Name", font=('verdana 12 normal'), fg='black')
        fullNameLabel.place(relx=.05, y=15)

        fullNameEntry = Entry(addPatientWindow, width=25, fg='grey', justify='center')
        fullNameEntry.config(font=('verdana', 12))
        fullNameEntry.place(relx=.35, y=15)

        emailLabel = Label(addPatientWindow, text="* Email", font=('verdana 12 normal'), fg='black')
        emailLabel.place(relx=.05, y=60)

        emailEntry = Entry(addPatientWindow, width=25, fg='grey', justify='center')
        emailEntry.config(font=('verdana', 12))
        emailEntry.place(relx=.35, y=60)

        phoneLabel = Label(addPatientWindow, text="* Phone", font=('verdana 12 normal'), fg='black')
        phoneLabel.place(relx=.05, y=105)

        phoneEntry = Entry(addPatientWindow, text="* Phone", width=25, fg='grey', justify='center')
        phoneEntry.config(font=('verdana', 12))
        phoneEntry.place(relx=.35, y=105)

        doctorLabel = Label(addPatientWindow, text="* Doctor", font=('verdana 12 normal'), fg='black')
        doctorLabel.place(relx=.05, y=165)

        self.cursor.execute("SELECT name FROM doctors")
        docs = self.cursor.fetchall()
        replaced_docs = []
        for doc in docs:
            replaced_docs.append(doc[0])
        print(replaced_docs)
        d_variable = StringVar(addPatientWindow)

        doctorEntry = OptionMenu(addPatientWindow, d_variable, *replaced_docs)
        doctorEntry.config(font=('verdana', 12))
        doctorEntry.place(relx=.35, y=160)
        doctorEntry['menu'].config(fg='red')

        r_sql = "SELECT room_number FROM rooms WHERE status=%s "
        r_values = ("Vacant",)
        self.cursor.execute(r_sql, r_values)
        roms = self.cursor.fetchall()
        if not roms:
            roms = ["No Room Available"]
        r_variable = StringVar(addPatientWindow)

        roomLabel = Label(addPatientWindow, text="* Room", font=('verdana 12 normal'), fg='black')
        roomLabel.place(relx=.05, y=210)

        roomEntry = OptionMenu(addPatientWindow, r_variable, *roms)
        roomEntry.config(font=('verdana', 12))
        roomEntry.place(relx=.35, y=210)

        descriptionLabel = Label(addPatientWindow, text="* Description", font=('verdana 12 normal'), fg='black')
        descriptionLabel.place(relx=.05, y=270)

        descriptionEntry = Entry(addPatientWindow, width=25, fg='grey', justify='left')
        descriptionEntry.config(font=('verdana', 12))
        descriptionEntry.place(relx=.35, y=270)

        def RegisterPatient():
            name = fullNameEntry.get()
            email = emailEntry.get()
            doctor = d_variable.get()
            phone = phoneEntry.get()
            room = r_variable.get().replace("(", "").replace(")", "").replace(",", "")
            print(room)
            description = descriptionEntry.get()

            if (len(name) == 0 or len(email) == 0 or len(doctor) == 0 or len(
                    phone) == 0 or len(room) == 0) or len(description) == 0:
                messagebox.showerror("Error", "All fields are required")

            elif not (re.search(regex, email)):
                messagebox.showerror("Error", "Invalid Email")
            elif (len(phone) > 10 or len(phone) < 10 or not phone.isdigit()):
                messagebox.showerror("Error", "Phone number must be of 10 digit")
            elif (room == "No Room Available"):
                messagebox.showerror("Error", "Cannot add patient without vacant room")
            else:
                p_sql = "INSERT INTO patients (name, email,phone,status,room_number,last_admitted_date,doctor_name,description) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)"
                p_val = (
                    name, email, phone, "Admitted", int(room), str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S')),
                    doctor,
                    description)
                self.cursor.execute(p_sql, p_val)
                self.db.commit()

                rw_sql = "UPDATE rooms SET status= %s , patient_name = %s WHERE room_number = %s"
                rw_value = ("Occupied", name, room)
                self.cursor.execute(rw_sql, rw_value)
                self.db.commit()

                messagebox.showinfo("Success", "Successfully added")
                self.patientview.delete(*self.patientview.get_children())
                self.button["state"] = NORMAL

                self.cursor.execute("SELECT * FROM patients")
                patients = self.cursor.fetchall()
                patient_index = 0
                for patient in patients:
                    self.patientview.insert("", patient_index, patient_index, values=patient)
                    patient_index = patient_index + 1

                self.roomview.delete(*self.roomview.get_children())
                self.cursor.execute("SELECT * FROM rooms")
                rooms = self.cursor.fetchall()
                room_index = 0
                for room in rooms:
                    self.roomview.insert("", room_index, room_index, values=room)
                    room_index = room_index + 1
                addPatientWindow.destroy()

        patient_submit = Button(addPatientWindow, text="ADD", font=('arial 12 normal'), height=1,
                                fg='white',
                                width=20,
                                bg='green', command=RegisterPatient)
        patient_submit.place(relx=.30, y=320)

        def closeAddPatientWindow():

            self.button["state"] = NORMAL
            addPatientWindow.destroy()

        addPatientWindow.protocol("WM_DELETE_WINDOW", closeAddPatientWindow)
