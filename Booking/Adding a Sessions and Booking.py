#homepage menu

import sqlite3 as sql
con = sql.connect("skiSlopeDatabase.db")
cur = con.cursor()
from tkinter import *

from tkinter import *
#importing tree
import tkinter.ttk as ttk

class BookingMenu:

    def __init__(self,root):
        self.root = root
        #adding title
        self.root.title("Booking")
        #setting up frames
        self.frame1 = Frame(self.root)
        self.frame1.pack()

        self.frame2 = Frame(self.root)
        self.frame2.pack()

        self.frame3 = Frame(self.root)
        self.frame3.pack()

        self.frame4 = Frame(self.root)
        self.frame4.pack()

        self.frame5 = Frame(self.root)
        self.frame5.pack()

        self.frame6 = Frame(self.root)
        self.frame6.pack()

        self.frame7 = Frame(self.root)
        self.frame7.pack()


        

    #Firtname entry box
        
        self.fNameLabel = Label(self.frame1,text='Firstname: ')
        self.fNameLabel.pack(side=LEFT)

        self.fNameEntry = Entry(self.frame1)
        self.fNameEntry.pack(side=RIGHT)

    #Surname entry box
        
        self.sNameLabel = Label(self.frame2,text='Surname: ')
        self.sNameLabel.pack(side=LEFT)

        self.sNameEntry = Entry(self.frame2)
        self.sNameEntry.pack(side=RIGHT)
        
    #customer id entry box

        self.customerIdLabel = Label(self.frame3,text='Customer ID: ')
        self.customerIdLabel.pack(side=LEFT)

        self.customerIdEntry = Entry(self.frame3)
        self.customerIdEntry.pack(side=LEFT)

        self.searchCustomerButton = Button(self.frame3,text='Search ID',command=self.getCustomerID)
        self.searchCustomerButton.pack(side=RIGHT)

    #primary key entry box (sessionID)

        #customer id entry box

        self.sessionIdLabel = Label(self.frame5,text='Session ID: ')
        self.sessionIdLabel.pack(side=LEFT)

        self.sessionIdEntry = Entry(self.frame5)
        self.sessionIdEntry.pack(side=RIGHT)

        #tree to display sessions

        self.sessionsTree = ttk.Treeview(self.frame6)
        self.sessionsTree["columns"] = ("two","three","four")

        self.sessionsTree.column("#0",width=100)
        self.sessionsTree.column("two",width=100)
        self.sessionsTree.column("three",width=100)
        self.sessionsTree.column("four",width=150)


        self.sessionsTree.heading("#0", text="SessionID")
        self.sessionsTree.heading("two", text="Session Date")
        self.sessionsTree.heading("three", text="Session Time")
        self.sessionsTree.heading("four", text="Session Type")
        

        self.sessionsTree.pack()

        self.attributeList = []
        self.attribute = 1

        for row in cur.execute("""SELECT * FROM sessions"""):
          self.attribute += 1
          self.attributeList.append(self.attribute - 1)

        for i in range(1,self.attribute):

          cur.execute("""SELECT session_Date FROM sessions WHERE sessionID=?""", (i,))
          self.date = cur.fetchall()

          cur.execute("""SELECT session_Time FROM sessions WHERE sessionID=?""", (i,))
          self.time = cur.fetchall()

          cur.execute("""SELECT session_type FROM sessions WHERE sessionID=?""", (i,))
          self.type = cur.fetchall()

          self.sessionsTree.insert("",i,text=i, values=(self.date,self.time,self.type))


    #enter button

        self.enterButton = Button(self.frame7,text='Enter',command=self.insertValues)
        self.enterButton.pack(side=RIGHT)
        
    #Go back button
        self.backButton = Button(self.frame7,text='Go Back')
        self.backButton.pack(side=LEFT)


    #fuction for inserting values into the database

    def insertValues(self):
       
        #assinging entry field to variable and putting it into a list
        
        customerId = str(self.customerIdEntry.get())
        customerFirstname = str(self.fNameEntry.get())
        customerSurname = str(self.sNameEntry.get())
        sessionId = str(self.sessionIdEntry.get())
        cur.execute("""SELECT COUNT (DISTINCT booking_ref) FROM BookingList;""") #counting number of bookings to generate a booking ref
        bookRef = int(cur.fetchone()[0])+1 #working out the booking ref (take total number of bookings and add one
        bookingDetails = [sessionId,customerId,customerFirstname,customerSurname,bookRef] #list of values to insert into bookings table

        #getting customer name for cutomerID test

        firstname = str(self.fNameEntry.get())
        surname = str(self.sNameEntry.get())
        customerName = [firstname,surname]
        


        cur.execute('''SELECT sessionID FROM sessions WHERE sessionID = ?;''',sessionId)

        try:
            sessionIDTest = str(cur.fetchone()[0])
            cur.execute('''SELECT * FROM customers WHERE customer_Firstname = ? AND customer_Surname = ? ;''',customerName)
            customerID = str(cur.fetchone()[0])
            if customerId != customerID:

                window = Toplevel()
                Label(window,text = 'Error\n CustomerID does not match the customerID in the database').pack()
                Button(window,text='OK',command=window.destroy).pack()
                
            else:
                cur.execute('''INSERT INTO BookingList (sessionID,customerID,customer_Firstname,customer_Surname,booking_ref) VALUES (?,?,?,?,?);''', bookingDetails)
                #opening new window
                window = Toplevel()
                Label(window,text = 'Success! \n sucessfully booked customer into session\n Your booking refernce is : ' + str(bookRef)).pack()
                Button(window,text='OK',command=window.destroy).pack()
                
                con.commit()
                con.close()

        except TypeError: #if the fetchone value is a NoneType run error window message

            window = Toplevel()
            Label(window,text = ("Error \n SessionID doesn't exist")).pack()
            Button(window,text='OK',command=window.destroy).pack()

            
        
    def getCustomerID(self):
        firstname = str(self.fNameEntry.get())
        surname = str(self.sNameEntry.get())

        customerName = [firstname,surname]
        
        cur.execute('''SELECT * FROM customers WHERE customer_Firstname = ? AND customer_Surname = ? ;''',customerName)
        try:
            customerID = str(cur.fetchone()[0])
            window = Toplevel()
            Label(window,text = (firstname + " " + surname + " Customer ID: " + customerID)).pack()
            Button(window,text='OK',command=window.destroy).pack()
            
        except TypeError: #if the fetchone value is a NoneType run error window message
            window = Toplevel()
            Label(window,text = (firstname + " " + surname + "\n" + "This Customer is not in the database\n Please register the customer to book a session")).pack()
            Button(window,text='OK',command=window.destroy).pack()

    def goBackHome(self):

        self.root.destroy()
        home = Tk()
        homePage = HomePage(home)
        home.mainloop()
        

