from tkinter import *
import sqlite3

conn = sqlite3.connect('C:/Users/samke/Desktop/260CT/skiSlopeDatabase.db')
cur = conn.cursor()

class App:
  def __init__(self, master):
    self.master = master

    theLabel = Label(root, text="Session Prototype")
    theLabel.pack()
      
    middleFrame = Frame(master)
    middleFrame.pack()
    bottomFrame = Frame(master)
    bottomFrame.pack(side=BOTTOM)


    self.add = Button(middleFrame, text="Add Customers to Session", width =25, command=self.addWindow, height =3)
    self.remove = Button(middleFrame, text="Remove Customers", command=self.removeWindow, width =25, height =3)
    self.view = Button(middleFrame,text="View Session", command=self.sessionWindow, width =25, height =3)
    self.exit = Button(bottomFrame,text="Exit", command=exit)

    #self.w = Entry(topFrame, bd=5)
    #self.w.pack(side=RIGHT)

    self.add.pack(padx=5, pady=10, side=LEFT)
    self.remove.pack(padx=5, pady=10, side=RIGHT)
    self.view.pack(padx=5, pady=10,)
    self.exit.pack(side=BOTTOM)

  def sessionWindow(self):
    self.newWindow = Toplevel(self.master)
    self.app = viewSession(self.newWindow)

  def addWindow(self):
    self.newWindow = Toplevel(self.master)
    self.app = addCustomer(self.newWindow)

  def removeWindow(self):
    self.newWindow = Toplevel(self.master)
    self.app = removeCustomer(self.newWindow)


class viewSession:
    def __init__(self, master):
        self.master = master
        topFrame = Frame(master)
        topFrame.pack()
        middleFrame = Frame(master)
        middleFrame.pack()
        bottomFrame = Frame(master)
        bottomFrame.pack()
            
        self.session = Label(topFrame, text="Session ID")
        self.exit = Button(master, text="Exit", width=5, height=2,command=exit)
        self.showin = Button(bottomFrame, text="Show Customers in this Session", command=self.ID_entry)
        self.clear_txt = Button(bottomFrame, text="Clear Customers", command=self.clear)
        self.close = Button(bottomFrame, text="Close Window", command=self.close)
        self.customer_txt = Text(middleFrame)
        
        self.session.pack(side=LEFT, padx=10, pady=5)
        self.exit.pack(side=BOTTOM)
        self.showin.pack(side=TOP)
        self.clear_txt.pack(side=TOP)
        self.close.pack(side=BOTTOM)
        self.customer_txt.pack(side=TOP)
        
        self.w = Entry(topFrame, bd=5)
        self.w.pack(side=RIGHT)

    def ID_entry(self):
        sessionID = self.w.get()
        cur.execute("""SELECT customer_Firstname, customer_Surname
                FROM sessionList    
                WHERE sessionID == %s
                ORDER BY customer_Surname DESC
                """ % (sessionID))
        self.customer_txt.insert(END, cur.fetchall())

    def clear(self):
        self.customer_txt.delete(1.0, END)

    def close(self):
        self.master.destroy()                    

class addCustomer:
  def __init__(self, master):
    self.master = master
    topFrame = Frame(master)
    topFrame.pack()
    middleFrame = Frame(master)
    middleFrame.pack()
    bottomFrame = Frame(master)
    bottomFrame.pack()

    self.idlabel = Label(topFrame, text="Session ID")
    self.firlabel = Label(middleFrame, text="Enter Firstname")
    self.surlabel = Label(bottomFrame, text="Enter Surname")

    self.add = Button(master, text="Add customer", command=self.addCustomer)
    self.close = Button(master, text="Close Window", command=self.close)

    self.idEntry = Entry(topFrame, bd=5)
    self.firstnameEntry = Entry(middleFrame, bd=5)
    self.surnameEntry = Entry(bottomFrame, bd=5)

    self.txt = Text(master, height =7, width = 60)

    self.idlabel.pack(side=LEFT)
    self.firlabel.pack(side=LEFT)
    self.surlabel.pack(side=LEFT)
    self.add.pack(side=TOP)
    self.close.pack(side=BOTTOM)
    self.idEntry.pack(side=LEFT)
    self.firstnameEntry.pack(side=LEFT)
    self.surnameEntry.pack(side=LEFT)
    self.txt.pack(side=TOP)

  def addCustomer(self):
    ID = int(self.idEntry.get())
    firstname =self.firstnameEntry.get()
    surname = self.surnameEntry.get()

    cur.execute("""INSERT INTO sessionList
               (sessionID,customer_Firstname,customer_Surname)
                VALUES (?,?,?)""",[ID,firstname,surname])
    conn.commit()
    self.txt.insert(END, "Customer : %s %s, was added to session No.%d" % (firstname,surname,ID))

  def close(self):
    self.master.destroy()
        
class removeCustomer:
  def __init__(self, master):
    self.master = master
    topFrame = Frame(master)
    topFrame.pack()
    middleFrame = Frame(master)
    middleFrame.pack()
    bottomFrame = Frame(master)
    bottomFrame.pack()

    self.idlabel = Label(topFrame, text="Session ID")
    self.firlabel = Label(middleFrame, text="Enter Firstname")
    self.surlabel = Label(bottomFrame, text="Enter Surname")

    self.add = Button(master, text="Remove customer", command=self.removeCustomer)
    self.close = Button(master, text="Close Window", command=self.close)

    self.idEntry = Entry(topFrame, bd=5)
    self.firstnameEntry = Entry(middleFrame, bd=5)
    self.surnameEntry = Entry(bottomFrame, bd=5)

    self.txt = Text(master, height =7, width = 60)

    self.idlabel.pack(side=LEFT)
    self.firlabel.pack(side=LEFT)
    self.surlabel.pack(side=LEFT)
    self.add.pack(side=TOP)
    self.close.pack(side=BOTTOM)
    self.idEntry.pack(side=LEFT)
    self.firstnameEntry.pack(side=LEFT)
    self.surnameEntry.pack(side=LEFT)
    self.txt.pack(side=TOP)

  def removeCustomer(self):
    ID = int(self.idEntry.get())
    firstname =self.firstnameEntry.get()
    surname = self.surnameEntry.get()

    cur.execute("""DELETE FROM sessionList
             WHERE
             sessionID = ? AND
             customer_Firstname = ? AND
             customer_Surname = ?
             """, (ID,firstname,surname))
    conn.commit()
    self.txt.insert(END, "Customer : %s %s, was removed to session No.%d" % (firstname,surname,ID))

  def close(self):
    self.master.destroy()


conn.commit()

root = Tk()
root.title("Session Prototype")
root.resizable(width=False, height=False)
app = App(root)
root.mainloop()







