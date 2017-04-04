from tkinter import *
from tkinter import ttk
import datetime
import sqlite3
import os

class MembershipTesting:
    def __init__(self):
        """During object construction, all tests are run"""
        addTest = self.addMemberTest()
        if addTest:    
            print("Add Member Testing Passed!")
        else:
            print("Add Member Testing Failed")
            
        deleteTest = self.deleteMemberTest()
        if deleteTest:
            print("Delete Member Testing Passed!")
        else:
            print("Delete Member Testing Failed")

        upgradeTest = self.upgradeMemberTest()
        if upgradeTest:
            print("Upgrade Member Testing Passed!")
        else:
            print("Upgrade Member Testing Failed")

        if addTest and deleteTest and upgradeTest:
            print("All tests successful!")
            
    def addMemberTest(self):
        global test_db
        test_db = True
        test_controller = MemberController()
        #Tests are conducted using a temporary new database to prevent interference with the normal database
        test_controller.addMember("John","Smith",3,str(datetime.datetime.now())[:10],False)
        test_controller.addMember("Lorem","Ipsum",15,str(datetime.datetime.now())[:10],True)
        test_controller.addMember("First Name","Last Name",999,str(datetime.datetime.now())[:10],False)
        test_controller.addMember("forename","surname",0,str(datetime.datetime.now())[:10],True)
        test_controller.addMember("One","Two",10000,"2016-04-08",True)

        #If searching the details of the added members returns the expected result, the test is successful
        if test_controller.searchMembers("John","Smith",'3','4',str(datetime.datetime.now())[:10],"Basic Members Only")[0] != (1, 'John', 'Smith', 3, str(datetime.datetime.now())[:10], 'BASIC'):
            os.remove('testDB.db')
            print("test 1 failure")
            return False
        if test_controller.searchMembers("Lorem","Ipsum",'15','16',str(datetime.datetime.now())[:10],"Loyal Members Only")[0] != (2, 'Lorem', 'Ipsum', 15, str(datetime.datetime.now())[:10], 'LOYAL'):
            os.remove('testDB.db')
            print("test 2 failure")
            return False
        if test_controller.searchMembers("First Name","Last Name",'999','1000',str(datetime.datetime.now())[:10],"Basic Members Only")[0] != (3, 'First Name', 'Last Name', 999, str(datetime.datetime.now())[:10], 'BASIC'):
            os.remove('testDB.db')
            print("test 3 failure")
            return False
        if test_controller.searchMembers("forename","surname",'0','1',str(datetime.datetime.now())[:10],"Loyal Members Only")[0] != (4, 'forename', 'surname', 0, str(datetime.datetime.now())[:10], 'LOYAL'):
            os.remove('testDB.db')
            print("test 4 failure")
            return False
        if test_controller.searchMembers("One","Two",'10000','10001',"2016-04-08","Loyal Members Only")[0] != (5, 'One', 'Two', 10000, "2016-04-08", 'LOYAL'):
            os.remove('testDB.db')
            print("test 5 failure")
            return False
        
        os.remove('testDB.db')
        return True

    def deleteMemberTest(self):
        global test_db
        test_db = True
        test_controller = MemberController()
        
        test_controller.addMember("John","Smith",3,str(datetime.datetime.now())[:10],False)
        test_controller.addMember("Lorem","Ipsum",15,str(datetime.datetime.now())[:10],True)
        test_controller.addMember("First Name","Last Name",999,str(datetime.datetime.now())[:10],False)
        test_controller.addMember("forename","surname",0,str(datetime.datetime.now())[:10],True)
        test_controller.addMember("One","Two",10000,"2016-04-08",True)

        #Member IDs can be safely assumed in this test environment
        test_controller.deleteMember(1)
        test_controller.deleteMember(2)
        test_controller.deleteMember(3)
        test_controller.deleteMember(4)
        test_controller.deleteMember(5)

        #If searching for the member returns a result, the deletion was not successful
        if len(test_controller.searchMembers("John","Smith",'3','4',str(datetime.datetime.now())[:10],"Basic Members Only"))>0:
            os.remove('testDB.db')
            print("test 1 failure")
            return False
        if len(test_controller.searchMembers("Lorem","Ipsum",'15','16',str(datetime.datetime.now())[:10],"Loyal Members Only"))>0:
            os.remove('testDB.db')
            print("test 2 failure")
            return False
        if len(test_controller.searchMembers("First Name","Last Name",'999','1000',str(datetime.datetime.now())[:10],"Basic Members Only"))>0:
            os.remove('testDB.db')
            print("test 3 failure")
            return False
        if len(test_controller.searchMembers("forename","surname",'0','1',str(datetime.datetime.now())[:10],"Loyal Members Only"))>0:
            os.remove('testDB.db')
            print("test 4 failure")
            return False
        if len(test_controller.searchMembers("One","Two",'10000','10001',"2016-04-08","Loyal Members Only"))>0:
            os.remove('testDB.db')
            print("test 5 failure")
            return False
        
        os.remove('testDB.db')
        return True

    def upgradeMemberTest(self):
        global test_db
        test_db = True
        test_controller = MemberController()
        
        test_controller.addMember("John","Smith",13,str(datetime.datetime.now())[:10],False)
        test_controller.addMember("Lorem","Ipsum",15,str(datetime.datetime.now())[:10],False)
        test_controller.addMember("First Name","Last Name",999,str(datetime.datetime.now())[:10],False)
        test_controller.addMember("forename","surname",10,str(datetime.datetime.now())[:10],False)
        test_controller.addMember("One","Two",10000,"2016-04-08",False)

        test_controller.upgradeMember(1)
        test_controller.upgradeMember(2)
        test_controller.upgradeMember(3)
        test_controller.upgradeMember(4)
        test_controller.upgradeMember(5)

        #By searching restricted to loyal members only, this can be used to show if the member was upgraded
        if len(test_controller.searchMembers("John","Smith",'13','14',str(datetime.datetime.now())[:10],"Loyal Members Only"))==0:
            os.remove('testDB.db')
            print("test 1 failure")
            return False
        if len(test_controller.searchMembers("Lorem","Ipsum",'15','16',str(datetime.datetime.now())[:10],"Loyal Members Only"))==0:
            os.remove('testDB.db')
            print("test 2 failure")
            return False
        if len(test_controller.searchMembers("First Name","Last Name",'999','1000',str(datetime.datetime.now())[:10],"Loyal Members Only"))==0:
            os.remove('testDB.db')
            print("test 3 failure")
            return False
        if len(test_controller.searchMembers("forename","surname",'10','11',str(datetime.datetime.now())[:10],"Loyal Members Only"))==0:
            os.remove('testDB.db')
            print("test 4 failure")
            return False
        if len(test_controller.searchMembers("One","Two",'10000','10001',"2016-04-08","Loyal Members Only"))==0:
            os.remove('testDB.db')
            print("test 5 failure")
            return False
        
        os.remove('testDB.db')
        return True

        

