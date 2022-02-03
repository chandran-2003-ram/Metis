# Number guessing game
# encoding UTF-8

import tkinter as tk
import random as r
import webbrowser as wb
from tkinter import  messagebox as msg_box
from urllib.request import urlopen
from urllib.error import URLError

__version__ = "v1.1.2"      # revised on 03-02-2022

choose_rand = "   Random number guessing   "
hint_text = "HINT:Enter a random range like\n<integer>-<integer>\nand press range"
valid_int = "HINT:Enter a valid integer!!"
limit_text = "Guess limit: 0"
remain = "Remaining chance: NULL"


class MainApp(tk.Tk):
    """
    This is the main GUI for the game inherited from 'tk.Tk()' class

    Methods:
    --------
    Range(self):
        Get a range for random numbers and generate a
        random number from the range.
    
    reset(self):
        Reset the entire game to intial state.
    
    freeze(self):
        Disable the widgets that are currently active.

    guess(self):
        Get a guess number and find it matches the random
        number or not also provide a hint message and number
        of available chances. If random number matches guess
        number send a "congrats" message until the available
        chances are left else send a "lost the game" message.

    Help(self):
        Open the help website of the game.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # variables for use by methods
        self.count = 0
        self.remaining_chance = 0

        # Root window attributes.
        self.title(f"Random number guessing({__version__})")
        self.configure(bg= "black")
        self.geometry("600x400")
        self.resizable(False, False)
        
        # Widgets get defined here.
        self.intro_label = tk.Label(self,font= "arial"  ,text= choose_rand, background= "black", foreground= "blue")        # Top widget

        self.hint_label = tk.Label(self,font= ("arial", 14)  ,text= hint_text, background= "black", foreground= "blue")     # hint widget

        self.guess_limit_label = tk.Label(self,font= ("arial", 14)  ,text= limit_text, background= "black", foreground= "blue")     # guess limit  widget

        self.remaining_chance_label = tk.Label(self,font= ("arial", 14)  ,text= remain, background= "black", foreground= "blue")    # remaining chance widget

        self.input_box = tk.Entry(self, font= "arial", foreground= "black" , background= "#9099a2")     # Input field 

        self.guess_bt = tk.Button(self, text= "Guess", state= tk.DISABLED, bg= "#f01688",font =("arial",14),fg = "#00b7fa",command = lambda : self.guess())     # Guess button

        self.reset_bt = tk.Button(self, text= "Reset", font= ("arial", 14), bg= "#f01688", fg= "#00b7fa", command= lambda : self.reset())   # Reset button

        self.range_bt = tk.Button(self, text= "Range", font= ("arial", 14), bg= "#f01688", fg= "#00b7fa", command= lambda : self.Range())   # Range button

        self.quit_bt = tk.Button(self, text= "Quit", bg= "#ff2929",font =("arial",14),fg = "#00b7fa",command = quit)    # Quit button

        self.help_bt = tk.Button(self, text= "Help", bg= "#ff2929",font =("arial",8),fg = "#00b7fa",command = lambda : self.Help())    # Help button

        # Alignment if widgets
        self.intro_label.place(x= 150, y = 30)
        self.input_box.place(x= 170, y = 70)
        self.range_bt.place(x= 400, y = 65)
        self.guess_bt.place(x= 475, y = 65)
        self.guess_limit_label.place(x = 140, y = 110)
        self.remaining_chance_label.place(x = 280, y = 110)
        self.hint_label.place(x = 160, y = 150)
        self.reset_bt.place(x = 210, y = 300)
        self.quit_bt.place(x = 280, y = 300)
        self.help_bt.place(x= 265, y= 350)

    def Range(self):
        """
        Get a range for random numbers and generate a
        random number from the range.
        """

        global rand_num, range_, initial_chance
        try:
            temp = self.input_box.get().split(sep="-")
            range_ = (int(temp[0]),int(temp[1]))
            print("Range of numbers:",range_)
            if range_[0]>range_[1]:
                self.hint_label.configure(text= f"HINT: Invalid range=<{range_[0]}>-<{range_[1]}>")
                print("Invalid range:",range_)
            else:
                initial_chance = range_[1]-range_[0]+1
                self.input_box.delete(0,tk.END)
                rand_num = r.randint(range_[0],range_[1])
                self.range_bt.configure(state= tk.DISABLED)
                self.guess_bt.configure(state= tk.ACTIVE)
                self.hint_label.configure(text= f"HINT:Guess a number from\n{range_[0]} to {range_[1]}")
                self.guess_limit_label.configure(text= f"Guess limit: {initial_chance}")
                
                # for use by guess()
                self.remaining_chance = initial_chance 
                self.remaining_chance_label.configure(text= f"Remaining chance: {self.remaining_chance}")
                self.remaining_chance-=1
        except ValueError:
            self.input_box.delete(0,tk.END)
            self.hint_label.configure(text= valid_int)
        except IndexError:
            self.input_box.delete(0,tk.END)
            self.hint_label.configure(text= valid_int)
        else:
            try:
                print("initial_chance:",initial_chance)     # test code
                print("Random number:",rand_num)        # Test code
            except NameError:
                print("range is invalid so no random number is generated")

    def reset(self):
        """ Reset the entire game to intial state. """

        print("Reset to default...")        # test code
        self.count = 0
        self.input_box.delete(0,tk.END)     # input_box
        self.input_box.configure(state= tk.NORMAL)      # input_box
        self.range_bt.configure(state= tk.ACTIVE)       # range button
        self.guess_bt.configure(state= tk.DISABLED)     # guess button
        self.guess_limit_label.configure(text= limit_text)      # guess limit label
        self.remaining_chance_label.configure(text= remain)     # remaining chance label
        self.hint_label.configure(text= hint_text)      # hint label

    def freeze(self):
        """ Disable the widgets that are currently active. """
        self.range_bt.configure(state= tk.DISABLED)
        self.guess_bt.configure(state= tk.DISABLED)
        self.input_box.delete(0, tk.END)
        self.input_box.configure(state= tk.DISABLED)
 
    def guess(self):
        """
        Get a guess number and find it matches the random
        number or not also provide a hint message and number
        of available chances. If random number matches guess
        number send a "congrats" message until the available
        chances are left else send a "lost the game" message.
        """
        if self.remaining_chance > 0:
            try:
                self.remaining_chance_label.configure(text= f"Remaining chance: {self.remaining_chance}")
                self.remaining_chance-=1
                guessed = int(self.input_box.get())
                self.count += 1
                if guessed == rand_num:
                    self.hint_label.configure(text= f"""CONGRATS: You won \U0001F60F \nyou guessed it right in {self.count} guesses. 
    reset to play new game.""")
                    self.freeze()
                elif guessed != rand_num:
                    if guessed < rand_num:
                        self.input_box.delete(0,tk.END)
                        hint = "HINT: the number is too small!!"
                        self.hint_label.configure(text= hint)
                    elif guessed > rand_num:
                        self.input_box.delete(0,tk.END)
                        hint = "HINT: the number is too large!!"
                        self.hint_label.configure(text= hint)
            except ValueError:
                self.input_box.delete(0,tk.END)
                self.hint_label.configure(text= valid_int)
        else:
            self.hint_label.configure(text= "SORRY: you've lost the game,\nexceeded the guess chance\npress reset to play again!!")
            self.remaining_chance_label.configure(text= f"Remaining chance: {self.remaining_chance}")
            self.guess_bt.configure(state= tk.DISABLED)
            self.input_box.configure(state= tk.DISABLED)
            self.input_box.delete(0, tk.END)

    def Help(self):
        """ Open the help website of the game. """
        try:
            urlopen("ssds.com", timeout= 1)    # TO check the internet connectivity.
            wb.open("https://github.com/chandran-2003-ram/Metis/wiki/Number-guessing-Game#how-to-play-the-game", new= 2)
        except URLError:
            msg_box.showwarning(message= "Check you're connected to a network", title= "Warning:Connectivity issue found")
        except ValueError:
            msg_box.showwarning(message= "No Such website found", title= "Warning: Site not found")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
