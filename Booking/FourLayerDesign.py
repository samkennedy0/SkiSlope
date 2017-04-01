#connecting to database
import sqlite3 as sql
con = sql.connect('skiSlopeDatabase.db') #connecting to sql
cur = con.cursor() 
from tkinter import *
#importing tree
import tkinter.ttk as ttk

class BookingUI(): #user interface layer
  def __init__(self,root):
    self.root = root
    #adding title
    root.title("Booking")
    #setting up frames so that I can pack my button etc into them later
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
    
    self.fNameLabel = Label(self.frame1,text='Firstname: ') #assigning the text that will appear on the label 
    self.fNameLabel.pack(side=LEFT) #packing it into the the first frame

    self.fNameEntry = Entry(self.frame1)#creating entry box
    self.fNameEntry.pack(side=RIGHT)#packing entry box into first frame

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

    self.searchCustomerButton = Button(self.frame3,text='Search ID',command=self.GetID) #creating a button called search ID and assigning it a command getCustomerID
    self.searchCustomerButton.pack(side=RIGHT)#packing button into frame

    #primary key entry box (sessionID)

    #customer id entry box

    self.sessionIdLabel = Label(self.frame5,text='Session ID: ')
    self.sessionIdLabel.pack(side=LEFT)

    self.sessionIdEntry = Entry(self.frame5)
    self.sessionIdEntry.pack(side=RIGHT)

    #tree to display sessions, a tree view is a tbale which displays data like a database table 

    self.sessionsTree = ttk.Treeview(self.frame6)
    self.sessionsTree["columns"] = ("two","three","four") #setting up tree coloumns

    self.sessionsTree.column("#0",width=100) #setting up the width of each column 
    self.sessionsTree.column("two",width=100)
    self.sessionsTree.column("three",width=100)
    self.sessionsTree.column("four",width=150)


    self.sessionsTree.heading("#0", text="SessionID") #assigning column headings 
    self.sessionsTree.heading("two", text="Session Date")
    self.sessionsTree.heading("three", text="Session Time")
    self.sessionsTree.heading("four", text="Session Type")
    

    self.sessionsTree.pack() #pacing tree in frame

    self.attributeList = []#list of attributes that will go into tree
    self.attribute = 1

    for row in cur.execute("""SELECT * FROM sessions"""):#select all atributes from the sessions table
      self.attribute += 1
      self.attributeList.append(self.attribute - 1)

    for i in range(1,self.attribute):

      cur.execute("""SELECT session_Date FROM sessions WHERE sessionID=?""", (i,))
      self.date = cur.fetchall()#fetching all session dates from database

      cur.execute("""SELECT session_Time FROM sessions WHERE sessionID=?""", (i,))
      self.time = cur.fetchall()#fecthing all session times from database

      cur.execute("""SELECT session_type FROM sessions WHERE sessionID=?""", (i,))
      self.type = cur.fetchall()#fetching all session types from database

      self.sessionsTree.insert("",i,text=i, values=(self.date,self.time,self.type))#inserting all the attributes into a tree



    #pre paid checkbox
    self.prePaid = IntVar()
    self.prePaidCheck = Checkbutton(self.frame7, text="Pre-Paid", variable=self.prePaid)#setting up checkbox
    self.prePaidCheck.pack(side=RIGHT)
      

    #enter button

    self.enterButton = Button(self.frame7,text='Enter',command=self.InsertIntoDb)#enter button that adds all the input data to the database
    self.enterButton.pack(side=RIGHT)
    
    #Go back button
    self.backButton = Button(self.frame7,text='Go Back')#go back button that will return to home back when combined with other functionalities 
    self.backButton.pack(side=LEFT)

  
  def InsertIntoDb(self):
     return(BookingPersistance.insertValues(self))

  def GetID(self):
      return(BookingPersistance.getCustomerID(self))
  
class BookingController: #controller class
  def __init__(self):

    root = Tk()
    bookingUI = BookingUI(root)
    root.mainloop()

