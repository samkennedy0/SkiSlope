#imports for the program. SQLite3 is the database, tkinter imports the interface details, and ttk imports the tree and comboboxes as well.
#unittest is used to test the code
#os is used to check for the database insie the file location. This isn't necessarily needed, as i could have sued the main database for testing.
import sqlite3 as lite
from tkinter import *
import tkinter.ttk as ttk
import unittest
import os


#This is used for starting the tests. There are 5 tests to confirm the program works as it should with the test data.
#The test works by adding  5 different test cases into the test database. If the program can find all 5 tests, the testing is successful and the program continues
class customerTesting(unittest.TestCase):
   def __init__(self):
      #addTest is used to test the program, if one test fails then addTest is considered a failure, otherwise its considered a success
      addTest = self.addCustomerTest()
      if addTest:
         print("Add Customer Testing Passed")
      else:
         print("Add Customer Testing Failed")

   #this function starts the test process
   def addCustomerTest(self):
      #The use of a global testBoolean is to alert every class that the data being passed is or isnt test data. This comes up later on in the program.
      global testBoolean
      testBoolean = True

      #Easily adds all the tests into the customer controller, without having to state customer controller every time
      #It also allows the data to be added to a function inside the CustomerController class
      testCont = CustomerController()

      #Starts the process to add data to the test database
      testCont.addCustomer("Bloggs", "Fred", 2, "Decent session")
      testCont.addCustomer("Brown", "Frederick", 1, "Decent session")
      testCont.addCustomer("qwert", "asdf", 3, "Decent session")
      testCont.addCustomer("Name", "Other", 2, "Decent session")
      testCont.addCustomer("Person", "FThis", 1, "Decent session")

      #These details search through the test database to find the data, and then if the data is not the same as what it should be, the test database is deleted and that the relevant tests are failed.
      if testCont.searchCustomer("Bloggs", "Fred", 2, 1)[0] != (2, "Bloggs", "Fred", 2, 1):
         os.remove('test.db')
         print("Test 1 Failed")
         return False

      if testCont.searchCustomer("Brown", "Frederick", 1, 1)[0] != (3, "Brown", "Frederick", 1, 1):
         os.remove('test.db')
         print("Test 2 Failed")
         return False

      if testCont.searchCustomer("qwert", "asdf", 3, 1)[0] != (4, "qwert", "asdf", 3, 1):
         os.remove('test.db')
         print("Test 3 Failed")
         return False

      if testCont.searchCustomer("Name", "Other", 2, 1)[0] != (5, "Name", "Other", 2, 1):
         os.remove('test.db')
         print("Test 4 Failed")
         return False

      if testCont.searchCustomer("Person", "FThis", 1, 1)[0] != (6, "Person", "FThis", 1, 1):
         os.remove('test.db')
         print("Test 5 Failed")
         return False

      #removes the test database at the end of the tests, and states that all tests are passed
      os.remove('test.db')
      return True

