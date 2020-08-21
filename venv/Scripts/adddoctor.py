from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as mysql
import re


class adddoctor(object):
    global regex
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    global addDoctorWindow, fullNameEntry, emailEntry, specialityEntry, phoneEntry, variable, cursor, db, btn

    def __init__(self, cursor, db, doctorview, button, editbutton, deletebutton):
        self.cursor = cursor
        self.db = db
        self.doctorview = doctorview
        self.button = button
        self.editbutton = editbutton
        self.deletebutton = deletebutton
        btn = button
        self.setup()

    def setup(self):

        addDoctorWindow = Tk()
        addDoctorWindow.title("Add Doctor")
        width = 470
        height = 350
        addDoctorWindow.maxsize(width, height)
        addDoctorWindow.minsize(width, height)
        x = (addDoctorWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (addDoctorWindow.winfo_screenheight() // 2) - (height // 2)
        addDoctorWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        addDoctorWindow.configure(bg='white')

        fullNameLabel = Label(addDoctorWindow, text="* Full Name", font=('verdana 12 normal'), fg='black')
        fullNameLabel.place(relx=.05, y=15)

        fullNameEntry = Entry(addDoctorWindow, width=25, fg='grey', justify='center')
        fullNameEntry.config(font=('verdana', 12))
        fullNameEntry.place(relx=.35, y=15)

        emailLabel = Label(addDoctorWindow, text="* Email", font=('verdana 12 normal'), fg='black')
        emailLabel.place(relx=.05, y=60)

        emailEntry = Entry(addDoctorWindow, width=25, fg='grey', justify='center')
        emailEntry.config(font=('verdana', 12))
        emailEntry.place(relx=.35, y=60)

        specialityLabel = Label(addDoctorWindow, text="* Speciality", font=('verdana 12 normal'), fg='black')
        specialityLabel.place(relx=.05, y=105)

        specs = ["Neurologist", "Cardiologist", "Dentist", "Dermatologist", "Ophthalmologist", "Nephrologist"]
        variable = StringVar(addDoctorWindow)
        variable.set(specs[1])

        specialityEntry = OptionMenu(addDoctorWindow, variable, *specs)
        specialityEntry.config(font=('verdana', 12))
        specialityEntry.place(relx=.35, y=105)
        specialityEntry['menu'].config(fg='red')

        phoneLabel = Label(addDoctorWindow, text="* Phone", font=('verdana 12 normal'), fg='black')
        phoneLabel.place(relx=.05, y=160)

        phoneEntry = Entry(addDoctorWindow, width=25, fg='grey', justify='center')
        phoneEntry.config(font=('verdana', 12))
        phoneEntry.place(relx=.35, y=160)

        def RegisterDoctor():
            name = fullNameEntry.get()
            email = emailEntry.get()
            speciality = variable.get()
            phone = phoneEntry.get()

            if (len(name) == 0 or len(email) == 0 or len(speciality) == 0 or len(
                    phone) == 0):
                messagebox.showerror("Error", "All fields are required")

            elif not (re.search(regex, email)):
                messagebox.showerror("Error", "Invalid Email")
            elif (len(phone) > 10 or len(phone) < 10):
                messagebox.showerror("Error", "Phone number must be of 10 digit")
            else:
                sql = "INSERT INTO doctors (name, email,speciality,phone) VALUES (%s, %s,%s,%s)"
                val = (name, email, speciality, phone)
                self.cursor.execute(sql, val)
                self.db.commit()
                messagebox.showinfo("Success", "Successfullt added")
                self.doctorview.delete(*self.doctorview.get_children())
                self.button["state"] = NORMAL

                self.cursor.execute("SELECT * FROM doctors")
                doctors = self.cursor.fetchall()
                doctor_index = 0
                for doctor in doctors:
                    self.doctorview.insert("", doctor_index, doctor_index, values=doctor)
                    doctor_index = doctor_index + 1
                addDoctorWindow.destroy()

        doctor_submit = Button(addDoctorWindow, text="ADD", font=('arial 12 normal'), height=1,
                               fg='white',
                               width=20,
                               bg='green', command=RegisterDoctor)
        doctor_submit.place(relx=.30, y=240)

        def closeAddDoctorWindow():
            self.button["state"] = NORMAL
            addDoctorWindow.destroy()

        addDoctorWindow.protocol("WM_DELETE_WINDOW", closeAddDoctorWindow)
