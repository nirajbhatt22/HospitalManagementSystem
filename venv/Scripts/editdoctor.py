from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as mysql
import re


class editdoctor(object):
    global regex
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    global editDoctorWindow, fullNameEntry, emailEntry, specialityEntry, phoneEntry, variable, cursor, db

    def __init__(self, cursor, db, doctorview, button, editbutton, deletebutton, value):
        self.cursor = cursor
        self.db = db
        self.doctorview = doctorview
        self.button = button
        self.editbutton = editbutton
        self.deletebutton = deletebutton
        self.value = value
        print(value[1])
        self.setup()

    def setup(self):

        editDoctorWindow = Tk()
        editDoctorWindow.title("Edit Doctor")
        width = 470
        height = 350
        editDoctorWindow.maxsize(width, height)
        editDoctorWindow.minsize(width, height)
        x = (editDoctorWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (editDoctorWindow.winfo_screenheight() // 2) - (height // 2)
        editDoctorWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        editDoctorWindow.configure(bg='white')

        fullNameLabel = Label(editDoctorWindow, text="* Full Name", font=('verdana 12 normal'), fg='black')
        fullNameLabel.place(relx=.05, y=15)

        fullNameEntry = Entry(editDoctorWindow, width=25, fg='grey', justify='center')
        fullNameEntry.config(font=('verdana', 12))
        fullNameEntry.place(relx=.35, y=15)
        fullNameEntry.insert(0, self.value[1])

        emailLabel = Label(editDoctorWindow, text="* Email", font=('verdana 12 normal'), fg='black')
        emailLabel.place(relx=.05, y=60)

        emailEntry = Entry(editDoctorWindow, width=25, fg='grey', justify='center')
        emailEntry.config(font=('verdana', 12))
        emailEntry.place(relx=.35, y=60)
        emailEntry.insert(0, self.value[2])

        specialityLabel = Label(editDoctorWindow, text="* Speciality", font=('verdana 12 normal'), fg='black')
        specialityLabel.place(relx=.05, y=105)

        specs = ["Neurologist", "Cardiologist", "Dentist", "Dermatologist", "Ophthalmologist", "Nephrologist"]
        variable = StringVar(editDoctorWindow)
        variable.set(str(self.value[3]))

        specialityEntry = OptionMenu(editDoctorWindow, variable, *specs)
        specialityEntry.config(font=('verdana', 12))
        specialityEntry.place(relx=.35, y=105)
        specialityEntry['menu'].config(fg='grey')

        phoneLabel = Label(editDoctorWindow, text="* Phone", font=('verdana 12 normal'), fg='black')
        phoneLabel.place(relx=.05, y=160)

        phoneEntry = Entry(editDoctorWindow, width=25, fg='grey', justify='center')
        phoneEntry.config(font=('verdana', 12))
        phoneEntry.place(relx=.35, y=160)
        phoneEntry.insert(0, self.value[4])

        def EditDoctor():
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
                sql = "UPDATE doctors SET name=%s ,email=%s, speciality=%s,phone=%s WHERE id=%s"
                val = (name, email, speciality, phone, self.value[0])
                self.cursor.execute(sql, val)
                self.db.commit()
                messagebox.showinfo("Success", "Successfullt Edited")
                self.doctorview.delete(*self.doctorview.get_children())
                self.button["state"] = NORMAL
                self.editbutton["state"] = NORMAL
                self.deletebutton["state"] = NORMAL

                self.cursor.execute("SELECT * FROM doctors")
                doctors = self.cursor.fetchall()
                doctor_index = 0
                for doctor in doctors:
                    self.doctorview.insert("", doctor_index, doctor_index, values=doctor)
                    doctor_index = doctor_index + 1
                editDoctorWindow.destroy()

        doctor_submit = Button(editDoctorWindow, text="SAVE", font=('arial 12 normal'), height=1,
                               fg='white',
                               width=20,
                               bg='green', command=EditDoctor)
        doctor_submit.place(relx=.30, y=240)

        def closeeditDoctorWindow():
            self.button["state"] = NORMAL
            self.editbutton["state"] = NORMAL
            self.deletebutton["state"] = NORMAL
            editDoctorWindow.destroy()

        editDoctorWindow.protocol("WM_DELETE_WINDOW", closeeditDoctorWindow)
