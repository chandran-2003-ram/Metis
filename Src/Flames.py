import tkinter as tk
from tkinter import ttk, messagebox as msg_box
from urllib.request import urlopen
from urllib.error import URLError
import webbrowser as wb

__version__ = "1.0.0"
wiki_link = "https://github.com/chandran-2003-ram/Metis/wiki/Flames-Game#how-to-play-the-game"
partner_1 = "Partner 1"
partner_2 = "Partner 2"

class FlamesApp(tk.Tk):
    """
    This is the main GUI for the app inherited from 'tk.Tk()' class

    Methods:
    --------

    remove_match_char(self:object, list1:list, list2:list)->list:
        Remove a common character and return a list with a list and a flag value.

    flames(self:object, p1_list:list, p2_list:list)->None:
        Finds the relationship status and display the status to the user.

    reset(self:object)-> None:
        Reset to the initial state of the game.

    name(self:object)-> None:
        Get the valid input strings(i.e. names) and call the flames method.

    process(self:object)->None:
        call a function based on reset status.

    Help(self:object)->None:
        Open the help website of the game.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Variables definition
        self.reset_status = False
        self.partners_names = []
        

        # Root window attributes
        self.title(f"Flames({__version__})")
        self.configure(bg= "#f9e3ef")       #  (magenta-pink - #f9e3ef)
        self.geometry("720x430")

        # Widgets deifition
        self.flames_label = ttk.Label(self, text="Flames", font=("Papyrus",80), background= "#f9e3ef")       # flames title label
        self.partner_label = ttk.Label(self, background= "#f9e3ef", font= ("arial",11), text= partner_1)      # partner label
        self.name_label = ttk.Label(self, background= "#FFC0CB", text= "Name", font= ("arial",11), relief= tk.RIDGE)     # name label
        self.input_box = tk.Entry(self, width= 40, relief= tk.SUNKEN)        # input_box widget
        self.process_bt = tk.Button(self, text= "Enter",font= ("arial", 9), bg= "#FFC0CB", relief= tk.GROOVE, command= lambda : self.process())      # Process button
        self.relation_label = ttk.Label(self, background= "#f9e3ef", foreground= "#A020F0", font= ("arial",11), relief= tk.FLAT)     # relationship label
        self.quit_bt = tk.Button(self, text= "Quit",font= ("arial", 9), bg= "#FA5F55", relief= tk.RIDGE, command= quit)      # quit button
        self.help_bt = tk.Button(self, text= "Help",font= ("arial", 9), bg= "#FA5F55", relief= tk.RIDGE, command= lambda : self.Help())      # help button

        # Widegets alignment 
        self.flames_label.place(x = 200, y = 30)
        self.partner_label.place(x = 330, y = 180)
        self.name_label.place(x = 200, y = 199 )
        self.input_box.place(x = 244, y= 200)
        self.process_bt.place(x= 486,y = 197)
        self.relation_label.place(x = 244, y = 230)
        self.quit_bt.place(x = 330, y = 350)
        self.help_bt.place(x = 370, y = 350)

# Algorithm was copied from: https://www.geeksforgeeks.org/python-program-to-implement-simple-flames-game/
    def remove_match_char(self,list1, list2):
        """
        Remove a common character and return a list with a list and a flag value.

        Parameters:
        -----------
        list1:(list)
            A list containing characters of a name.
        list2:(list)
            A list containing characters of a name.

        Return:
        -------
            A list with a nested list and a flag value(boolean).
        """

        for i in range(len(list1)) :
            for j in range(len(list2)) :

                if list1[i] == list2[j] :
                    c = list1[i]
                    list1.remove(c)
                    list2.remove(c)

                    list3 = list1 + ["*"] + list2
                    return [list3, True]

        list3 = list1 + ["*"] + list2
        return [list3, False]

    def flames(self, p1_list, p2_list):
        """
        Finds the relationship status and display the status to the user.

        Parameters:
        -----------
        p1_list:(list)
            A list containing characters of a name.
        p2_list:(list)
            A list containing characters of a name.

        Return:
        -------
            None
        """

        proceed = True        
        while proceed :

            ret_list = self.remove_match_char(list(p1_list), list(p2_list))

            con_list = ret_list[0]
            proceed = ret_list[1]
            star_index = con_list.index("*")
            p1_list = con_list[ : star_index]
            p2_list = con_list[star_index + 1 : ]

        count = len(p1_list) + len(p2_list)

        result = ["Friends", "Love", "Affection", "Marriage", "Enemy", "Siblings"]

        while len(result) > 1 :

            split_index = (count % len(result) - 1)
            
            if split_index >= 0 :
                right = result[split_index + 1 : ]
                left = result[ : split_index]
                result = right + left
            else :
                result = result[ : len(result) - 1]

        print("Relationship status :", result[0])       # test code
        self.relation_label.configure(text= f"You're relationship status: {result[0]}")

    def reset(self)-> None:
        """
        Reset to the initial state of the game.

        Parameters:
        -----------

        self:object
            An object of class FlamesApp()

        Returns:
        --------
            None
        """

        self.input_box.configure(state= tk.NORMAL)
        self.process_bt.configure(text= "Enter")
        self.partner_label.configure(text= partner_1)
        self.partners_names.clear()
        self.reset_status = False
        self.relation_label.configure(text= "")
        

    def name(self)-> None:
        """
        Get the valid input strings(i.e. names) and call the flames method.

        Parameters:
        -----------

        self:object
            An object of class FlamesApp()

        Returns:
        --------
            None
        """

        try:
            name = str(self.input_box.get()).replace(" ", "").lower()
            assert name.isalpha()
            self.input_box.delete(0, tk.END)
            print(name)     # test code
            self.partners_names.append(name)
        
            if len(self.partners_names) == 1:
                self.partner_label.configure(text= partner_2)
            elif len(self.partners_names) == 2:
                self.flames(self.partners_names[0], self.partners_names[1])
                self.process_bt.configure(text= "reset")
                self.input_box.configure(state= tk.DISABLED)
                self.reset_status = True
        except AssertionError:
            msg_box.showwarning(title= "Warning: Invalid input", message= "1.Use only aplphabets\n2. Avoid special characters like fullstop('.')\n2. Don't leave blank")

    def process(self):
        """
        Call a function based on reset status.

        Parameters:
        -----------

        self:object
            An object of class FlamesApp()

        Returns:
        --------
            None
        """

        if self.reset_status == False:
            self.name()
        elif self.reset_status == True:
            self.reset()
    
    def Help(self):
        """
        Open the help website of the game.

        Parameters:
        -----------

        self:object
            An object of class FlamesApp()

        Returns:
        --------
            None
        """

        try:
            urlopen(wiki_link, timeout= 1)    # TO check the internet connectivity.
            wb.open(wiki_link, new= 2)
        except URLError:
            msg_box.showwarning(message= "Check you're connected to a network", title= "Warning:Connectivity issue found")
        except ValueError:
            msg_box.showwarning(message= "No Such website found", title= "Warning: Site not found")

# Drive code
if __name__== "__main__":
    app = FlamesApp()
    app.mainloop()
