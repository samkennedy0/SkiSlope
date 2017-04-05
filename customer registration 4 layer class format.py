import sqlite3 as lite
from tkinter import *
import tkinter.ttk as ttk
import unittest
import os


class customerTesting(unittest.TestCase):
   def __init__(self):
      addTest = self.addCustomerTest()
      if addTest:
         print("Add Customer Testing Passed")
      else:
         print("Add Customer Testing Failed")

   def addCustomerTest(self):
      global test_db
      test_db = True
      test_controller = CustomerController()

      test_controller.addCustomer("Bloggs", "Fred", 2, "Decent session")
      test_controller.addCustomer("Brown", "Frederick", 1, "Decent session")
      test_controller.addCustomer("qwert", "asdf", 3, "Decent session")
      test_controller.addCustomer("Name", "Other", 2, "Decent session")
      test_controller.addCustomer("Person", "FThis", 1, "Decent session")
      
      if test_controller.searchCustomer("Bloggs", "Fred", 2, 1)[0] != (2, "Bloggs", "Fred", 2, 1):
         os.remove('testDB.db')
         print("Test 1 Failure")
         return False

      if test_controller.searchCustomer("Brown", "Frederick", 1, 1)[0] != (3, "Brown", "Frederick", 1, 1):
         os.remove('testDB.db')
         print("Test 2 Failure")
         return False

      if test_controller.searchCustomer("qwert", "asdf", 3, 1)[0] != (4, "qwert", "asdf", 3, 1):
         os.remove('testDB.db')
         print("Test 3 Failure")
         return False

      if test_controller.searchCustomer("Name", "Other", 2, 1)[0] != (5, "Name", "Other", 2, 1):
         os.remove('testDb.db')
         print("Test 4 Failed")
         return False

      if test_controller.searchCustomer("Person", "FThis", 1, 1)[0] != (6, "Person", "FThis", 1, 1):
         os.remove('testDB.db')
         print("Test 5 Failed")
         return False

      os.remove('testDb.db')
      return True



class customerUserInterface:

   def __init__(self):
      global test_db
      test_db = False
      self.Firstname = ""
      self.Surname = ""
      self.MembershipId = 0
      self.SessionId = 0

      self.button_font = ("Arial", 12)

      self.addcustomer()
    
   def addcustomer(self):

      self.cur = lite.connect('register.db') # This is used to determine the section needed in the database
      self.con=self.cur.cursor() # This is used to add data to the selected section

      self.customeradd = Tk()
      self.customeradd.title("Add Customer")
      self.customeradd.geometry('500x500')

      lbl2=Label(self.customeradd, text="Surname?", font= self.button_font)
      lbl2.place(x=40, y=30, height=75, width=200)

      #These three lines create a textbox to enter the Surname
      self.txt1 = StringVar(self.customeradd)
      self.txt1=Entry(self.customeradd, font=self.button_font)
      self.txt1.place(x=270, y=55, height=50, width=200)

      #These two lines create a label to describe the second textbox
      lbl3=Label(self.customeradd, text="First name?", font=self.button_font)
      lbl3.place(x=40, y=105, height=75, width=200)

      self.txt2 = StringVar(self.customeradd)
      self.txt2=Entry(self.customeradd, font= self.button_font)
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

      itemlist=[]
      item=1
      for row in self.con.execute("SELECT * FROM Memberships"):
         item+=1
         itemlist.append(item-1)


      for i in range(1, item):
         self.con.execute("SELECT MembershipName FROM Memberships WHERE MembershipID=?", (i,))
         Name=self.con.fetchone()[0]
         self.con.execute("SELECT MembershipCost FROM Memberships WHERE MembershipID=?", (i,))
         cost=self.con.fetchone()[0]

         tree.insert("", i, text=i, values=(Name, cost))
     
      lbl4=Label(self.customeradd, text="Membership?", font=self.button_font)
      lbl4.place(x=40, y=280, height=75, width=200)

      self.combo2 = StringVar(self.customeradd)
      self.combo2 = ttk.Combobox(self.customeradd, font=self.button_font, state='normal', value=itemlist)
      self.combo2.place(x=270, y=290, height=50, width=200)
     
      lbl6=Label(self.customeradd, text="Select Session", font=self.button_font)
      lbl6.place(x=40, y=375, height=50, width=200)

      listsessionName=[]
      item=1
     
      for row in self.con.execute("SELECT * FROM Sessions"):
         item+=1
             
      for i in range(1, item):
         self.con.execute("SELECT SessionName FROM Sessions WHERE SessionID=?", (i,))
         name = self.con.fetchone()[0]
         listsessionName.append(name)

      self.combo = StringVar(self.customeradd)
      self.combo = ttk.Combobox(self.customeradd, font=self.button_font, state='normal', value=listsessionName)
      self.combo.place(x=270, y=375, height=50, width=200)
      
      btn1=Button(self.customeradd, justify=LEFT)
      btn1.place(bordermode=OUTSIDE, height=50, width=50)
     
      #These three lines create and place a silver confirm button, which leads to confirming the data
      btn2=Button(self.customeradd, text="Confirm", font=self.button_font, background="Silver", foreground="Red", command=self.confirm)
      btn2.place(x=200, y=450, height=50, width=100)

   def confirm(self):

      self.cur = lite.connect('register.db') # This is used to determine the section needed in the database
      self.con=self.cur.cursor() # This is used to add data to the selected section
      
      self.Surname=self.txt1.get() #Retrieves the first textbox value
      self.Firstname=self.txt2.get() #retrieves the second textbox vallue
      self.MembershipId=self.combo2.get() #Retrieves the third textbox value
      self.SessionId=self.combo.get()

      customer_controller = CustomerController()
      customer_controller.addCustomer(self.Surname, self.Firstname, self.MembershipId, self.SessionId)

      messagebox.showinfo(self.customeradd, "Customer added")