class MembershipUserInterface:
    
    def __init__(self):
        #for consistency, store field values as attributes
        global test_db
        test_db = False
        self.input_first_name = ""
        self.input_last_name = ""
        self.input_sessions_booked = 0
        self.input_date_joined = datetime.datetime.now() #UNIX time default date
        self.is_loyal = False

        #define common fonts
        self.logo_font = ("Veranda",19)
        self.title_font = ("Veranda",16)
        self.button_font = ("Veranda",10)

        #define common geometries
        self.main_window_size = 300, 300
        self.add_window_size = 300, 420
        self.delete_window_size = 300, 480
        self.upgrade_window_size = 300, 480
        self.search_window_size = 600, 500
        
        self.button_padding = 10
        self.title_padding = 15
        
        self.mainLoop()

    def getDate(self):
        self.input_date_joined = str(datetime.datetime.now())[:10]
        
    def mainLoop(self):
        #root initialisation
        self.main_root_window = Tk()
        self.main_root_window.title("The Sphere: Memberships")
        self.main_root_window.geometry('{}x{}'.format(self.main_window_size[0],self.main_window_size[1]))

        """TEXT"""
        #company title
        main_sphere_title = Label(self.main_root_window,text="The Sphere", font = self.logo_font)
        main_sphere_title.pack()

        #subinterface title
        main_membership_title = Label(self.main_root_window, text = "MEMBERSHIPS", font = self.title_font)
        main_membership_title.pack(pady=self.title_padding)

        """BUTTONS"""
        #add member button
        main_add_member_button = Button(self.main_root_window, text = "Add Member", font = self.button_font, command = self.mainAddMemberCallback)
        main_add_member_button.pack(pady=self.button_padding)

        #delete member button
        main_delete_member_button = Button(self.main_root_window, text = "Delete Member", font = self.button_font, command = self.mainDeleteMemberCallback)
        main_delete_member_button.pack(pady=self.button_padding)

        #upgrade member button
        main_upgrade_member_button = Button(self.main_root_window, text = "Upgrade Member", font = self.button_font, command = self.mainUpgradeMemberCallback)
        main_upgrade_member_button.pack(pady=self.button_padding)

        #upgrade member button
        main_exit_button = Button(self.main_root_window, text = "Exit Memberships", font = self.button_font, command = self.mainExitCallback)
        main_exit_button.pack(pady=self.button_padding*2)

        #Loops the interface, ALWAYS KEEP AT BOTTOM
        self.main_root_window.mainloop()

    def mainAddMemberCallback(self):
        #Other sections of the interface are loaded by destroying the current one and initialising the new one
        self.main_root_window.destroy()
        self.addLoop()
    def mainDeleteMemberCallback(self):
        self.main_root_window.destroy()
        self.deleteLoop()
    def mainUpgradeMemberCallback(self):
        self.main_root_window.destroy()
        self.upgradeLoop()
    def mainExitCallback(self):
        self.main_root_window.destroy()

    def addLoop(self):

        #root initialisation
        self.add_root_window = Tk()
        self.add_root_window.title("The Sphere: Add Member")
        self.add_root_window.geometry('{}x{}'.format(self.add_window_size[0],self.add_window_size[1]))

        """TEXT"""
        #company title
        add_sphere_title = Label(self.add_root_window,text="The Sphere", font = self.logo_font)
        add_sphere_title.pack()

        #subinterface title
        add_membership_title = Label(self.add_root_window, text = "ADD MEMBER", font = self.title_font)
        add_membership_title.pack(pady=self.title_padding)

        """FIELDS"""
        #first name label
        add_first_name_label = Label(self.add_root_window, text = "First Name", font = self.button_font)
        add_first_name_label.pack()
        
        #first name field
        self.add_first_name = StringVar(self.add_root_window)
        add_first_name_entry = Entry(self.add_root_window, textvariable = self.add_first_name)
        add_first_name_entry.pack(pady=self.button_padding)

        #last name label
        add_last_name_label = Label(self.add_root_window, text = "Last Name", font = self.button_font)
        add_last_name_label.pack()

        #last name field
        self.add_last_name = StringVar(self.add_root_window)
        add_last_name_entry = Entry(self.add_root_window, textvariable = self.add_last_name)
        add_last_name_entry.pack(pady=self.button_padding)

        #sessions booked label
        add_sessions_booked_label = Label(self.add_root_window, text = "Sessions Booked", font = self.button_font)
        add_sessions_booked_label.pack()

        #sessions booked field
        self.add_sessions_booked = StringVar(self.add_root_window)
        add_sessions_booked_entry = Entry(self.add_root_window, textvariable = self.add_sessions_booked)
        add_sessions_booked_entry.pack(pady=self.button_padding)

        #loyal checkbox
        self.add_is_loyal = IntVar(self.add_root_window)
        add_is_loyal_checkbox = Checkbutton(self.add_root_window, text = "Loyal Member? ", variable = self.add_is_loyal)
        add_is_loyal_checkbox.pack(pady=self.button_padding)

        """BUTTONS"""
        #submit button
        add_submit_button = Button(self.add_root_window, text = "Add Member", font = self.button_font, command = self.addSubmitCallback)
        add_submit_button.pack(pady=self.button_padding)

        #return button
        add_return_button = Button(self.add_root_window, text = "Return to Memberships", font = self.button_font, command = self.addReturnCallback)
        add_return_button.pack(pady=self.button_padding)

        #Loops the interface, ALWAYS KEEP AT BOTTOM
        self.add_root_window.mainloop()

    def addSubmitCallback(self):
        #StringVars have to be specifically retrieved
        self.input_first_name = self.add_first_name.get()
        self.input_last_name = self.add_last_name.get()

        #Input fields are text by default, this requires conversion
        self.input_sessions_booked = int(self.add_sessions_booked.get())
        self.getDate()
        self.input_is_loyal = self.add_is_loyal.get()

        #A controller is specifically constructed to add a member
        member_controller = MemberController()
        member_controller.addMember(self.input_first_name, self.input_last_name, self.input_sessions_booked, self.input_date_joined, self.input_is_loyal)
        
    def addReturnCallback(self):
        self.add_root_window.destroy()
        self.mainLoop()

    def deleteLoop(self):

        #root initialisation
        self.delete_root_window = Tk()
        self.delete_root_window.title("The Sphere: Delete Member")
        self.delete_root_window.geometry('{}x{}'.format(self.delete_window_size[0],self.delete_window_size[1]))

        """TEXT"""
        #company title
        delete_sphere_title = Label(self.delete_root_window,text="The Sphere", font = self.logo_font)
        delete_sphere_title.pack()

        #subinterface title
        delete_membership_title = Label(self.delete_root_window, text = "DELETE MEMBER", font = self.title_font)
        delete_membership_title.pack(pady=self.title_padding)

        """FIELDS"""
        #first name label
        delete_first_name_label = Label(self.delete_root_window, text = "First Name", font = self.button_font)
        delete_first_name_label.pack()
        
        #first name field
        self.delete_first_name = StringVar(self.delete_root_window)
        delete_first_name_entry = Entry(self.delete_root_window, textvariable = self.delete_first_name)
        delete_first_name_entry.pack(pady=self.button_padding)

        #last name label
        delete_last_name_label = Label(self.delete_root_window, text = "Last Name", font = self.button_font)
        delete_last_name_label.pack()

        #last name field
        self.delete_last_name = StringVar(self.delete_root_window)
        delete_last_name_entry = Entry(self.delete_root_window, textvariable = self.delete_last_name)
        delete_last_name_entry.pack(pady=self.button_padding)

        #sessions booked min label
        delete_sessions_booked_min_label = Label(self.delete_root_window, text = "Minimum Sessions Booked", font = self.button_font)
        delete_sessions_booked_min_label.pack()

        #sessions booked min field
        self.delete_sessions_booked_min = StringVar(self.delete_root_window)
        delete_sessions_booked_min_entry = Entry(self.delete_root_window, textvariable = self.delete_sessions_booked_min)
        delete_sessions_booked_min_entry.pack(pady=self.button_padding)

        #sessions booked max label
        delete_sessions_booked_min_label = Label(self.delete_root_window, text = "Maximum Sessions Booked", font = self.button_font)
        delete_sessions_booked_min_label.pack()

        #sessions booked max field
        self.delete_sessions_booked_max = StringVar(self.delete_root_window)
        delete_sessions_booked_max_entry = Entry(self.delete_root_window, textvariable = self.delete_sessions_booked_max)
        delete_sessions_booked_max_entry.pack(pady=self.button_padding)

        #loyal listbox
        self.delete_loyalty = StringVar(self.delete_root_window)
        self.delete_loyalty.set("All Member Types")
        
        self.delete_loyalty_option = OptionMenu(self.delete_root_window,self.delete_loyalty,"All Member Types","Basic Members Only", "Loyal Members Only")
        self.delete_loyalty_option.pack(pady=self.button_padding)

        """BUTTONS"""
        #submit button
        delete_search_button = Button(self.delete_root_window, text = "Search Members", font = self.button_font, command = self.deleteSearchCallback)
        delete_search_button.pack(pady=self.button_padding)

        #return button
        delete_return_button = Button(self.delete_root_window, text = "Return to Memberships", font = self.button_font, command = self.deleteReturnCallback)
        delete_return_button.pack(pady=self.button_padding)

        #Loops the interface, ALWAYS KEEP AT BOTTOM
        self.delete_root_window.mainloop()

    def deleteSearchCallback(self):
        self.input_first_name = self.delete_first_name.get()
        self.input_last_name = self.delete_last_name.get()

        self.input_sessions_booked_min = self.delete_sessions_booked_min.get()

        self.input_sessions_booked_max = self.delete_sessions_booked_max.get()
            
        self.getDate()
        self.input_is_loyal = self.delete_loyalty.get()

        member_controller = MemberController()
        results = member_controller.searchMembers(self.input_first_name, self.input_last_name, self.input_sessions_booked_min, self.input_sessions_booked_max, self.input_date_joined, self.input_is_loyal)

        self.searchdeleteLoop(results)
        
    def deleteReturnCallback(self):
        self.delete_root_window.destroy()
        self.mainLoop()

    def searchdeleteLoop(self,results):
        #root initialisation
        self.searchdelete_root_window = Tk()
        self.searchdelete_root_window.title("The Sphere: Delete Member")
        self.searchdelete_root_window.geometry('{}x{}'.format(self.search_window_size[0],self.search_window_size[1]))

        """TEXT"""
        #company title
        searchdelete_sphere_title = Label(self.searchdelete_root_window,text="The Sphere", font = self.logo_font)
        searchdelete_sphere_title.pack()

        #subinterface title
        searchdelete_section_title = Label(self.searchdelete_root_window, text = "SEARCH RESULTS", font = self.title_font)
        searchdelete_section_title.pack(pady=self.title_padding)

        """TREE"""
        self.searchdelete_tree = ttk.Treeview(self.searchdelete_root_window)
        self.searchdelete_tree["columns"] = ("ID","First Name","Last Name","Sessions Booked","Date Joined","Member Type")
        self.searchdelete_tree["show"] = "headings"

        self.searchdelete_tree.column("ID", width=self.search_window_size[0]//12)
        self.searchdelete_tree.column("First Name", width=self.search_window_size[0]//4)
        self.searchdelete_tree.column("Last Name", width=self.search_window_size[0]//4)
        self.searchdelete_tree.column("Sessions Booked", width=self.search_window_size[0]//12)
        self.searchdelete_tree.column("Date Joined", width=self.search_window_size[0]//6)
        self.searchdelete_tree.column("Member Type", width=self.search_window_size[0]//6)

        self.searchdelete_tree.heading("ID",text="ID")
        self.searchdelete_tree.heading("First Name",text="First Name")
        self.searchdelete_tree.heading("Last Name",text="Last Name")
        self.searchdelete_tree.heading("Sessions Booked",text="Sessions Booked")
        self.searchdelete_tree.heading("Date Joined",text="Date Joined")
        self.searchdelete_tree.heading("Member Type",text="Member Type")

        #The selected item is updated upon mouse release, this ensures the currently selected item is actually stored
        self.searchdelete_tree.bind('<ButtonRelease-1>', self.searchdeleteSelection)

        for row in results:
            #The results are already in the same format needed for the tree
            self.searchdelete_tree.insert("",0,values=row)

        self.searchdelete_tree.pack()

        """BUTTONS"""
        #submit button
        searchdelete_submit_button = Button(self.searchdelete_root_window, text = "Delete Selected Member", font = self.button_font, command = self.searchdeleteSubmitCallback)
        searchdelete_submit_button.pack(pady=self.button_padding)

        #return button
        searchdelete_return_button = Button(self.searchdelete_root_window, text = "Exit Search", font = self.button_font, command = self.searchdeleteReturnCallback)
        searchdelete_return_button.pack(pady=self.button_padding)

        #Loops the interface, ALWAYS KEEP AT BOTTOM
        self.searchdelete_root_window.mainloop()

    def searchdeleteSelection(self,arg):
        #Update selection
        self.searchdelete_selection = self.searchdelete_tree.item(self.searchdelete_tree.focus())

    def searchdeleteSubmitCallback(self):
        #Values 1 and 2 correspond to the member name
        member_name = self.searchdelete_selection["values"][1] + " " + self.searchdelete_selection["values"][2]
        #A prompt is used to prevent accidental deletion
        answer = messagebox.askquestion("Delete Member","Are you sure you want to delete " + member_name + " from the database?", icon='warning')
        if answer == "yes":
            member_controller = MemberController()
            member_controller.deleteMember(self.searchdelete_selection["values"][0]) #Value 0 is the member ID, so no additional information is needed
            messagebox.showinfo("Deletion Successful",member_name + " has been successfully deleted from the database.")
            self.searchdelete_root_window.destroy()
            self.deleteSearchCallback()
        else:
            return

    def searchdeleteReturnCallback(self):
        self.searchdelete_root_window.destroy()
        
    def upgradeLoop(self):

        #root initialisation
        self.upgrade_root_window = Tk()
        self.upgrade_root_window.title("The Sphere: Upgrade Member")
        self.upgrade_root_window.geometry('{}x{}'.format(self.upgrade_window_size[0],self.upgrade_window_size[1]))

        """TEXT"""
        #company title
        upgrade_sphere_title = Label(self.upgrade_root_window,text="The Sphere", font = self.logo_font)
        upgrade_sphere_title.pack()

        #subinterface title
        upgrade_membership_title = Label(self.upgrade_root_window, text = "UPGRADE MEMBER", font = self.title_font)
        upgrade_membership_title.pack(pady=self.title_padding)

        """FIELDS"""
        #first name label
        upgrade_first_name_label = Label(self.upgrade_root_window, text = "First Name", font = self.button_font)
        upgrade_first_name_label.pack()
        
        #first name field
        self.upgrade_first_name = StringVar(self.upgrade_root_window)
        upgrade_first_name_entry = Entry(self.upgrade_root_window, textvariable = self.upgrade_first_name)
        upgrade_first_name_entry.pack(pady=self.button_padding)

        #last name label
        upgrade_last_name_label = Label(self.upgrade_root_window, text = "Last Name", font = self.button_font)
        upgrade_last_name_label.pack()

        #last name field
        self.upgrade_last_name = StringVar(self.upgrade_root_window)
        upgrade_last_name_entry = Entry(self.upgrade_root_window, textvariable = self.upgrade_last_name)
        upgrade_last_name_entry.pack(pady=self.button_padding)

        #sessions booked min label
        upgrade_sessions_booked_min_label = Label(self.upgrade_root_window, text = "Minimum Sessions Booked", font = self.button_font)
        upgrade_sessions_booked_min_label.pack()

        #sessions booked min field
        self.upgrade_sessions_booked_min = StringVar(self.upgrade_root_window)
        upgrade_sessions_booked_min_entry = Entry(self.upgrade_root_window, textvariable = self.upgrade_sessions_booked_min)
        upgrade_sessions_booked_min_entry.pack(pady=self.button_padding)

        #sessions booked max label
        upgrade_sessions_booked_min_label = Label(self.upgrade_root_window, text = "Maximum Sessions Booked", font = self.button_font)
        upgrade_sessions_booked_min_label.pack()

        #sessions booked max field
        self.upgrade_sessions_booked_max = StringVar(self.upgrade_root_window)
        upgrade_sessions_booked_max_entry = Entry(self.upgrade_root_window, textvariable = self.upgrade_sessions_booked_max)
        upgrade_sessions_booked_max_entry.pack(pady=self.button_padding)

        """BUTTONS"""
        #submit button
        upgrade_search_button = Button(self.upgrade_root_window, text = "Search Members", font = self.button_font, command = self.upgradeSearchCallback)
        upgrade_search_button.pack(pady=self.button_padding)

        #return button
        upgrade_return_button = Button(self.upgrade_root_window, text = "Return to Memberships", font = self.button_font, command = self.upgradeReturnCallback)
        upgrade_return_button.pack(pady=self.button_padding)

        #Loops the interface, ALWAYS KEEP AT BOTTOM
        self.upgrade_root_window.mainloop()

    def upgradeSearchCallback(self):
        self.input_first_name = self.upgrade_first_name.get()
        self.input_last_name = self.upgrade_last_name.get()

        self.input_sessions_booked_min = self.upgrade_sessions_booked_min.get()
        self.input_sessions_booked_max = self.upgrade_sessions_booked_max.get()

        #Filtering is necessary to ensure members who have not booked for at least 10 sessions are not accessible by the upgrade menu
        if len(self.input_sessions_booked_min) == 0:
            self.input_sessions_booked_min = "10"

        if int(self.input_sessions_booked_min) < 10:
            self.input_sessions_booked_min = "10"

        if len(self.input_sessions_booked_max) == 0:
            self.input_sessions_booked_max = "999999999"
            
        if int(self.input_sessions_booked_max) < 10:
            self.input_sessions_booked_max = "10"
        
        self.getDate()

        member_controller = MemberController()
        results = member_controller.searchMembers(self.input_first_name, self.input_last_name, self.input_sessions_booked_min, self.input_sessions_booked_max, self.input_date_joined, "Basic Members Only")

        self.searchupgradeLoop(results)
        
    def upgradeReturnCallback(self):
        self.upgrade_root_window.destroy()
        self.mainLoop()

    def searchupgradeLoop(self,results):
        #root initialisation
        self.searchupgrade_root_window = Tk()
        self.searchupgrade_root_window.title("The Sphere: Upgrade Member")
        self.searchupgrade_root_window.geometry('{}x{}'.format(self.search_window_size[0],self.search_window_size[1]))

        """TEXT"""
        #company title
        searchupgrade_sphere_title = Label(self.searchupgrade_root_window,text="The Sphere", font = self.logo_font)
        searchupgrade_sphere_title.pack()

        #subinterface title
        searchupgrade_section_title = Label(self.searchupgrade_root_window, text = "SEARCH RESULTS", font = self.title_font)
        searchupgrade_section_title.pack(pady=self.title_padding)

        """TREE"""
        self.searchupgrade_tree = ttk.Treeview(self.searchupgrade_root_window)
        self.searchupgrade_tree["columns"] = ("ID","First Name","Last Name","Sessions Booked","Date Joined","Member Type")
        self.searchupgrade_tree["show"] = "headings"

        self.searchupgrade_tree.column("ID", width=self.search_window_size[0]//12)
        self.searchupgrade_tree.column("First Name", width=self.search_window_size[0]//4)
        self.searchupgrade_tree.column("Last Name", width=self.search_window_size[0]//4)
        self.searchupgrade_tree.column("Sessions Booked", width=self.search_window_size[0]//12)
        self.searchupgrade_tree.column("Date Joined", width=self.search_window_size[0]//6)
        self.searchupgrade_tree.column("Member Type", width=self.search_window_size[0]//6)

        self.searchupgrade_tree.heading("ID",text="ID")
        self.searchupgrade_tree.heading("First Name",text="First Name")
        self.searchupgrade_tree.heading("Last Name",text="Last Name")
        self.searchupgrade_tree.heading("Sessions Booked",text="Sessions Booked")
        self.searchupgrade_tree.heading("Date Joined",text="Date Joined")
        self.searchupgrade_tree.heading("Member Type",text="Member Type")

        self.searchupgrade_tree.bind('<ButtonRelease-1>', self.searchupgradeSelection)

        for row in results:
            self.searchupgrade_tree.insert("",0,values=row)

        self.searchupgrade_tree.pack()

        """BUTTONS"""
        #submit button
        searchupgrade_submit_button = Button(self.searchupgrade_root_window, text = "Upgrade Selected Member", font = self.button_font, command = self.searchupgradeSubmitCallback)
        searchupgrade_submit_button.pack(pady=self.button_padding)

        #return button
        searchupgrade_return_button = Button(self.searchupgrade_root_window, text = "Exit Search", font = self.button_font, command = self.searchupgradeReturnCallback)
        searchupgrade_return_button.pack(pady=self.button_padding)

        #Loops the interface, ALWAYS KEEP AT BOTTOM
        self.searchupgrade_root_window.mainloop()

    def searchupgradeSelection(self,arg):
        self.searchupgrade_selection = self.searchupgrade_tree.item(self.searchupgrade_tree.focus())

    def searchupgradeSubmitCallback(self):
        member_name = self.searchupgrade_selection["values"][1] + " " + self.searchupgrade_selection["values"][2]
        answer = messagebox.askquestion("Upgrade Member","Are you sure you want to upgrade " + member_name + "?", icon='warning')
        if answer == "yes":
            member_controller = MemberController()
            member_controller.upgradeMember(self.searchupgrade_selection["values"][0])
            messagebox.showinfo("Upgrade Successful",member_name + " has been successfully upgraded to a loyal member.")
            self.searchupgrade_root_window.destroy()
            self.upgradeSearchCallback()
        else:
            return

    def searchupgradeReturnCallback(self):
        self.searchupgrade_root_window.destroy()

class MemberController:
    def __init__(self):
        pass
    def addMember(self, first_name, last_name, sessions_booked, date_joined, is_loyal):
        #MemberFactory handles member construction separately
        member_factory = MemberFactory(first_name, last_name, sessions_booked, date_joined, is_loyal)
        return member_factory.getMember()
    def searchMembers(self, first_name, last_name, sessions_booked_min, sessions_booked_max, date_joined, is_loyal):
        #A generic data access class is necessary when we are not sure which member types will be returned
        member_impl = GenericMemberImpl()
        if len(first_name) == 0:
            first_name = ''
        else:
            first_name = "first_name = '" + first_name + "' AND" #Portions of the query are only added if values were specified for them

        if len(last_name) == 0:
            last_name = ''
        else:
            last_name = "last_name = '" + last_name + "' AND"

        if len(sessions_booked_max) == 0:
            sessions_booked_max = 999999999
        else:
            sessions_booked_max = int(sessions_booked_max)

        if len(sessions_booked_min) == 0:
            sessions_booked_min = 0
        else:
            sessions_booked_min = int(sessions_booked_min)

        if is_loyal == "All Member Types": #The dropdown box values are translated to member types
            is_loyal = ""
        if is_loyal == "Basic Members Only":
            is_loyal = "member_type = 'BASIC' AND"
        if is_loyal == "Loyal Members Only":
            is_loyal = "member_type = 'LOYAL' AND"
            
        
        return member_impl.searchMembers(first_name,last_name,sessions_booked_min,sessions_booked_max,date_joined,is_loyal).fetchall()

    def deleteMember(self,member_id):
        generic_member_impl = GenericMemberImpl()
        generic_member_impl.deleteMember(member_id)

    def upgradeMember(self,member_id):
        generic_member_impl = GenericMemberImpl()
        generic_member_impl.upgradeMember(member_id)

class MemberFactory:
    def __init__(self, first_name, last_name, sessions_booked, date_joined, is_loyal):
        if is_loyal:
            self.member = self.getLoyalMember(first_name, last_name, sessions_booked, date_joined)
        else:
            self.member = self.getBasicMember(first_name, last_name, sessions_booked, date_joined)
        self.member.saveData()

    def getMember(self):
        return self.member
    
    def getBasicMember(self, first_name, last_name, sessions_booked, date_joined):
        return BasicMember(first_name, last_name, sessions_booked, date_joined)
    
    def getLoyalMember(self, first_name, last_name, sessions_booked, date_joined):
        return LoyalMember(first_name, last_name, sessions_booked, date_joined)

class Member:
    def __init__(self, first_name, last_name, sessions_booked, date_joined):
        self.first_name = first_name
        self.last_name = last_name
        self.sessions_booked = sessions_booked
        self.date_joined = date_joined
        
    def getFirstName(self):
        return self.first_name
    def setFirstName(self, first_name):
        self.first_name = first_name

    def getLastName(self):
        return self.last_name
    def setLastName(self, last_name):
        self.last_name = last_name

    def getSessionsBooked(self):
        return self.sessions_booked
    def setSessionsBooked(self, sessions_booked):
        self.sessions_booked = sessions_booked

    def getDateJoined(self):
        return self.date_joined
    def setDateJoined(self, date_joined):
        self.date_joined = date_joined

    def calcPayment(self):
        pass

class BasicMember(Member):
    def saveData(self):
        #Each member type uses their own data access methods
        basic_member_impl = BasicMemberImpl([self])
        basic_member_impl.writeAll()

class LoyalMember(Member):
    def saveData(self):
        loyal_member_impl = LoyalMemberImpl([self])
        loyal_member_impl.writeAll()      

class BasicMemberImpl:
    def __init__(self, members):
        self.members = members

        #Check if this is a unit test, if so, use a temporary test database
        global test_db
        db_exists = False
        self.db_name = 'MemberDB.db'
        if test_db:
            self.db_name = 'testDB.db'
        if os.path.isfile(self.db_name):
            db_exists = True

        self.db_connection = sqlite3.connect(self.db_name)
        self.sql_cursor = self.db_connection.cursor()

        if not db_exists:
            self.sql_cursor.execute("CREATE TABLE Members(id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, sessions_booked INTEGER NOT NULL, date_joined TEXT NOT NULL, member_type TEXT DEFAULT BASIC);")
    
    def writeAll(self):
        for member in self.members:
            self.writeMember(member.first_name,member.last_name,member.sessions_booked,member.date_joined)
    
    def writeMember(self, first_name, last_name, sessions_booked, date_joined):
        self.sql_cursor.execute("INSERT INTO Members (first_name,last_name,sessions_booked,date_joined) VALUES ('%s','%s',%d,'%s')" % (first_name,last_name,sessions_booked,date_joined))
        self.db_connection.commit()

class LoyalMemberImpl:
    def __init__(self, members):
        self.members = members
        global test_db
        db_exists = False
        self.db_name = 'MemberDB.db'
        if test_db:
            self.db_name = 'testDB.db'
        if os.path.isfile(self.db_name):
            db_exists = True

        self.db_connection = sqlite3.connect(self.db_name)
        self.sql_cursor = self.db_connection.cursor()

        if not db_exists:
            self.sql_cursor.execute("CREATE TABLE Members(id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, sessions_booked INTEGER NOT NULL, date_joined TEXT NOT NULL, member_type TEXT DEFAULT BASIC);")

    def writeAll(self):
        for member in self.members:
            self.writeMember(member.first_name,member.last_name,member.sessions_booked,member.date_joined)

    def writeMember(self, first_name, last_name, sessions_booked, date_joined):
        self.sql_cursor.execute("INSERT INTO Members (first_name,last_name,sessions_booked,date_joined,member_type) VALUES ('%s','%s',%d,'%s','LOYAL')" % (first_name,last_name,sessions_booked,date_joined))
        self.db_connection.commit()
        
class GenericMemberImpl:
    def __init__(self):
        global test_db
        self.db_name = 'MemberDB.db'
        if test_db:
            self.db_name = 'testDB.db'
        db_exists = False

        if os.path.isfile(self.db_name):
            db_exists = True

        self.db_connection = sqlite3.connect(self.db_name)
        self.sql_cursor = self.db_connection.cursor()

        if not db_exists:
            self.sql_cursor.execute("CREATE TABLE Members(id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, sessions_booked INTEGER NOT NULL, date_joined TEXT NOT NULL, member_type TEXT DEFAULT BASIC);")
    
    def searchMembers(self, first_name, last_name, sessions_booked_min, sessions_booked_max, date_joined, is_loyal):
        return self.sql_cursor.execute("SELECT * FROM Members WHERE %s %s %s sessions_booked BETWEEN %d AND %d" % (first_name,last_name,is_loyal,sessions_booked_min,sessions_booked_max))

    def deleteMember(self, member_id):
        self.sql_cursor.execute("DELETE FROM Members WHERE id = %d" % (member_id))
        self.db_connection.commit()

    def upgradeMember(self, member_id):
        self.sql_cursor.execute("UPDATE Members SET member_type = 'LOYAL' WHERE id = %d" % (member_id))
        self.db_connection.commit()
    
if __name__ == "__main__":
    main_win = MembershipUserInterface()
else:
    #testing
    test = MembershipTesting()

    #debug
    dbg_win = MembershipUserInterface()
