from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
from main import *
import mysql.connector as mysql

db_create = mysql.connect(
    host="localhost",
    user="root",
    passwd="password")

db_cursor = db_create.cursor()
db_cursor.execute("CREATE DATABASE IF NOT EXISTS hospital")

db = mysql.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="hospital"
)
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE  IF NOT EXISTS users (id INT NOT NULL AUTO_INCREMENT ,name VARCHAR(100) NOT NULL , email VARCHAR(200) NOT NULL ,password VARCHAR(2000) NOT NULL , shift VARCHAR(10) NOT NULL , phone VARCHAR(15) NOT NULL , PRIMARY KEY (id,email))")
cursor.execute(
    "CREATE TABLE  IF NOT EXISTS patients (id INT NOT NULL AUTO_INCREMENT ,name VARCHAR(100) NOT NULL , email VARCHAR(200) NOT NULL ,phone VARCHAR(15) NOT NULL,status VARCHAR(12) NOT NULL , room_number INT, last_admitted_date VARCHAR(200) NOT NULL, doctor_name VARCHAR(50) NOT NULL, description VARCHAR(100), PRIMARY KEY (id,email))")
cursor.execute(
    "CREATE TABLE  IF NOT EXISTS rooms (id INT NOT NULL AUTO_INCREMENT ,room_number INT NOT NULL , status VARCHAR(15) NOT NULL , patient_name VARCHAR(40), PRIMARY KEY (id,room_number))")
cursor.execute(
    "CREATE TABLE  IF NOT EXISTS doctors (id INT NOT NULL AUTO_INCREMENT ,name VARCHAR(100) NOT NULL , email VARCHAR(200) NOT NULL ,speciality VARCHAR(20) NOT NULL, phone VARCHAR(15),PRIMARY KEY (id,email))")
cursor.execute("SHOW TABLES")
print(cursor.fetchall())


