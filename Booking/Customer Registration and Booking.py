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
            Button(window,text='Cancel',command=window.destroy).pack()
            Button(window,text='REgister',command=customeradd).pack()

    def goBackHome(self):

        self.root.destroy()
        home = Tk()
        homePage = HomePage(home)
        home.mainloop()
        

def customeradd():
        customeradd=Tk() #Sets the name of the window
        customeradd.title("Add a customer") #Sets the window heading
        customeradd.geometry("500x500") #Sets the window size

        #These two lines create a label to describe the first textbox
        lbl2=Label(customeradd, text="Surname?", font=("Arial", 12))
        lbl2.place(x=40, y=30, height=75, width=200)

        #These two lines create a textbox to enter the Surname
        txt1=Entry(customeradd, font=("Arial", 12))
        txt1.place(x=270, y=55, height=50, width=200)

        #These two lines create a label to describe the second textbox
        lbl3=Label(customeradd, text="First name?", font=("Arial", 12))
        lbl3.place(x=40, y=105, height=75, width=200)

        txt2=Entry(customeradd, font=("Arial", 12))
        txt2.place(x=270, y=120, height=50, width=200)

        tree=ttk.Treeview(customeradd) #States that the tree is a Treeview type to be used in this window
        tree["columns"]=("two","three") #Creates the columns for the tree

        #Each column has to specify its size and the heding of the column
        tree.column("two", width=90)
        tree.column("three", width=90)
        tree.column("#0", width=90)
        tree.heading("#0", text="MembershipID")
        tree.heading("two", text="Membership")
        tree.heading("three",text="Cost")
        tree.place(x=60, y=180, height=100, width=360) # Determines the overall size of the tree and where it will be placed

        itemlist=[]
        item=1
        for row in cur.execute("SELECT * FROM Memberships"):
                item+=1
                itemlist.append(item-1)


        for i in range(1, item):
                cur.execute("SELECT MembershipName FROM Memberships WHERE MembershipID=?", (i,))
                Name=cur.fetchone()[0]
                cur.execute("SELECT MembershipCost FROM Memberships WHERE MembershipID=?", (i,))
                cost=cur.fetchone()[0]

                tree.insert("", i, text=i, values=(Name, cost))
        
        lbl4=Label(customeradd, text="Membership?", font=("Arial", 12))
        lbl4.place(x=40, y=280, height=75, width=200)

        combo2 = ttk.Combobox(customeradd, font=("Arial", 12), state='normal', value=itemlist)
        combo2.place(x=270, y=290, height=50, width=200)
        
        def confirm():

                #A recursive process that finds the length of the entity, to be used as the latest id
                item=1
                for row in cur.execute("SELECT * FROM Customers"):
                        item+=1        
                Id=item 
                Surname=txt1.get() #Retrieves the first textbox value
                Firstname=txt2.get() #retrieves the second textbox vallue
                MembershipID=combo2.get() #Retrieves the third textbox value


                new=[Id, Surname, Firstname, MembershipID] #All the data retrieved is placed into a list to make it easier to enter
                cur.execute("INSERT INTO Customers VALUES(?,?,?,?)" ,new) #The list is entered into the database
                con.commit() # This saves the data from the previous SQLite code into the database
                messagebox.showinfo(customeradd, "Customer added") #Alerts the user that the data has been entered
                customeradd.destroy()

        def goBackHome():

            customeradd.destroy()
            home = Tk()
            homePage = HomePage(home)
            home.mainloop()

        #The code for the back button is the same as last time, except the button leads to the previous window
        # insted of logging out of the program
        btn1=Button(customeradd, justify=LEFT,command=goBackHome)
        btn1.place(bordermode=OUTSIDE, height=50, width=50)
        
        #These three lines create and place a silver confirm button, which leads to confirming the data
        btn2=Button(customeradd, text="Confirm", font=("Arial", 12), background="Silver", foreground="Red", command=confirm)
        btn2.place(x=200, y=450, height=50, width=100)


class HomePage:
    def __init__(self,root):
        self.root = root
        self.root.title("Ski Slope Booking System")
        self.root.geometry("205x150")

        self.addSessionButton = Button(self.root, text="Add Custromer",command=self.goToAddCustomer).grid(row=3,column=0)

        self.BookingButton = Button(self.root, text="Add Booking",command=self.goToBooking).grid(row=3,column=1)


    def goToAddCustomer(self):

        self.root.destroy()
        customeradd()

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

            