class BookingEntity():
    def __init__(self):
        self.customerId = None
        self.customerFirstName = None
        self.customerSurname = None
        self.sessionId = None
        self.bookingRef = None
        self.prePaid = None 

    #get fucntions to get the values needed by the persistence layer
    def getCustomerId(BookingUI):
      customerId = str(BookingUI.customerIdEntry.get())
      return(customerId)
    def getCustomerFirstname(BookingUI):
      customerFirstname = str(BookingUI.fNameEntry.get())
      return(customerFirstname)
    def getCustomerSurname(BookingUI):
      customerSurname = str(BookingUI.sNameEntry.get())
      return(customerSurname)
    def getSessionId(BookingUI):
      sessionId = str(BookingUI.sessionIdEntry.get())
      return(sessionId)
    def getBookingRef():
      cur.execute("""SELECT COUNT (DISTINCT booking_ref) FROM BookingList;""") #counting number of bookings to generate a booking ref
      bookRef = int(cur.fetchone()[0])+1 #working out the booking ref (take total number of bookings and add one
      return(bookRef)
    def getPrePaid(BookingUI):
      prePaid =int(BookingUI.prePaid.get())#get int of check box, 1 = true and 0 = false
      return(prePaid)
    
class BookingPersistance():
  def __init__(self):
    self.bookingDetails = None
  def insertValues(BookingUI):
    bookingDetails = [] #list of values to insert into bookings table
    #appending values to list
    bookingDetails.append(BookingEntity.getSessionId(BookingUI))
    bookingDetails.append(BookingEntity.getCustomerId(BookingUI))
    bookingDetails.append(BookingEntity.getCustomerFirstname(BookingUI))
    bookingDetails.append(BookingEntity.getCustomerSurname(BookingUI))
    bookingDetails.append(BookingEntity.getBookingRef())
    bookingDetails.append(BookingEntity.getPrePaid(BookingUI))
  

    #getting customer name for cutomerID test

    customerName = [BookingEntity.getCustomerFirstname(BookingUI),BookingEntity.getCustomerSurname(BookingUI)] #putting values into a list so it can be used in an sql query

    cur.execute('''SELECT sessionID FROM sessions WHERE sessionID = ?;''',BookingEntity.getSessionId(BookingUI))#select session id where the sessionID is equal to the one inputted

    try:
        sessionIDTest = str(cur.fetchone()[0])#fecth session id
        cur.execute('''SELECT * FROM customers WHERE customer_Firstname = ? AND customer_Surname = ? ;''',customerName)
        customerID = str(cur.fetchone()[0])#fetch customer id
        if BookingEntity.getCustomerId(BookingUI) != customerID: #test to see if customer id inputted match one in database

            window = Toplevel()
            Label(window,text = 'Error\n CustomerID does not match the customerID in the database').pack()
            Button(window,text='OK',command=window.destroy).pack()
            
        else:
            cur.execute('''INSERT INTO BookingList (sessionID,customerID,customer_Firstname,customer_Surname,booking_ref,prePaid) VALUES (?,?,?,?,?,?);''', bookingDetails) #inserting data into database
            #opening new window
            window = Toplevel()
            Label(window,text = 'Success! \n sucessfully booked customer into session\n Your booking refernce is : ' + str(BookingEntity.getBookingRef())).pack()
            Button(window,text='OK',command=window.destroy).pack()
            
            con.commit()
            con.close()

    except TypeError: #if the fetchone value is a NoneType run error window message

        window = Toplevel()
        Label(window,text = ("Error \n SessionID doesn't exist")).pack()
        Button(window,text='OK',command=window.destroy).pack()

            
  def getCustomerID(BookingUI):
   
    #get customer firstname and surname
    firstname = str(BookingEntity.getCustomerFirstname(BookingUI))
    surname = str(BookingEntity.getCustomerSurname(BookingUI))
    
    customerName = [firstname,surname]
   
    
    cur.execute('''SELECT * FROM customers WHERE customer_Firstname = ? AND customer_Surname = ? ;''',customerName)#select all attributes where customer name is equal to the one entered
    try:
      customerID = str(cur.fetchone()[0])
      window = Toplevel()#create a new window
      Label(window,text = (firstname + " " + surname + " Customer ID: " + customerID)).pack()#label that displays customer's name and id
      Button(window,text='OK',command=window.destroy).pack()
    
    except TypeError: #if the fetchone value is a NoneType run error window message, meaning customer isnt in database
      window = Toplevel()
      Label(window,text = (firstname + " " + surname + "\n" + "This Customer is not in the database\n Please register the customer to book a session")).pack()
      Button(window,text='OK',command=window.destroy).pack()
      



   

        
BookingController()
        
    