class CustomerController:
   def __init__(self):
      pass
   
   def addCustomer(self, Surname, Firstname, MembershipId, SessionId):
      customer_factory = CustomerFactory(Surname, Firstname, MembershipId, SessionId)
      return customer_factory.getCustomer()

   def searchCustomer(self, Surname, Firstname, MembershipId, SessionId):
      customer_impl = CustomerImpl(self)
      return customer_impl.searchCustomers(Surname, Firstname, MembershipId, SessionId).fetchall()


class CustomerFactory:
   def __init__(self, Surname, Firstname, MembershipId, SessionId):
      self.customers = self.getNormalCustomer(Surname, Firstname, MembershipId, SessionId)
      self.customers.saveData()

   def getCustomer(self):
      return self.customers

   def getNormalCustomer(self, Surname, Firstname, MembershipId, SessionId):
      return NormalCustomer(Surname, Firstname, MembershipId, SessionId)

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

class NormalCustomer(Customer):
   def saveData(self):
      customerImplement = CustomerImpl([self])
      customerImplement.WriteAll()

class CustomerImpl:
   def __init__(self, customers):
      self.customers = customers

      global test_db
      db_exists = False
      self.db_name = 'register.db'
      if test_db:
         self.db_name = 'testDB.db'
      if os.path.isfile(self.db_name):
         db_exists = True

      self.cur = lite.connect(self.db_name) 
      self.con=self.cur.cursor() 

      if not db_exists:
         self.con.execute("CREATE TABLE Customers(CustomerID INTEGER PRIMARY KEY AUTOINCREMENT, Surname TEXT NOT NULL, FirstName TEST NOT NULL, MembershipID INTEGER NOT NULL, SessionID INTEGER NOT NULL)")
         self.con.execute("CREATE TABLE Memberships(MenbershipID INTEGER PRIMARY KEY AUTOINCREMENT, MemebrshipName TEXT NOT NULL, MembershipCost BLOB NOT NULL)")
         self.con.execute("CREATE TABLE Sessions(SessionID INTEGER PRIMARY KEY AUTOINCREMENT, SessionName TEXT NOT NULL)")

         self.con.execute("INSERT INTO Customers VALUES (1, 'a', 'b', 4, 2)")
         self.con.execute("INSERT INTO Memberships VALUES(1, 'Basic', 3.50)")
         self.con.execute("INSERT INTO Sessions VALUES (1, 'Decent session')")

         self.cur.commit()

   def WriteAll(self):
      for customer in self.customers:
         self.WriteCustomer(customer.Surname, customer.Firstname, customer.MembershipId, customer.SessionId)

   def WriteCustomer(self, Surname, Firstname, MembershipId, SessionId):

      self.cur = lite.connect(self.db_name) 
      self.con=self.cur.cursor()
      
      item=1
      for row in self.con.execute("SELECT * FROM Customers"):
         item+=1        
      Id=item

      self.con.execute("SELECT SessionID FROM Sessions WHERE SessionName =?", (SessionId,))
      sesh = self.con.fetchone()[0]
      
      new = [Id, Surname, Firstname, MembershipId, sesh]
      self.con.execute("INSERT INTO Customers VALUES(?,?,?,?,?)" ,new)
      self.cur.commit()

   def searchCustomers(self, Surname, Firstname, MembershipId, SessionId):

      self.cur = lite.connect(self.db_name) 
      self.con=self.cur.cursor()
      
      self.con.execute("SELECT CustomerID FROM Customers WHERE Surname=? AND FirstName=? AND MembershipID=? AND SessionID=?", (Surname, Firstname, MembershipId, SessionId,))
      Id = self.con.fetchone()[0]
      
      return self.con.execute("SELECT * FROM Customers WHERE CustomerID=? AND Surname=? AND FirstName=? AND MembershipID=? AND SessionID=?", (Id, Surname, Firstname, MembershipId, SessionId))

if __name__ == "__main__":
   test = customerTesting()
   main_win = customerUserInterface()
else:
   test = customerTesting()
   debug_win = customerUserInterface()
