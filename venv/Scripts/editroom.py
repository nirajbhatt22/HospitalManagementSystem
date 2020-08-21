from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as mysql
import re


class editroom(object):
    global editroomWindow, fullNameEntry, emailEntry, specialityEntry, phoneEntry, variable, cursor, db

    def __init__(self, cursor, db, roomview, button, editbutton, deletebutton, value):
        self.cursor = cursor
        self.db = db
        self.roomview = roomview
        self.button = button
        self.editbutton = editbutton
        self.deletebutton = deletebutton
        self.value = value
        print(value[1])
        self.setup()

    def setup(self):

        editroomWindow = Tk()
        editroomWindow.title("Edit Room")
        width = 470
        height = 350
        editroomWindow.maxsize(width, height)
        editroomWindow.minsize(width, height)
        x = (editroomWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (editroomWindow.winfo_screenheight() // 2) - (height // 2)
        editroomWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        editroomWindow.configure(bg='white')

        roomNumberLabel = Label(editroomWindow, text="* Room Number", font=('verdana 12 normal'), fg='black')
        roomNumberLabel.place(relx=.05, y=15)

        roomNumberEntry = Entry(editroomWindow, width=25, fg='grey', justify='center')
        roomNumberEntry.config(font=('verdana', 12))
        roomNumberEntry.place(relx=.35, y=15)
        roomNumberEntry.insert(0, self.value[1])

        statusLabel = Label(editroomWindow, text="* Status", font=('verdana 12 normal'), fg='black')
        statusLabel.place(relx=.05, y=60)

        statusEntry = Entry(editroomWindow, width=25, fg='grey', justify='center')
        statusEntry.config(font=('verdana', 12))
        statusEntry.place(relx=.35, y=60)
        statusEntry.insert(0, self.value[2])
        statusEntry["state"] = DISABLED

        patientLabel = Label(editroomWindow, text="* Patient Id", font=('verdana 12 normal'), fg='black')
        patientLabel.place(relx=.05, y=105)

        patientEntry = Entry(editroomWindow, width=25, fg='grey', justify='center')
        patientEntry.config(font=('verdana', 12))
        patientEntry.place(relx=.35, y=105)
        patientEntry.insert(0, str(self.value[3]))
        patientEntry["state"] = DISABLED

        def editRoom():
            number = roomNumberEntry.get()

            if not (number.isdigit()):
                messagebox.showerror("Error", "Room number must be digit")
            else:
                sql = "UPDATE rooms SET room_number=%s WHERE id=%s"
                val = (number, self.value[0])
                self.cursor.execute(sql, val)
                self.db.commit()
                messagebox.showinfo("Success", "Successfullt Saved")
                self.roomview.delete(*self.roomview.get_children())
                self.button["state"] = NORMAL
                self.editbutton["state"] = NORMAL
                self.deletebutton["state"] = NORMAL

                self.cursor.execute("SELECT * FROM rooms")
                rooms = self.cursor.fetchall()
                room_index = 0
                for room in rooms:
                    self.roomview.insert("", room_index, room_index, values=room)
                    room_index = room_index + 1
                editroomWindow.destroy()

        room_submit = Button(editroomWindow, text="SAVE", font=('arial 12 normal'), height=1,
                             fg='white',
                             width=20,
                             bg='green', command=editRoom)
        room_submit.place(relx=.30, y=180)

        def closeeditroomWindow():
            self.button["state"] = NORMAL
            self.editbutton["state"] = NORMAL
            self.deletebutton["state"] = NORMAL
            editroomWindow.destroy()

        editroomWindow.protocol("WM_DELETE_WINDOW", closeeditroomWindow)
