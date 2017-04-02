import sys
import sqlite3 as sql
connection = sql.connect("skiSlopeDatabase.db")
cursor = connection.cursor()
from tkinter import *
from tkinter import messagebox

#Imports and setting up a database connection

class UI(): #Gui Class - UI Layer
    
    def __init__(self, main):
        '''This function creates the GUI in tkinter'''
        
        #Count the number of entries in the database, return the new session ID
        cursor.execute("SELECT COUNT (*) FROM sessions")
        self.count = cursor.fetchone()[0] + 1
        
        self.main = main #Defining the window as "main"
        self.main.title("Add Session") #Giving the form a title
        self.main.geometry("300x200") #Setting the dimensions of the window
    
        #Creation of the frames, to hold all of the GUI
        self.frame1 = Frame(main)
        self.frame1.pack()
        self.frame2 = Frame(main)
        self.frame2.pack()
        self.frame3 = Frame(main)
        self.frame3.pack()
        self.frame4 = Frame(main)
        self.frame4.pack()
        self.frame5 = Frame(main)
        self.frame5.pack()
        self.frame6 = Frame(main)
        self.frame6.pack()
        
        #Creation of the labels, the text in them and there posistion in the window
        self.label1 = Label(self.frame1, text='Session ID Is: ').pack(side=LEFT)
        self.label7 = Label(self.frame1, text=self.count).pack(side=RIGHT)
        self.label2 = Label(self.frame2, text='Ski Instructor').pack(side=LEFT)
        self.label3 = Label(self.frame3, text='Session Date').pack(side=LEFT)
        self.label4 = Label(self.frame4, text='Session Time').pack(side=LEFT)
        self.label5 = Label(self.frame5, text='Session Type').pack(side=LEFT)

        #Creation of the entry box and the 4 option menus. Stored with each one is there "name" there
        #posistion in the form, and the information stored on the dropdown list

        #In each case of the option menus, a sample of dummy data is used
        self.instructor_option_tk = StringVar()
        self.InstructorOption = "Jamie Townsend"
        self.instructor_option_tk.set(self.InstructorOption)
        self.skiInstructorEntry = OptionMenu(self.frame2, self.instructor_option_tk, "Jamie Townsend", "Jon Salmon", "Zac Davis", "Kelly Sam")
        self.skiInstructorEntry.pack(side=RIGHT)

        self.date_option_tk = StringVar()
        self.DateOption = "24/03/2017"
        self.date_option_tk.set(self.DateOption)
        self.sessionDateEntry = OptionMenu(self.frame3, self.date_option_tk, "24/03/2017", "23/03/2017")
        self.sessionDateEntry.pack(side=RIGHT)

        self.time_option_tk = StringVar()
        self.TimeOption = "10:00:00"
        self.time_option_tk.set(self.TimeOption)
        self.sessionTimeEntry = OptionMenu(self.frame4, self.time_option_tk, "10:00:00", "12:00:00", "14:00:00", "16:00:00", "18:00:00", "20:00:00")
        self.sessionTimeEntry.pack(side=RIGHT)

        self.type_option_tk = StringVar()
        self.TypeOption = "Training Session"
        self.type_option_tk.set(self.TypeOption)
        self.sessionTypeEntry = OptionMenu(self.frame5, self.type_option_tk, "Training Session", "Standard Session")
        self.sessionTypeEntry.pack(side=RIGHT)

        #Creation of the buttons, the text on the button there posistion on the window
        #and the command thats run if they are pressed
        self.bAdd = Button(self.frame6, text="Add Session", command=self.Insert)
        self.bAdd.pack(side=LEFT)
        self.bBack = Button(self.frame6, text="Go Back")
        self.bBack.pack(side=RIGHT)

    def Insert(self): #Function ran when add session button is pressed
        return Persistance.insertDB(self)

class Controller():
    def __init__(self):
        #Controller class, initiates the GUI window
        main = Tk()
        menu = UI(main)
        main.mainloop()
        
class Entity():
    def __init__(self): #Entity class, holds all the data
        self.sessionID = None
        self.skiInstructor = None
        self.sessionDate = None
        self.sessionTime = None
        self.sessionType = None
        self.count = None

    def getSessionID(): #Gets value of sessionID
        cursor.execute("SELECT COUNT (*) FROM sessions")
        count = cursor.fetchone()[0] + 1
        sessionID = str(count)
        return sessionID

    def getSkiInstructor(UI): #Gets value of skiInstructor
        skiInstructor = str(UI.instructor_option_tk.get())
        return skiInstructor

    def getSessionDate(UI): #Gets value of sessionDate
        sessionDate = str(UI.date_option_tk.get())
        return sessionDate

    def getSessionTime(UI): #Gets value of sessionTime
        sessionTime = str(UI.time_option_tk.get())
        return sessionTime

    def getSessionType(UI): #Gets value of sessionType
        sessionType = str(UI.type_option_tk.get())
        return sessionType
        
class Persistance(): #Persistance layer
    def __init__(self):    
        self.sessionDetails = None 
               
    def insertDB(UI):
        '''Get values from inputs, send to SQL Database'''
        sessionDetails = [Entity.getSessionID(), Entity.getSkiInstructor(UI),
        Entity.getSessionDate(UI), Entity.getSessionTime(UI), Entity.getSessionType(UI)]
        cursor.execute('''INSERT INTO sessions (sessionID, ski_instructor, session_date,
        session_time, session_type) VALUES (?,?,?,?,?);''', sessionDetails)
        print("Data sucessfully added to the database") #Success message for coder
        
        messagebox.showinfo("Sucess", "Data Added Successfully") #Success message for user

        #Save changes to database, and close connection
        connection.commit()
        connection.close()

Controller() #Call controller to initiate window

