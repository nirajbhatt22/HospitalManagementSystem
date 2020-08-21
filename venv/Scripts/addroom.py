from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as mysql
import re


class addroom(object):
    global addRoomWindow, fullNameEntry, emailEntry, specialityEntry, phoneEntry, variable, cursor, db, btn

    def __init__(self, cursor, db, roomview, button, editbutton, deletebutton):
        self.cursor = cursor
        self.db = db
        self.roomview = roomview
        self.button = button
        self.editbutton = editbutton
        self.deletebutton = deletebutton
        btn = button
        self.setup()

    def setup(self):

        addRoomWindow = Tk()
        addRoomWindow.title("Add Room")
        width = 340
        height = 200
        addRoomWindow.maxsize(width, height)
        addRoomWindow.minsize(width, height)
        x = (addRoomWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (addRoomWindow.winfo_screenheight() // 2) - (height // 2)
        addRoomWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        addRoomWindow.configure(bg='white')

        roomNumber = Label(addRoomWindow, text="* Room Number", font=('verdana 12 normal'), fg='black')
        roomNumber.place(relx=.05, y=15)

        roomNumberEntry = Entry(addRoomWindow, width=10, fg='grey', justify='center')
        roomNumberEntry.config(font=('verdana', 12))
        roomNumberEntry.place(relx=.45, y=15)

        def RegisterRoom():
            number = roomNumberEntry.get()

            if not (number.isdigit()):
                messagebox.showerror("Error", "Room must be number")
            else:
                sql = "INSERT INTO rooms (room_number, status,patient_name) VALUES (%s, %s,%s)"
                val = (number, "Vacant", None)
                self.cursor.execute(sql, val)
                self.db.commit()
                messagebox.showinfo("Success", "Successfullt added")
                self.roomview.delete(*self.roomview.get_children())
                self.button["state"] = NORMAL

                self.cursor.execute("SELECT * FROM rooms")
                rooms = self.cursor.fetchall()
                room_index = 0
                for room in rooms:
                    self.roomview.insert("", room_index, room_index, values=room)
                    room_index = room_index + 1
                addRoomWindow.destroy()

        room_submit = Button(addRoomWindow, text="ADD", font=('arial 12 normal'), height=1,
                             fg='white',
                             width=20,
                             bg='green', command=RegisterRoom)
        room_submit.place(relx=.30, y=90)

        def closeaddRoomWindow():
            self.button["state"] = NORMAL
            addRoomWindow.destroy()

        addRoomWindow.protocol("WM_DELETE_WINDOW", closeaddRoomWindow)