#the class that covers all of the UI for the program. I have a minimal amount of SQL in this section just to grab data for the tree view and comboboxes.
#This class also calls the next class in the system (CustomerController) when details are selected
class customerUserInterface:

   def __init__(self):
      global testBoolean
      testBoolean = False

      #Initial setting of variables in this class.
      self.Firstname = ""
      self.Surname = ""
      self.MembershipId = 0
      self.SessionId = 0

      #Sets the main font throughout the program interface, limiting the amount of repetition
      self.mainFont = ("Arial", 12)

      #calls the UI function
      self.addcustomer()


   #the main function for the UI
   def addcustomer(self):

      self.cur = lite.connect('register.db') # This is used to determine the section needed in the database
      self.con=self.cur.cursor() # This is used to add data to the selected section

      #Sets the tkinter window type, title and size
      self.customeradd = Tk()
      self.customeradd.title("Add Customer")
      self.customeradd.geometry('500x500')

      #A label to state which field is entered into the textbox (Surname)
      lbl2=Label(self.customeradd, text="Surname?", font= self.mainFont)
      lbl2.place(x=40, y=30, height=75, width=200)

      #These three lines create a textbox to enter the Surname
      self.txt1 = StringVar(self.customeradd)
      self.txt1=Entry(self.customeradd, font=self.mainFont)
      self.txt1.place(x=270, y=55, height=50, width=200)

      #These two lines create a label to describe the second textbox
      lbl3=Label(self.customeradd, text="First name?", font=self.mainFont)
      lbl3.place(x=40, y=105, height=75, width=200)

      #Creates a text box for entering the Firstname
      self.txt2 = StringVar(self.customeradd)
      self.txt2=Entry(self.customeradd, font= self.mainFont)
      self.txt2.place(x=270, y=120, height=50, width=200)

      tree=ttk.Treeview(self.customeradd) #States that the tree is a Treeview type to be used in this window
      tree["columns"]=("two","three") #Creates the columns for the tree

      #Each column has to specify its size and the heding of the column
      tree.column("two", width=90)
      tree.column("three", width=90)
      tree.column("#0", width=90)
      tree.heading("#0", text="MembershipID")
      tree.heading("two", text="Membership")
      tree.heading("three",text="Cost")
      tree.place(x=60, y=180, height=100, width=360) # Determines the overall size of the tree and where it will be placed

      #Adds the ID's for the treeview by accessing the rows in the table Memberships. For each row, 1 is added to the counter (item) and the previous value is stored in an array.
      #This array contains all the ID's for each row in order.
      itemlist=[]
      item=1
      for row in self.con.execute("SELECT * FROM Memberships"):
         item+=1
         itemlist.append(item-1)

      #By using the ID's just created, this grabs the data from the tabke Memberships and stores it in the relevant variables, to be inserted into the treeview
      for i in range(1, item):
         self.con.execute("SELECT MembershipName FROM Memberships WHERE MembershipID=?", (i,))
         Name=self.con.fetchone()[0]
         self.con.execute("SELECT MembershipCost FROM Memberships WHERE MembershipID=?", (i,))
         cost=self.con.fetchone()[0]
         tree.insert("", i, text=i, values=(Name, cost))

      #Creates a label for deciding on which Membership to choose
      lbl4=Label(self.customeradd, text="Membership?", font=self.mainFont)
      lbl4.place(x=40, y=280, height=75, width=200)

      #Creates a combobox to easily showe all Membership ID's and decdie which one you need
      self.combo2 = StringVar(self.customeradd)
      self.combo2 = ttk.Combobox(self.customeradd, font=self.mainFont, state='normal', value=itemlist)
      self.combo2.place(x=270, y=290, height=50, width=200)

      #Creates a label for deciding on which session to choose
      lbl6=Label(self.customeradd, text="Select Session", font=self.mainFont)
      lbl6.place(x=40, y=375, height=50, width=200)

      #In a similar way to the treeview, this creates a list of ID's to be used to get the data from sessions.
      #However, as the data doesn't have to be inserted into the combobox in the same way, it can just be one list of data to be edited later on.
      listsessionName=[]
      item=1
     
      for row in self.con.execute("SELECT * FROM Sessions"):
         item+=1
             
      for i in range(1, item):
         self.con.execute("SELECT SessionName FROM Sessions WHERE SessionID=?", (i,))
         name = self.con.fetchone()[0]
         listsessionName.append(name)

      #this creates the combobox for choosing sessions, in the same way as before but using text instead of numbers
      self.combo = StringVar(self.customeradd)
      self.combo = ttk.Combobox(self.customeradd, font=self.mainFont, state='normal', value=listsessionName)
      self.combo.place(x=270, y=375, height=50, width=200)

      #Creates a button to be used for returning to the previous section. This is only used when combining my code with the rest of my groups code.
      btn1=Button(self.customeradd, justify=LEFT, text="Back", font=self.mainFont)
      btn1.place(bordermode=OUTSIDE, height=50, width=50)
     
      #These three lines create and place a silver confirm button, which leads to confirming the data
      btn2=Button(self.customeradd, text="Confirm", font=self.mainFont, background="Silver", foreground="Red", command=self.confirm)
      btn2.place(x=200, y=450, height=50, width=100)

   #A function to confrim the data that has been entered, and then call the second class, the CustomerControlelr
   def confirm(self):

      self.cur = lite.connect('register.db') # This is used to determine the section needed in the database
      self.con=self.cur.cursor() # This is used to add data to the selected section

      #Sets the variables to their required data
      self.Surname=self.txt1.get() #Retrieves the first textbox value
      self.Firstname=self.txt2.get() #retrieves the second textbox vallue
      self.MembershipId=self.combo2.get() #Retrieves the third textbox value
      self.SessionId=self.combo.get()

      #calls the next class witht he relevant variables
      customer_controller = CustomerController()
      customer_controller.addCustomer(self.Surname, self.Firstname, self.MembershipId, self.SessionId)

      #once all the other processes are completed, this messagebox appears to confirm that the data has been added
      messagebox.showinfo(self.customeradd, "Customer added")

