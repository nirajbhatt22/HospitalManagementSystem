from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as mysql
import re


class editpatient(object):
    global regex
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    def __init__(self, cursor, db, patientview, roomview, addbutton, dischargebutton, editbutton, value):
        self.cursor = cursor
        self.db = db
        self.patientview = patientview
        self.roomview = roomview
        self.addbutton = addbutton
        self.dischargebutton = dischargebutton
        self.editbutton = editbutton
        self.value = value
        self.setup()

    def setup(self):

        editPatientWindow = Tk()
        editPatientWindow.title("Edit Patient")
        width = 470
        height = 420
        editPatientWindow.maxsize(width, height)
        editPatientWindow.minsize(width, height)
        x = (editPatientWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (editPatientWindow.winfo_screenheight() // 2) - (height // 2)
        editPatientWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        editPatientWindow.configure(bg='white')

        fullNameLabel = Label(editPatientWindow, text="* Full Name", font=('verdana 12 normal'), fg='black')
        fullNameLabel.place(relx=.05, y=15)

        fullNameEntry = Entry(editPatientWindow, width=25, fg='grey', justify='center')
        fullNameEntry.config(font=('verdana', 12))
        fullNameEntry.place(relx=.35, y=15)
        fullNameEntry.insert(0, self.value[1])

        emailLabel = Label(editPatientWindow, text="* Email", font=('verdana 12 normal'), fg='black')
        emailLabel.place(relx=.05, y=60)

        emailEntry = Entry(editPatientWindow, width=25, fg='grey', justify='center')
        emailEntry.config(font=('verdana', 12))
        emailEntry.place(relx=.35, y=60)
        emailEntry.insert(0, self.value[2])

        phoneLabel = Label(editPatientWindow, text="* Phone", font=('verdana 12 normal'), fg='black')
        phoneLabel.place(relx=.05, y=105)

        phoneEntry = Entry(editPatientWindow, width=25, fg='grey', justify='center')
        phoneEntry.config(font=('verdana', 12))
        phoneEntry.place(relx=.35, y=105)
        phoneEntry.insert(0, self.value[3])

        statusLabel = Label(editPatientWindow, text="* Status", font=('verdana 12 normal'), fg='black')
        statusLabel.place(relx=.05, y=150)

        statusEntry = Entry(editPatientWindow, width=25, fg='grey', justify='center')
        statusEntry.config(font=('verdana', 12))
        statusEntry.place(relx=.35, y=150)
        statusEntry.insert(0, self.value[4])
        statusEntry["state"] = DISABLED

        r_sql = "SELECT room_number FROM rooms WHERE status=%s "
        r_values = ("Vacant",)
        self.cursor.execute(r_sql, r_values)
        roms = self.cursor.fetchall()
        print(self.value)
        if not roms:
            roms = [self.value[5], "No Room Available"]
        r_variable = StringVar(editPatientWindow)
        roms.append(self.value[5])
        r_variable.set(value=self.value[5])

        roomLabel = Label(editPatientWindow, text="* Room", font=('verdana 12 normal'), fg='black')
        roomLabel.place(relx=.05, y=195)

        roomEntry = OptionMenu(editPatientWindow, r_variable, *roms)
        roomEntry.config(font=('verdana', 12))
        roomEntry.place(relx=.35, y=195)

        doctorLabel = Label(editPatientWindow, text="* Doctor", font=('verdana 12 normal'), fg='black')
        doctorLabel.place(relx=.05, y=250)

        self.cursor.execute("SELECT name FROM doctors")
        docs = self.cursor.fetchall()
        replaced_docs = []
        for doc in docs:
            replaced_docs.append(doc[0])
        print(replaced_docs)
        d_variable = StringVar(editPatientWindow)
        d_variable.set(value=self.value[7])

        doctorEntry = OptionMenu(editPatientWindow, d_variable, *replaced_docs)
        doctorEntry.config(font=('verdana', 12))
        doctorEntry.place(relx=.35, y=250)
        doctorEntry['menu'].config(fg='red')

        descriptionLabel = Label(editPatientWindow, text="* Description", font=('verdana 12 normal'), fg='black')
        descriptionLabel.place(relx=.05, y=305)

        descriptionEntry = Entry(editPatientWindow, width=25, fg='grey', justify='center')
        descriptionEntry.config(font=('verdana', 12))
        descriptionEntry.place(relx=.35, y=305)
        descriptionEntry.insert(0, self.value[8])

        def editSave():
            name = fullNameEntry.get()
            email = emailEntry.get()
            doctor = d_variable.get()
            print(doctor)
            room = r_variable.get()
            room = room.replace("(", "").replace(")", "").replace(",", "")
            phone = phoneEntry.get()
            description = descriptionEntry.get()

            if (len(name) == 0 or len(email) == 0 or len(doctor) == 0 or len(
                    phone) == 0 or len(room) == 0 or len(description) == 0):
                messagebox.showerror("Error", "All fields are required")

            elif not (re.search(regex, email)):
                messagebox.showerror("Error", "Invalid Email")
            elif (len(phone) > 10 or len(phone) < 10):
                messagebox.showerror("Error", "Phone number must be of 10 digit")
            elif (room[0] == "No Room Available"):
                messagebox.showerror("Error", "Selected room is not available")
            else:
                sql = "UPDATE patients SET name=%s ,email=%s, phone=%s,room_number=%s,doctor_name=%s,description=%s WHERE id=%s"
                val = (name, email, phone, room, doctor, description, self.value[0])
                self.cursor.execute(sql, val)

                self.patientview.delete(*self.patientview.get_children())
                self.cursor.execute("SELECT * FROM patients")
                patients = self.cursor.fetchall()
                patient_index = 0
                for patient in patients:
                    self.patientview.insert("", patient_index, patient_index, values=patient)
                    patient_index = patient_index + 1

                if not (self.value[5] == room):
                    ro_sql = "UPDATE rooms SET status=%s, patient_name=%s WHERE room_number=%s"
                    ro_values = ("Vacant", None, self.value[5])
                    self.cursor.execute(ro_sql, ro_values)

                    rn_sql = "UPDATE rooms SET status=%s, patient_name=%s WHERE room_number=%s"
                    rn_values = ("Occupied", name, room)
                    self.cursor.execute(rn_sql, rn_values)

                    self.roomview.delete(*self.roomview.get_children())
                    self.cursor.execute("SELECT * FROM rooms")
                    rooms = self.cursor.fetchall()
                    room_index = 0
                    for room in rooms:
                        self.roomview.insert("", room_index, room_index, values=room)
                        room_index = room_index + 1

                self.db.commit()

                messagebox.showinfo("Success", "Successfullt Edited")
                closeeditPatientWindow()

        edit_submit = Button(editPatientWindow, text="SAVE", font=('arial 12 normal'), height=1,
                             fg='white',
                             width=20,
                             bg='green', command=editSave)
        edit_submit.place(relx=.30, y=360)

        def closeeditPatientWindow():
            self.addbutton["state"] = NORMAL
            self.dischargebutton["state"] = NORMAL
            self.editbutton["state"] = NORMAL
            editPatientWindow.destroy()

        editPatientWindow.protocol("WM_DELETE_WINDOW", closeeditPatientWindow)
