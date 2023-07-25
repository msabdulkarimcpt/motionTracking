from tkinter import *
import motion as mt
#import mysql.connector
import MySQLdb as sql

# Establish a connection to MySQL
db = sql.connect(
    host="localhost",
    user="root",
    password="Superstar@123",
    database="motiondet"
)

def login():
    # Getting form data
    uname = username.get()
    pwd = password.get()
    # Applying empty validation
    if uname == '' or pwd == '':
        message.set("Fill the empty field!!!")
    else:
        # Create a cursor object to execute SQL queries
        cursor = db.cursor()
        # Execute SQL query to retrieve the user with the entered username and password
        query = "SELECT * FROM userlogin WHERE username = %s AND password = %s"
        values = (uname, pwd)
        cursor.execute(query, values)
        # Fetch the result
        result = cursor.fetchone()
        if result:
            message.set("Login success")
            login_screen.after(2000, lambda: login_screen.destroy())
            mt.motion_track()
        else:
            message.set("Wrong username or password!!!")

def Loginform():
    global login_screen
    login_screen = Tk()
    login_screen.title("Login Form")
    login_screen.geometry("300x250")
    login_screen.configure(bg="#D1E5F0")  # Set light blue background color

    global message
    global username
    global password
    username = StringVar()
    password = StringVar()
    message = StringVar()

    Label(login_screen, width="300", text="Please enter details below", bg="#3370CC", fg="white").pack()
    Label(login_screen, text="Username * ", bg="#D1E5F0").place(x=20, y=40)
    Entry(login_screen, textvariable=username).place(x=110, y=42)
    Label(login_screen, text="Password * ", bg="#D1E5F0").place(x=20, y=80)
    Entry(login_screen, textvariable=password, show="*").place(x=110, y=82)
    Label(login_screen, text="", textvariable=message, bg="#FFFF11").place(x=75, y=170)
    Button(login_screen, text="Login", width=10, height=1, bg="#3370CC", fg="white", command=login).place(x=105, y=130)

    login_screen.mainloop()

Loginform()

