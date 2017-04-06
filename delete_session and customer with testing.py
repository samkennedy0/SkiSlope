import sqlite3 as lite
from tkinter import *
import tkinter.ttk as ttk


class CustomerImplementation:
    connection = None
    c = None
    def __init__(self, master):
        # construct of the main window
        self.text = Label(master, text="Delete Session")
        self.text.pack()
        self.text["text"] = "       DELETE Customer AND BOOKING"

        name_label = Label(master, text = "Name")
        name_label.pack()
        
        self.nameField = Entry(master, text = "Name", width=50)
        self.nameField.insert(0, "Enter Name")
        self.nameField.pack()

        name_label = Label(master, text = "Details")
        name_label.pack()

        self.ageField = Entry(master, text = "age", width=30)
        self.ageField.insert(0, "Enter Age")
        self.ageField.pack()


        self.dayOfVisit = Entry(master, text = "Day of Visit", width=30)
        self.dayOfVisit.insert(0, "Day of Visit")
        self.dayOfVisit.pack()
        
        self.dayOfLeave = Entry(master, text = "Day of leave", width=30)
        self.dayOfLeave.insert(0, "Day of leave")
        self.dayOfLeave.pack()

        self.btn=Button(master, text='Add', command=self.add_customer_info)
        self.btn.pack()

        self.reloadbtn = Button(master, text='Reload list', command=self.reload_list)
        self.reloadbtn.pack()
        
        self.showbtn = Button(master, text='Update selected', command=self.update_selected)
        self.showbtn.pack()

        self.delbtn = Button(master, text='Delete all', command=self.del_all_notes)
        self.delSelectedbtn = Button(master, text='Delete selected', command=self.del_selected)

        self.delbtn.pack()
        self.delSelectedbtn.pack()
       
        self.content=Listbox(master, width=50)
        self.content.pack()

        # open database
        self.connect_db(db_name = 'register.db')
        self.initial_listBox()

    def connect_db(self, db_name):
        self.conn = lite.connect(db_name)
        self.c = self.conn.cursor()
        # create table
        self.c.execute('''CREATE TABLE IF NOT EXISTS people(name TEXT primary key, age TEXT, dayOfVisit TEXT, dayOfLeave TEXT)''')
        self.conn.commit()

    def initial_listBox(self):
        # read people
        c = self.conn.cursor()
        people = c.execute("SELECT * FROM people")
        self.conn.commit()

        # add to list
        for person in people:
            self.content.insert(END, person)
        self.c.close()
        
    def reload_list(self):
        self.content.delete(0,END)
        self.initial_listBox()

    def clearNameField(self, event):
        self.nameField.delete(0,END)

    def clearAgeField(self, event):
        self.ageField.delete(0,END)

    def cleardayOfVisit(self, event):
        self.dayOfVisit.delete(0,END)

    def clearFbField(self, event):
        self.fbField.delete(0,END)
        
    def add_customer_info(self):
        if self.nameField.get() == "":
            self.text["text"] = "Please type something"
        else:
            name = self.nameField.get()
            age = self.ageField.get()
            dayOfVisit = self.dayOfVisit.get()
            dayOfLeave = self.dayOfLeave.get()
            self.nameField.delete(0, END)
            self.ageField.delete(0, END)
            self.dayOfVisit.delete(0, END)
            self.dayOfLeave.delete(0, END)

            c = self.conn.cursor()

            c.execute("INSERT INTO people VALUES (?, ?, ?, ?)", (name, age, dayOfVisit, dayOfLeave))
            self.conn.commit()
            c.close()

            # add to list
            self.content.insert(END, (name, age, dayOfVisit, dayOfLeave))

    def update_selected(self):
        person = self.content.get(ACTIVE)
        name_search, age_search, dayOfVisit_search, dayOfLeave_search = self.content.get(ACTIVE)
        if self.nameField.get() == "":
            self.text["text"] = "Please type something"
        else:
            name = self.nameField.get()
            age = self.ageField.get()
            dayOfVisit = self.dayOfVisit.get()
            dayOfLeave = self.dayOfLeave.get()
            self.nameField.delete(0, END)
            self.ageField.delete(0, END)
            self.dayOfVisit.delete(0, END)
            self.dayOfLeave.delete(0, END)

        # delete in database
        c = self.conn.cursor()
        c.execute("UPDATE people SET name = ? ,age = ? WHERE name= ? and dayOfVisit=? and dayOfLeave=? ", (name, age, name, dayOfVisit, dayOfLeave))
        self.conn.commit()
        c.close()
        self.reload_list()

    def del_all_notes(self):
        # get selected person       
        c = self.conn.cursor()

        people = self.content.get(0, END)
        if len(people):
            for name,age,dayOfVisit,dayOfLeave in people:
                # delete all from database
                c.execute("DELETE FROM people WHERE  name=? and age=? and dayOfVisit=? and dayOfLeave=?", (name, age, dayOfVisit, dayOfLeave))
                self.conn.commit()
        c.close()
        
        # delete on list
        self.content.delete(0,END)
        
    def del_selected(self):
        # get selected person       
        person = self.content.get(ACTIVE)
        name, age, dayOfVisit, dayOfLeave = self.content.get(ACTIVE)
        # delete in database
        c = self.conn.cursor()
        c.execute("DELETE FROM people WHERE name=? and age=? and dayOfVisit=? and dayOfLeave=? ", (name, age, dayOfVisit, dayOfLeave))
        self.conn.commit()
        c.close()
        

        # delete on list
        self.content.delete(ANCHOR)



root = Tk()
CustomerImplementation(root)
root.mainloop()
