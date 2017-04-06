from tkinter import *
import sqlite3
import unittest
import os
conn = sqlite3.connect("skiSlopeDatabase.db")
cur = conn.cursor()
#Sets up database connection and settings




class Interface:  #UI Layer / Interface Class
  def __init__(self, master):
                 
    master.title("Session Prototype")
    master.resizable(width=False, height=False)

    

    #Frames to hold the gui objects. 
    self.master = master
    topFrame = Frame(master)
    topFrame.pack()
    middleFrame = Frame(master)
    middleFrame.pack()
    bottomFrame = Frame(master)
    bottomFrame.pack()

    #Labels of the interface
    self.idlabel = Label(topFrame, text="Session ID",padx=10)
    self.firlabel = Label(middleFrame, text="Enter Firstname")
    self.surlabel = Label(bottomFrame, text="Enter Surname")

    #Buttons of the interfaece
    self.remove = Button(master, text="Remove customer", command=self.removeCustomer)
    self.close = Button(master, text="Close Window", command=self.close)
    self.search = Button(topFrame, text="Search", command=self.find)
    self.clear = Button(master, text="Clear", command=self.clear)

    #Entry froms of the interface
    self.idEntry = Entry(topFrame, bd=5)
    self.firstnameEntry = Entry(middleFrame, bd=5)
    self.surnameEntry = Entry(bottomFrame, bd=5)

    #Text box where data from database querys are displayed 
    self.txt = Text(master, height =10, width = 80)

    #How labels are packed
    self.idlabel.pack(side=LEFT)
    self.firlabel.pack(side=LEFT)
    self.surlabel.pack(side=LEFT)

    #How buttons are packed
    self.remove.pack(side=TOP)
    self.close.pack(side=BOTTOM)
    self.search.pack(side=RIGHT,padx=10)
    self.clear.pack(side=BOTTOM)
    
    #How entry and text boxes are packed
    self.idEntry.pack(side=LEFT)
    self.firstnameEntry.pack(side=LEFT)
    self.surnameEntry.pack(side=LEFT)
    self.txt.pack(side=TOP)

    #SQL statement to display Session details
    #Allows client to see what sessions are availabe 
    cur.execute("""SELECT MAX(sessionID) FROM sessions""")    
    maxID = cur.fetchone()
    maxSession = maxID[0]
    for i in range(maxSession):
      cur.execute("""SELECT * FROM sessions
                  WHERE sessionID = %s """ % (i))     #adds session table contetns
      conn.commit()
      self.txt.insert(END, "\n")                      #into text box within the page
      self.txt.insert(END, cur.fetchall())
     
      

  def removeCustomer(self):         
    return(Persistance.Remove(self))        #calls the remove function in the persistane layer
                
  def find(self):
    return(Persistance.Find(self))          #calls the find function in the persistance layer

  def close(self):
    self.master.destroy()                   #closes the window

  def clear(self):
    self.txt.delete(1.0, END)
    return(test.add())#clears the text box


    
class Controller:       #Controller class
  def __init__(self):   #Initiates the interface
    master = Tk()
    menu = Interface(master)
    master.mainloop()
    print("s")


class Entity():       
  def __init__(self):         #Declares varaibles 
    self.customerID = None
    self.customerForname = None
    self.customerSurname = None

    #get varibales used to pass data into persistance layer

  def getID(Interface):
      customerID = str(Interface.idEntry.get())       #gets data from entry boxs on interface layer
      return (customerID)                             
        
  def getForname(Interface):
      customerForname = str(Interface.firstnameEntry.get())
      return customerForname

  def getSurname(Interface):
      customerSurname = str(Interface.surnameEntry.get())
      return customerSurname




    
class Persistance:      
  def __init__(self):
    self.bookingDetails = None
    
    
  def Find(Interface):            #function to get customer details from booking list     
    ID = (Entity.getID(Interface))
    cur.execute("""SELECT customer_Firstname, customer_Surname
                FROM BookingList    
                WHERE sessionID == %s
                ORDER BY customer_Surname DESC
                """ % (ID))
    search = (cur.fetchall())   #gets results from database execute, prints to shell
    print(search)
    

  def Remove(Interface):        #Function to remove customers from bookinglist table 
    bookingDetails = [Entity.getID(Interface),  #Uses get functions to retive the info 
                      Entity.getForname(Interface), Entity.getSurname(Interface)]
    try:                        #Checks if any details are blank 
      if bookingDetails == ["","",""] or bookingDetails[0] == "" or \
      bookingDetails[1] == "" or bookingDetails[2] == "":    
          print ("Empty fields ")      #tells user if it is, doesnt execute statement
          
      else:
        cur.execute("""DELETE FROM BookingList
                 WHERE
                 sessionID = ? AND
                 customer_Firstname = ? AND
                 customer_Surname = ?
                 """, (bookingDetails))   #Deletes details inputed from table
        conn.commit()
        print("Details" + str(bookingDetails) + "removed from Booking list")    #prints to shell
        
    except TypeError:
      print ("TypeError")
  



if __name__ == "__main__":    
  Controller()    #calls the controller to start the UI

    





  
      