#This class is used as a gateway between the user interface data and the sql database commands. It sends the data to the relevant factory to then be sent to the main class
#This class has two different operations. One for the main processes, and one (searchCustomer) specifically for the testing of the program
class CustomerController:
   def __init__(self):
      pass

   #adda the relevant passed data into the customer factory. With more details included in the data, these factories can be more specific, however as the program is, all data is in one factory
   def addCustomer(self, Surname, Firstname, MembershipId, SessionId):
      customerFactory = CustomerFactory(Surname, Firstname, MembershipId, SessionId)
      return customerFactory.getCustomer()

   #this calls the search function, which does not use the CustomerFactory class (as its not creating data but searchming through existing data)
   def searchCustomer(self, Surname, Firstname, MembershipId, SessionId):
      implementCustomer = CustomerImplement(self)
      return implementCustomer.searchCustomers(Surname, Firstname, MembershipId, SessionId).fetchall()

#This class is used to sort out what kind of customer will be added to the database. From there, the data is transferred to the specific factory clas (in this case, Normal Customer).
#As the program isnow, the extra class is a bit excessive. However as the program improves, this will be how i implement different kinds of customer into the database in the future
class CustomerFactory:
   def __init__(self, Surname, Firstname, MembershipId, SessionId):
      self.customers = self.getNormalCustomer(Surname, Firstname, MembershipId, SessionId)
      self.customers.saveData()

   #used to return the custoemr data
   def getCustomer(self):
      return self.customers

   #Used to return 
   def getNormalCustomer(self, Surname, Firstname, MembershipId, SessionId):
      return NormalCustomer(Surname, Firstname, MembershipId, SessionId)

#class to organise the variables to make them ready for the database. This includes setting the variables and hecking that they are real types
class Customer:
   def __init__(self, Surname, Firstname, MembershipId, SessionId):
      self.Surname = Surname
      self.Firstname = Firstname
      self.MembershipId = MembershipId
      self.SessionId = SessionId

   def getSurname(self):
      return self.Surname
   def setSurname(self, Surname):
      self.Surname = Surname

   def getFirstname(self):
      return self.Firstname
   def setFirstname(self, Firstname):
      self.Firstname = Firstname

   def getMembershipId(self):
      return self.MembershipId
   def setMembershipId(self, MembershipId):
      self.MembershipId = MembershipId

   def getSessionId(self):
      return self.SessionId
   def setSessionId(self, SessionId):
      self.SessionId = SessionId

#This class is used to determine what kind of customer is being implemente d(in this case the only type of customer, a normal customr), and then carry out the CustomerImplement class function to add the customer
class NormalCustomer(Customer):
   #Used to enter all the data into the database when called, this is in case multiple users are being added at once. 
   def saveData(self):
      CustomerImplementement = CustomerImplement([self])
      CustomerImplementement.InsertAll()

