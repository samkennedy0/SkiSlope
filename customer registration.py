import sqlite3 as lite # Contains SQLite (the database) and all its commands
from tkinter import * # All of the tkinter commands
import tkinter.ttk as ttk # This is an extra tkinter module, used for comboboxes and tables (trees)

cur = lite.connect('register.db') # This is used to determine the section needed in the database
con=cur.cursor() # This is used to add data to the selected section


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
        for row in con.execute("SELECT * FROM Memberships"):
                item+=1
                itemlist.append(item-1)


        for i in range(1, item):
                con.execute("SELECT MembershipName FROM Memberships WHERE MembershipID=?", (i,))
                Name=con.fetchone()[0]
                con.execute("SELECT MembershipCost FROM Memberships WHERE MembershipID=?", (i,))
                cost=con.fetchone()[0]

                tree.insert("", i, text=i, values=(Name, cost))
        
        lbl4=Label(customeradd, text="Membership?", font=("Arial", 12))
        lbl4.place(x=40, y=280, height=75, width=200)

        combo2 = ttk.Combobox(customeradd, font=("Arial", 12), state='normal', value=itemlist)
        combo2.place(x=270, y=290, height=50, width=200)
        

        lbl6=Label(customeradd, text="Select Session", font=("Arial", 12))
        lbl6.place(x=40, y=375, height=50, width=200)

        listsessionName=[]
        item=1
        
        for row in con.execute("SELECT * FROM Sessions"):
                item+=1
                
        for i in range(1, item):
                con.execute("SELECT SessionName FROM Sessions WHERE SessionID =?", (i,))
                name = con.fetchone()[0]
                listsessionName.append(name)
                
        print(listsessionName)
        combo = ttk.Combobox(customeradd, font=("Arial", 12), state='normal', value=listsessionName)
        combo.place(x=270, y=375, height=50, width=200)

        def confirm():

                #A recursive process that finds the length of the entity, to be used as the latest id
                item=1
                for row in con.execute("SELECT * FROM Customers"):
                        item+=1        
                Id=item 
                Surname=txt1.get() #Retrieves the first textbox value
                Firstname=txt2.get() #retrieves the second textbox vallue
                MembershipID=combo2.get() #Retrieves the third textbox value
                SessionID = combo.get()

                con.execute("SELECT SessionID from Sessions WHERE SessionName =?", (SessionID,))
                sesh = con.fetchone()[0]

                new=[Id, Surname, Firstname, MembershipID, sesh] #All the data retrieved is placed into a list to make it easier to enter
                con.execute("INSERT INTO Customers VALUES(?,?,?,?,?)" ,new) #The list is entered into the database
                cur.commit() # This saves the data from the previous SQLite code into the database
                messagebox.showinfo(customeradd, "Customer added") #Alerts the user that the data has been entered
                customeradd.destroy()

        #The code for the back button is the same as last time, except the button leads to the previous window
        # insted of logging out of the program
        btn1=Button(customeradd, justify=LEFT)
        btn1.place(bordermode=OUTSIDE, height=50, width=50)
        
        #These three lines create and place a silver confirm button, which leads to confirming the data
        btn2=Button(customeradd, text="Confirm", font=("Arial", 12), background="Silver", foreground="Red", command=confirm)
        btn2.place(x=200, y=450, height=50, width=100)

customeradd()