class login():
    global loginWindow, width, height, emailEntry, passwordEntry, checkUser, usertype
    global regex
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    # Creating a new Tkinter Login window
    loginWindow = Tk()
    # window title
    loginWindow.title("Hospital Management System")
    # windows height and width
    width = 400
    height = 300
    # windows max size and placement on center of the screen
    loginWindow.maxsize(width, height)
    loginWindow.minsize(width, height)
    x = (loginWindow.winfo_screenwidth() // 2) - (width // 2)
    y = (loginWindow.winfo_screenheight() // 2) - (height // 2)
    loginWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    loginWindow.configure(bg='green')
    # loginWindow.tk.call('wm', 'iconphoto', loginWindow._w, PhotoImage(file='icon.png'))
    # Adding the title to the screen
    heading = Label(loginWindow, text="LOGIN", font=('verdana 18 bold'), fg='yellow',
                    bg='green')
    heading.place(relx=.42, rely=0.05)
    # Adding username and password label,entry

    usernameLabel = Label(loginWindow, text="EMAIL", font=('arial 12 normal'), fg='white', bg='green')
    usernameLabel.place(relx=.21, y=100)

    emailEntry = Entry(loginWindow, width=22)
    emailEntry.place(relx=.47, y=102)

    passwordLabel = Label(loginWindow, text="PASSWORD", font=('arial 12 normal'), fg='white', bg='green')
    passwordLabel.place(relx=.21, y=140)

    passwordEntry = Entry(loginWindow, width=22, show="*")
    passwordEntry.place(relx=.47, y=142)

    # Function to handle the login button click
    def onClickLogin():
        # Getting the email, password, remember entry fields value
        email = emailEntry.get()
        password = passwordEntry.get()

        # Checking the length of the entry fields for loginWindow
        if (len(email) != 0 and len(password) != 0):
            # Calling the user checking function
            if (email == "admin" and password == "admin123"):
                print("Hello Admin")

            else:
                query = "SELECT * FROM users WHERE email= %s AND password= %s LIMIT 1"
                query_params = (email, password)
                cursor.execute(query, query_params)
                user = cursor.fetchall()
                print(user)
                if (len(user) > 0):
                    hideLoginWindow()
                    main(user, cursor, loginWindow, db)

                else:
                    messagebox.showerror("Error", "User not found!!")

    login = Button(loginWindow, text='LOG IN', font=('arial 12 normal'), width=10, height=1, fg='white',
                   bg='red',
                   command=onClickLogin)
    login.place(relx=.42, y=205)

    def onClickRegister(event):
        hideLoginWindow()
        showRegisterWindow()

    registerLabel = Label(loginWindow, text="Register", font=('arial 12 normal'), fg='yellow', bg='green')
    registerLabel.place(relx=.8, rely=.9)
    registerLabel.bind("<Button-1>", onClickRegister)


def hideLoginWindow():
    loginWindow.withdraw()


def showLoginWindow():
    loginWindow.deiconify()
    loginWindow.update()


# Function to handle he close button in login window
def closeLoginWindow():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        loginWindow.destroy()


def showRegisterWindow():
    registerWindow = Tk()
    # window title
    registerWindow.title("Hospital Management System")
    # windows height and width
    width = 400
    height = 400
    # windows max size and placement on center of the screen
    registerWindow.maxsize(width, height)
    registerWindow.minsize(width, height)
    x = (registerWindow.winfo_screenwidth() // 2) - (width // 2)
    y = (registerWindow.winfo_screenheight() // 2) - (height // 2)
    registerWindow.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    registerWindow.configure(bg='green')

    headingRegister = Label(registerWindow, text="REGISTER", font=('verdana 18 bold'), fg='yellow',
                            bg='green')
    headingRegister.place(relx=.36, rely=0.05)
    # Adding username and password label,entry

    usernameLabelRegister = Label(registerWindow, text="USERNAME", font=('arial 12 normal'), fg='white', bg='green')
    usernameLabelRegister.place(relx=.16, y=100)

    usernameEntryRegister = Entry(registerWindow, width=26)
    usernameEntryRegister.place(relx=.44, y=102)

    emailLabelRegister = Label(registerWindow, text="EMAIL", font=('arial 12 normal'), fg='white', bg='green')
    emailLabelRegister.place(relx=.16, y=140)

    emailEntryRegister = Entry(registerWindow, width=26)
    emailEntryRegister.place(relx=.44, y=142)

    phoneLabelRegister = Label(registerWindow, text="PHONE", font=('arial 12 normal'), fg='white', bg='green')
    phoneLabelRegister.place(relx=.16, y=180)

    phoneEntryRegister = Entry(registerWindow, width=26)
    phoneEntryRegister.place(relx=.44, y=182)

    passwordLabelRegister = Label(registerWindow, text="PASSWORD", font=('arial 12 normal'), fg='white', bg='green')
    passwordLabelRegister.place(relx=.16, y=220)

    passwordEntryRegister = Entry(registerWindow, width=26, show="*")
    passwordEntryRegister.place(relx=.44, y=222)

    confirmPasswordLabelRegister = Label(registerWindow, text="CONFIRM", font=('arial 12 normal'), fg='white',
                                         bg='green')
    confirmPasswordLabelRegister.place(relx=.16, y=260)

    confirmPasswordEntryRegiter = Entry(registerWindow, width=26, show="*")
    confirmPasswordEntryRegiter.place(relx=.44, y=262)

    def onClickSave():
        name = usernameEntryRegister.get()
        email = emailEntryRegister.get()
        phone = phoneEntryRegister.get()
        password = passwordEntryRegister.get()
        confirm = confirmPasswordEntryRegiter.get()

        if (len(name) == 0 or len(email) == 0 or len(phone) == 0 or len(password) == 0 or len(confirm) == 0):
            messagebox.showerror("Error", "All Fields are required")

        elif not(re.search(regex, email)):
            messagebox.showerror("Error", "Invalid email")
        elif (len(phone) > 10 or len(phone) < 10 or not phone.isdigit()):
            messagebox.showerror("Error","Phone number must consist of 10 digits.")

        elif not (password == confirm):
            messagebox.showerror("Error", "Both password must be same")
        else:
            register_sql = "INSERT INTO users (name,email,password,shift,phone) VALUES (%s,%s,%s,%s,%s)"
            register_values = (name, email, password, "Default", phone)
            cursor.execute(register_sql, register_values)
            db.commit()
            messagebox.showinfo("Success","Succesfully registered")
            closeRegisterWindow()

    register = Button(registerWindow, text='REGISTER', font=('arial 12 normal'), width=10, height=1, fg='white',
                      bg='red',
                      command=onClickSave)
    register.place(relx=.42, y=300)

    def closeRegisterWindow():
        registerWindow.destroy()
        showLoginWindow()

    registerWindow.protocol("WM_DELETE_WINDOW", closeRegisterWindow)


# Setting the close button protocol in the login window
loginWindow.protocol("WM_DELETE_WINDOW", closeLoginWindow)
loginWindow.mainloop()

if __name__ == "__login__":
    app = login()
