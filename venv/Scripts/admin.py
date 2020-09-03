from tkinter import *
from tkinter import messagebox


class admin(object):

    def __init__(self, cursor, loginWindow, db):
        self.cursor = cursor
        self.loginWindow = loginWindow
        self.db = db
        global users
        self.setupGUI()

    def setupGUI(self):
        adminWindow = Tk()
        adminWindow.title("Hospital Management System")
        width = 780
        height = 200
        adminWindow.maxsize(width, height)
        adminWindow.minsize(width, height)
        x = (adminWindow.winfo_screenwidth() // 2) - (width // 2)
        y = (adminWindow.winfo_screenheight() // 2) - (height // 2)
        adminWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        adminWindow.configure(bg='white')

        userview = ttk.Treeview(adminWindow)

        userview["columns"] = ["ID", "Full Name", "Email", "Password", "Shift", "Phone"]
        userview.column("ID", minwidth=20, width=20, stretch=False)
        userview.column("Full Name", minwidth=150, width=150, stretch=False)
        userview.column("Email", minwidth=200, width=200, stretch=False)
        userview.column("Password", minwidth=140, width=140, stretch=False)
        userview.column("Shift", minwidth=140, width=140, stretch=False)
        userview.column("Phone", minwidth=140, width=140, stretch=False)

        userview["show"] = "headings"
        userview.heading("ID", text="ID", )
        userview.heading("Full Name", text="Full Name")
        userview.heading("Email", text="Email")
        userview.heading("Password", text="Password")
        userview.heading("Shift", text="Shift")
        userview.heading("Phone", text="Phone")
        userview.pack(fill='both')

        self.fillusers(userview)

        def onDoubleClickUser(event):
            global users
            adminWindow.withdraw()
            selectedUser = users[int(userview.selection()[0])]

            userEditWindow = Tk()
            # window title
            userEditWindow.title("Hospital Management System")
            # windows height and width
            width = 400
            height = 400
            # windows max size and placement on center of the screen
            userEditWindow.maxsize(width, height)
            userEditWindow.minsize(width, height)
            x = (userEditWindow.winfo_screenwidth() // 2) - (width // 2)
            y = (userEditWindow.winfo_screenheight() // 2) - (height // 2)
            userEditWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            userEditWindow.configure(bg='green')

            headingEdit = Label(userEditWindow, text="EDIT USER", font=('verdana 18 bold'), fg='yellow',
                                bg='green')
            headingEdit.place(relx=.36, rely=0.05)
            # Adding username and password label,entry

            usernameLabelEdit = Label(userEditWindow, text="USERNAME", font=('arial 12 normal'), fg='white',
                                      bg='green')
            usernameLabelEdit.place(relx=.16, y=100)

            usernameEntryEdit = Entry(userEditWindow, width=26)
            usernameEntryEdit.place(relx=.44, y=102)
            usernameEntryEdit.insert(0, selectedUser[1])

            emailLabelEdit = Label(userEditWindow, text="EMAIL", font=('arial 12 normal'), fg='white', bg='green')
            emailLabelEdit.place(relx=.16, y=140)

            emailEntryEdit = Entry(userEditWindow, width=26)
            emailEntryEdit.place(relx=.44, y=142)
            emailEntryEdit.insert(0, selectedUser[2])

            phoneLabelEdit = Label(userEditWindow, text="PHONE", font=('arial 12 normal'), fg='white', bg='green')
            phoneLabelEdit.place(relx=.16, y=180)

            phoneEntryEdit = Entry(userEditWindow, width=26)
            phoneEntryEdit.place(relx=.44, y=182)
            phoneEntryEdit.insert(0, selectedUser[5])

            passwordLabelEdit = Label(userEditWindow, text="PASSWORD", font=('arial 12 normal'), fg='white',
                                      bg='green')
            passwordLabelEdit.place(relx=.16, y=220)

            passwordEntryEdit = Entry(userEditWindow, width=26)
            passwordEntryEdit.place(relx=.44, y=222)
            passwordEntryEdit.insert(0, selectedUser[3])

            def onClickSave():
                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

                name = usernameEntryEdit.get()
                email = emailEntryEdit.get()
                phone = phoneEntryEdit.get()
                password = passwordEntryEdit.get()

                if (len(name) == 0 or len(email) == 0 or len(phone) == 0 or len(password) == 0):
                    messagebox.showerror("Error", "All Fields are required")

                elif not (re.search(regex, email)):
                    messagebox.showerror("Error", "Invalid email")
                elif (len(phone) > 10 or len(phone) < 10 or not phone.isdigit()):
                    messagebox.showerror("Error", "Phone number must consist of 10 digits.")

                else:
                    edit_sql = "UPDATE users SET name=%s,email=%s,password=%s,phone=%s WHERE id=%s"
                    edit_values = (name, email, password, phone, int(selectedUser[0]))
                    self.cursor.execute(edit_sql, edit_values)
                    self.db.commit()
                    messagebox.showinfo("Success", "Succesfully Edited")
                    closeuserEditWindow()
                    userview.delete(*userview.get_children())
                    self.fillusers(userview)

            Edit = Button(userEditWindow, text='Edit', font=('arial 12 normal'), width=10, height=1, fg='white',
                          bg='red',
                          command=onClickSave)
            Edit.place(relx=.42, y=300)

            def showAdminWindow():
                adminWindow.deiconify()
                adminWindow.update()

            def closeuserEditWindow():
                userEditWindow.destroy()
                showAdminWindow()

            userEditWindow.protocol("WM_DELETE_WINDOW", closeuserEditWindow)

        userview.bind("<Double-1>", onDoubleClickUser)

        def closeAdminWindow():
            adminWindow.destroy()
            self.loginWindow.deiconify()
            self.loginWindow.update()

        adminWindow.protocol("WM_DELETE_WINDOW", closeAdminWindow)
        adminWindow.mainloop()

    def fillusers(self, userview):
        global users
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        user_index = 0
        for user in users:
            userview.insert("", user_index, user_index, values=user)
            user_index = user_index + 1