#This class is used to both add data to the database and find the searched for data. It directly relates to the SQLite database.
class CustomerImplement:
   
   def __init__(self, customers):
      self.customers = customers

      #This is when the test boolean becomes important. If the program is a test, and it is not using the relaDatabase, then a new test database is created.
      #Otherwise the normal database is used
      global testBoolean
      realDatabase = False
      self.databaseName = 'register.db'
      if testBoolean:
         self.databaseName = 'test.db'
      if os.path.isfile(self.databaseName):
         realDatabase = True

      self.cur = lite.connect(self.databaseName) 
      self.con=self.cur.cursor() 

      #This creates the test database (if the test are carried out), and inserts test data into the program just as a basis for the database. All changes are saved to the temporary database
      if not realDatabase:
         self.con.execute("CREATE TABLE Customers(CustomerID INTEGER PRIMARY KEY AUTOINCREMENT, Surname TEXT NOT NULL, FirstName TEST NOT NULL, MembershipID INTEGER NOT NULL, SessionID INTEGER NOT NULL)")
         self.con.execute("CREATE TABLE Memberships(MenbershipID INTEGER PRIMARY KEY AUTOINCREMENT, MemebrshipName TEXT NOT NULL, MembershipCost BLOB NOT NULL)")
         self.con.execute("CREATE TABLE Sessions(SessionID INTEGER PRIMARY KEY AUTOINCREMENT, SessionName TEXT NOT NULL)")

         self.con.execute("INSERT INTO Customers VALUES (1, 'a', 'b', 4, 2)")
         self.con.execute("INSERT INTO Memberships VALUES(1, 'Basic', 3.50)")
         self.con.execute("INSERT INTO Sessions VALUES (1, 'Decent session')")

         self.cur.commit()
         
   #Adds all the data to the relevant database. This could easily be doen without stating it as adding all th data, as i only enter one user at a time. However, when the program expands, this wil make adding multiple users at once easier.
   def InsertAll(self):
      for customer in self.customers:
         self.InsertCustomer(customer.Surname, customer.Firstname, customer.MembershipId, customer.SessionId)

   #This function is used to enter the customers into the databae. it goes per customer, so is called by the InsertAll function for each customer in self.customers.
   def InsertCustomer(self, Surname, Firstname, MembershipId, SessionId):

      self.cur = lite.connect(self.databaseName) 
      self.con=self.cur.cursor()

      #Ths calculates how many customers are already registered, making sure that the new customer will be next in the database according to the primary key
      #as my program does not need a delete statement, there was no worry to repeating id's due to deleting a member in the middle of the database.
      item=1
      for row in self.con.execute("SELECT * FROM Customers"):
         item+=1        
      Id=item

      #this selects the id for the relevant selected session. The id is a foreign key in the customer table.
      self.con.execute("SELECT SessionID FROM Sessions WHERE SessionName =?", (SessionId,))
      sesh = self.con.fetchone()[0]

      #the data is entered into a list to make it easy to enter into the database. once this is done, all changes are saved and the program returns back through the classes to the ui.
      new = [Id, Surname, Firstname, MembershipId, sesh]
      self.con.execute("INSERT INTO Customers VALUES(?,?,?,?,?)" ,new)
      self.cur.commit()

   #This is used for searching the customer database for data. it is only used in this case for the testing.
   #The data is entered into the database in order to find the relevant primary key, then the program searched the database for any data that matches all of the given data.
   #The resukt is returned to compare to the test data.
   def searchCustomers(self, Surname, Firstname, MembershipId, SessionId):

      self.cur = lite.connect(self.databaseName) 
      self.con=self.cur.cursor()

      #Finds the id for the releveant data entered by the test
      self.con.execute("SELECT CustomerID FROM Customers WHERE Surname=? AND FirstName=? AND MembershipID=? AND SessionID=?", (Surname, Firstname, MembershipId, SessionId,))
      Id = self.con.fetchone()[0]

      #Searches for the relevantd ata matching all the given data. returns whatever it finds back to the test cases to compare to the expected outcome
      return self.con.execute("SELECT * FROM Customers WHERE CustomerID=? AND Surname=? AND FirstName=? AND MembershipID=? AND SessionID=?", (Id, Surname, Firstname, MembershipId, SessionId))

#starts the program by calling the test class, then once tht is completed, calls the ui class to create the interface
if __name__ == "__main__":
   test = customerTesting()
   main = customerUserInterface()

#If there is a problem starting the code, the test is run, folowed by a debugging process that will be implemented, to test for why there would be a problem.
else:
   test = customerTesting()
   debug = customerUserInterface()
