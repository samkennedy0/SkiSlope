#connecting to database
import sqlite3 as sql
con = sql.connect('skiSlopeDatabase.db') #connecting to sql
cur = con.cursor() 
from tkinter import *
#importing tree
import tkinter.ttk as ttk

#Creating classes for each of my entities

class Session: #creating session class

    def __init__(self,sessionID,sessionDate,sessionTime,sessionType): #setting up attributes of session class

        self.sessionID = sessionID
        self.sessionDate = sessionDate
        self.sessionTime = sessionTime
        self.sessionType = sessionType

    #get and set methods for each attribute

    def getSessionID(self):
        print(self.sessionID)
    def getSessionDate(self):
        print(self.sessionDate)
    def getSessionTime(self):
        print(self.sessionTime)
    def getSessionType(self):
        print(self.sessionType)

    def setSessionID(self,sessionID):
        self.sessionID = sessionID
    def setSessionDate(self,sessionDate):
        self.sessionID = sessionDate
    def setSessionTime(self,sessionTime):
        self.sessionID = sessionTime
    def setSessionType(self,sessionType):
        self.sessionID = sessionType

class Customer:
    def __init__(self,customerID,firstname,surname,membership):#setting up attributes of customer class

        self.firstname = firstname
        self.surname = surname
        self.membership = membership
        self.sessionsBooked = [] #sessions booked is a ArrayList so im assigning it to an empty list

    #defining set and get methods for the attributes 
    def getCustomerID(self):
        print(self.customerID)
    def getFirstname(self):
        print(self.firstname)
    def getSurname(self):
        print(self.surname)
    def getMembership(self):
        print(self.membership)
    def getSessionsBooked(self):
        print(self.sessionsBooked)

    def setCustomerID(self,customerID):
        self.customerID = customerID
    def setFirstname(self,firstname):
        self.firstname = firstname
    def setSurname(self,surname):
        self.surname = surname
    def setMembership(self,membership):
        self.membership = membership
    def setSessionsBooked(self,session):
        self.sessionsBooked.append(session)

class skiInstructor:
    def __init__(self,staffID,name):

        self.staffID = staffID
        self.name = name
        self.sessionList = [] #sessions list is a ArrayList so im assigning it to an empty list

    
    def getStaffID(self):
        print(self.staffID)
    def getName(self):
        print(self.name)
    def getSessionList(self):
        print(self.sessionList)

    def setStaffID(self,staffID):
        self.staffID = staffID
    def getName(self,name):
        self.name = name
    def getSessionList(self,session):
        self.sessionList.append(session)
        
        

class Booking(Session,Customer):
    def __init__(self):
        Session.__init__(sessionID,sessionDate,sessionTime,sessionType) #take attributes from the session and customer class
        Customer.__init__(customerID,firstname,surname,membership)

    def getSession(self):
        pass
    def setSession(self,session):
        pass
    def getCustomer(self,customer):
        pass
    def setCustomer(self):
        pass

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
        
            

        
            
        
    




root = Tk()
gui = BookingMenu(root)
root.mainloop()
    