class AddSession:
    def __init__(self,main):
        self.main = main
        self.main.title("Add Session")
        self.main.geometry("375x150")

        self.label1 = Label(self.main, text='Session ID').grid(row=3, column=0)
        self.label2 = Label(self.main, text='Ski Instructor').grid(row=4, column=0)
        self.label3 = Label(self.main, text='Session Date YYYY-MM-DD').grid(row=5, column=0)
        self.label4 = Label(self.main, text='Session Time HH:MM:SS').grid(row=6, column=0)
        self.label5 = Label(self.main, text='Session Type').grid(row=7, column=0)

        self.sessionIDEntry = Entry(self.main)
        self.sessionIDEntry .grid(row=3,column=1)        
        self.skiInstructorEntry = Entry(self.main)
        self.skiInstructorEntry.grid(row=4, column=1)
        self.sessionDateEntry = Entry(self.main)
        self.sessionDateEntry.grid(row=5, column=1)
        self.sessionTimeEntry = Entry(self.main)
        self.sessionTimeEntry.grid(row=6, column=1)
        self.sessionTypeEntry = Entry(self.main)
        self.sessionTypeEntry.grid(row=7, column=1)

        self.bAdd = Button(self.main, text="Add to Database", command=self.insertDB).grid(row=3, column=2)
        self.bBack = Button(self.main, text="Go Back",command=self.goBackHome).grid(row=7, column=2)

    def insertDB(self):
        
        sessionID = str(self.sessionIDEntry.get())
        skiInstructor = str(self.skiInstructorEntry.get())
        sessionDate = str(self.sessionDateEntry.get())
        sessionTime = str(self.sessionTimeEntry.get())
        sessionType = str(self.sessionTypeEntry.get())
        
        sessionDetails = [sessionID, skiInstructor,sessionDate,sessionTime,sessionType]
        cur.execute('''INSERT INTO sessions (sessionID, ski_instructor, session_date, session_time, session_type) VALUES (?,?,?,?,?);''', sessionDetails)
        
        con.commit()
        
    def goBackHome(self):

        self.main.destroy()
        home = Tk()
        homePage = HomePage(home)
        home.mainloop()


class HomePage:
    def __init__(self,root):
        self.root = root
        self.root.title("Ski Slope Booking System")
        self.root.geometry("205x150")

        self.addSessionButton = Button(self.root, text="Add Session",command=self.goToAddSession).grid(row=3,column=0)

        self.BookingButton = Button(self.root, text="Add Booking",command=self.goToBooking).grid(row=3,column=1)


    def goToAddSession(self):

        self.root.destroy()

        addSession = Tk()
        addSessionMenu = AddSession(addSession)
        addSession.mainloop()

    def goToBooking(self):

        self.root.destroy()
        booking = Tk()
        bookingMenu = BookingMenu(booking)
        booking.mainloop()
        
                
def RunGUI():

    root = Tk()
    homePage = HomePage(root)
    root.mainloop()
    con.close()

RunGUI()

            
