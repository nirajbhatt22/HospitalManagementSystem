from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
import mysql.connector as mysql
from adddoctor import *
from editdoctor import *
from addroom import *
from editroom import *
from addpatient import *


class main(object):

    def __init__(self, user, cursor, loginWindow, db):
        self.user = user
        self.cursor = cursor
        self.loginWindow = loginWindow
        self.db = db
        global doctors, rooms, patients
        self.setupGui()

    def setupGui(self):
        mainWindow = Tk()
        mainWindow.title("Hospital Management System")
        width = mainWindow.winfo_screenwidth()
        height = mainWindow.winfo_screenheight()
        mainWindow.maxsize(width, height)
        mainWindow.minsize(width, height)
        x = (mainWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (mainWindow.winfo_screenheight() // 2) - (height // 2)
        mainWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        mainWindow.configure(bg='white')

        def closeMainWindow():
            mainWindow.destroy()
            self.loginWindow.destroy()

        mainWindow.protocol("WM_DELETE_WINDOW", closeMainWindow)

        tab_parent = ttk.Notebook(mainWindow)

        tab_patients = Frame(tab_parent)
        tab_rooms = Frame(tab_parent)
        tab_doctors = Frame(tab_parent)

        tab_patients.configure(bg='green')
        tab_rooms.configure(bg='green')
        tab_doctors.configure(bg='green')

        tab_parent.add(tab_patients, text="Patients")
        tab_parent.add(tab_rooms, text="Rooms")
        tab_parent.add(tab_doctors, text="Doctors")
        tab_parent.pack(expand=1, fill='both')

        # Patients Tab
        # Patients Tab
        # Patients Tab
        # Patients Tab
        patientview = ttk.Treeview(tab_patients)

        patientview["columns"] = ["ID", "Full Name", "Email", "Phone", "Status", "Room No",
                                  "Last admitted", "Doctor", "Description"]
        patientview.column("ID", minwidth=20, width=20, stretch=False)
        patientview.column("Full Name", minwidth=150, width=150, stretch=False)
        patientview.column("Email", minwidth=200, width=200, stretch=False)
        patientview.column("Phone", minwidth=140, width=140, stretch=False)
        patientview.column("Description", minwidth=400, width=400, stretch=False)
        patientview.column("Status", minwidth=120, width=120, stretch=False)
        patientview.column("Room No", minwidth=80, width=80, stretch=False)
        patientview.column("Last admitted", minwidth=100, width=100, stretch=False)
        patientview.column("Doctor", minwidth=150, width=150, stretch=False)
        patientview["show"] = "headings"
        patientview.heading("ID", text="ID", )
        patientview.heading("Full Name", text="Full Name")
        patientview.heading("Email", text="Email")
        patientview.heading("Phone", text="Phone")
        patientview.heading("Description", text="Description")
        patientview.heading("Status", text="Status")
        patientview.heading("Room No", text="Room No")
        patientview.heading("Last admitted", text="Last admitted")
        patientview.heading("Doctor", text="Doctor")
        patientview.pack(fill='both')

        self.fillPatients(patientview)

        global selectedPatient

        def onDoubleClickPatient(event):
            global selectedPatient
            discharge_patient["state"] = NORMAL
            patient_selection = patientview.selection()
            p_selected = int(patient_selection[0])
            selectedPatient = patients[p_selected]
            print(selectedPatient)

        patientview.bind("<Double-1>", onDoubleClickPatient)

        def dischargePatient():
            global selectedPatient
            if (messagebox.askokcancel("Discharge", "Are you sure want to discharge this patient?")):
                p_sql = "UPDATE patients SET status=%s, room_number = %s WHERE id=%s"
                p_value = ("Discharged", None, selectedPatient[0])
                self.cursor.execute(p_sql, p_value)
                self.db.commit()
                patientview.delete(*patientview.get_children())
                self.fillPatients(patientview)

                r_sql = "UPDATE rooms SET status=%s, patient_name=%s"
                r_value = ("Vacant", None)
                self.cursor.execute(r_sql, r_value)
                self.db.commit()
                roomview.delete(*roomview.get_children())
                self.fillRooms(roomview)

                messagebox.showinfo("Success", "Updated Status")

        discharge_patient = Button(tab_patients, text='DISCHARGE PATIENT', font=('arial 12 normal'), width=30, height=2,
                                   fg='black',
                                   bg='white', command=dischargePatient)
        discharge_patient.place(relx=.25, rely=.40)
        discharge_patient["state"] = DISABLED

        # Rooms Tab
        # Rooms Tab
        # Rooms Tab
        # Rooms Tab
        # Rooms Tab
        roomview = ttk.Treeview(tab_rooms)

        roomview["columns"] = ["ID", "Room Number", "Status", "Patient Name"]
        roomview.column("ID", minwidth=20, width=20, stretch=False)
        roomview["show"] = "headings"
        roomview.heading("ID", text="ID", )
        roomview.heading("Room Number", text="Room Number")
        roomview.heading("Status", text="Status")
        roomview.heading("Patient Name", text="Patient Name")
        roomview.place(relx=0.25, rely=0.04)

        self.fillRooms(roomview)

        global selectedRoom

        def onDoubleClickRoom(event):
            global selectedRoom
            edit_room["state"] = NORMAL
            delete_room["state"] = NORMAL
            room_selection = roomview.selection()
            r_selected = int(room_selection[0])
            selectedRoom = rooms[r_selected]
            print(selectedRoom)

        roomview.bind("<Double-1>", onDoubleClickRoom)

        def onClickAddRoom():
            addroom(self.cursor, self.db, roomview, add_room, edit_room, delete_room)
            add_room["state"] = DISABLED
            edit_room["state"] = DISABLED
            delete_room["state"] = DISABLED

        def onClickEditRoom():
            editroom(self.cursor, self.db, roomview, add_room, edit_room, delete_room, selectedRoom)
            add_room["state"] = DISABLED
            edit_room["state"] = DISABLED
            delete_room["state"] = DISABLED

        def onClickDeleteRoom():
            global selectedRoom
            if (selectedRoom[2] == "Occupied"):
                messagebox.showinfo("Error","Cannot delete occupied room")
            elif (messagebox.askokcancel("Delete?", "Are you sure want to Delete?")):
                sql = "DELETE FROM rooms WHERE id = %s"
                v = int(selectedRoom[0])
                values = (v,)
                self.cursor.execute(sql, values)
                self.db.commit()
                messagebox.showinfo("Success", "Successfully deleted.")

                roomview.delete(*roomview.get_children())
                self.fillRooms(roomview)
                edit_room["state"] = DISABLED
                delete_room["state"] = DISABLED

        add_room = Button(tab_rooms, text='ADD ROOM', font=('verdana 12 normal'), width=15, height=2, fg='black',
                          bg='white', command=onClickAddRoom)
        add_room.place(relx=.80, rely=.05)

        edit_room = Button(tab_rooms, text='EDIT', font=('verdana 12 normal'), width=15, height=2, fg='black',
                           bg='white', command=onClickEditRoom)
        edit_room.place(relx=.80, rely=.15)
        edit_room["state"] = DISABLED

        delete_room = Button(tab_rooms, text='DELETE', font=('verdana 12 normal'), width=15, height=2, fg='black',
                             bg='white', command=onClickDeleteRoom)
        delete_room.place(relx=.80, rely=.25)
        delete_room["state"] = DISABLED

        # Patients tab required room view
        def onClickAddPatient():
            addpatient(self.cursor, self.db, patientview, roomview, add_patient, discharge_patient)

        add_patient = Button(tab_patients, text='ADD PATIENT', font=('arial 12 normal'), width=15, height=2,
                             fg='black',
                             bg='white', command=onClickAddPatient)
        add_patient.place(relx=.10, rely=.40)

        # Doctors Tab
        # Doctors Tab
        # Doctors Tab
        # Doctors Tab
        doctorview = ttk.Treeview(tab_doctors)

        doctorview["columns"] = ["ID", "Full Name", "Email", "Speciality", "Phone"]
        doctorview.column("ID", minwidth=20, width=20, stretch=False)
        # doctorview.column("Full Name", minwidth=150, width=150, stretch=False)
        # doctorview.column("Speciality", minwidth=200, width=200, stretch=False)
        # doctorview.column("Phone", minwidth=100, width=100, stretch=False)
        doctorview["show"] = "headings"
        doctorview.heading("ID", text="ID", )
        doctorview.heading("Full Name", text="Full Name")
        doctorview.heading("Email", text="Email")
        doctorview.heading("Speciality", text="Speciatlity")
        doctorview.heading("Phone", text="Phone")
        doctorview.place(relx=0, rely=0)

        self.fillDoctors(doctorview)

        global selectedDoctor

        def onDoubleClickDoctor(event):
            global selectedDoctor
            edit_doctor["state"] = NORMAL
            delete_doctor["state"] = NORMAL
            selection = doctorview.selection()
            d_selected = int(selection[0])
            selectedDoctor = doctors[d_selected]

        doctorview.bind("<Double-1>", onDoubleClickDoctor)

        def onClickAddDoctor():
            adddoctor(self.cursor, self.db, doctorview, add_doctor, edit_doctor, delete_doctor)
            add_doctor["state"] = DISABLED
            edit_doctor["state"] = DISABLED
            delete_doctor["state"] = DISABLED

        def onClickEditDoctor():
            editdoctor(self.cursor, self.db, doctorview, add_doctor, edit_doctor, delete_doctor, selectedDoctor)
            add_doctor["state"] = DISABLED
            edit_doctor["state"] = DISABLED
            delete_doctor["state"] = DISABLED

        def onClickDeleteDoctor():
            if (messagebox.askokcancel("Delete?", "Are you sure want to Delete?")):
                sql = "DELETE FROM doctors WHERE id = %s"
                v = int(selectedDoctor[0])
                values = (v,)
                self.cursor.execute(sql, values)
                self.db.commit()
                messagebox.showinfo("Success", "Successfully deleted.")

                doctorview.delete(*doctorview.get_children())
                self.fillDoctors(doctorview)
                edit_doctor["state"] = DISABLED
                delete_doctor["state"] = DISABLED

        add_doctor = Button(tab_doctors, text='ADD DOCTOR', font=('verdana 12 normal'), width=15, height=2, fg='black',
                            bg='white', command=onClickAddDoctor)
        add_doctor.place(relx=.80, rely=.05)

        edit_doctor = Button(tab_doctors, text='EDIT', font=('verdana 12 normal'), width=15, height=2, fg='black',
                             bg='white', command=onClickEditDoctor)
        edit_doctor.place(relx=.80, rely=.15)
        edit_doctor["state"] = DISABLED

        delete_doctor = Button(tab_doctors, text='DELETE', font=('verdana 12 normal'), width=15, height=2, fg='black',
                               bg='white', command=onClickDeleteDoctor)
        delete_doctor.place(relx=.80, rely=.25)
        delete_doctor["state"] = DISABLED

    def fillRooms(self, roomview):
        global rooms
        self.cursor.execute("SELECT * FROM rooms")
        rooms = self.cursor.fetchall()
        room_index = 0
        for room in rooms:
            roomview.insert("", room_index, room_index, values=room)
            room_index = room_index + 1

    def fillDoctors(self, doctorview):
        global doctors
        self.cursor.execute("SELECT * FROM doctors")
        doctors = self.cursor.fetchall()
        doctor_index = 0
        for doctor in doctors:
            doctorview.insert("", doctor_index, doctor_index, values=doctor)
            doctor_index = doctor_index + 1

    def fillPatients(self, patientsview):
        global patients
        self.cursor.execute("SELECT * FROM patients")
        patients = self.cursor.fetchall()
        patient_index = 0
        for patient in patients:
            patientsview.insert("", patient_index, patient_index, values=patient)
            patient_index = patient_index + 1
