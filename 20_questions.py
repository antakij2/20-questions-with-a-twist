#! /usr/bin/env python3

import random
from tkinter import *
from utils import *

# Buttons with a consistent width and text color
class WideButton(Button):
    WIDTH = 18
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, width=self.WIDTH, fg='black', **kwargs)

class App:
    WIDTH = 610
    HEIGHT = 300
    
    START_BLUE = '#99D9EA'
    PADX = round(WIDTH / 32)

    def clear_canvas_and_player_input_area(self):
        self.canvas.delete("all")
        for widget in self.player_input.winfo_children():
            widget.pack_forget()
    
    # If the AI guesses wrong, this constructs the text box into which the player can enter the right answer,
    # as well as the submit button
    def who_was_it(self):
        self.clear_canvas_and_player_input_area()
        self.question_label_text.set("Rats! Who were you thinking of?")
        self.utility_button_text.set("Submit")
        self.utility_button.configure(command=lambda: self.final_message(self.utility_button))
        for widget in [self.entry_frame, self.utility_button]:
            widget.pack(side=LEFT, padx=self.PADX)  
    
    # Display the correct message to the player at the end, according to whether the AI won or lost
    # Also display the "Play again" button
    def final_message(self, caller):
        self.clear_canvas_and_player_input_area()
    
        if caller is self.utility_button:
            self.entry_text.set('')
            message = "Thanks. I'll remember that for next time."
        else:
            message = "I knew it!!!"
            
        self.question_label_text.set(message)
        self.utility_button_text.set("Play again")
        self.utility_button.configure(command=self.reset)
        self.utility_button.pack()
    
    # Choose the next question to ask the player, keeping in mind whether the question is mutually exclusive
    # to others in its QuestionGroup: if yes, then that entire question group is removed from the running. If
    # not, then just the individual question is removed from the running
    def select_next_question(self):
        outer_selection = random.randrange(len(self.all_questions))
        qg = self.all_questions[outer_selection]
        inner_selection = random.randrange(len(qg.group))
        
        if qg.mutually_exclusive:
            core = qg.group[inner_selection]
            self.all_questions.pop(outer_selection)
        else:
            core = qg.group.pop(inner_selection)
            if not qg.group:
                self.all_questions.pop(outer_selection)
        
        return f"{qg.leadup} this person {core}?"
       
    # Display the next message (another question, a final remark, or a guess at the answer) along with any
    # applicable buttons, etc. to the user
    def display_next_message(self):
        if self.current_question == 20:
            self.question_label_text.set(f"{random.choice(answer_intros)}\n{''.join([chr((e-7)//4) for e in self.data])}!")
            self.canvas.create_image(self.WIDTH//2, 0, image=self.background_image, anchor='n') 
            
            self.maybe_button.pack_forget()
            self.yes_button.configure(command=lambda: self.final_message(self.yes_button))
            self.no_button.configure(command=self.who_was_it)
        else:
            self.question_label_text.set(self.select_next_question())
        
        self.current_question += 1
    
    # Reset the questions in the running and all internal state to be ready for a new game
    def reset(self):
        self.all_questions = renew_all_questions()
        self.current_question = 1
        self.display_next_message()
        self.utility_button.pack_forget()
        
        for button in [self.yes_button, self.maybe_button, self.no_button]:
            button.configure(command=self.display_next_message)
            button.pack(side=LEFT, padx=self.PADX)
    
    # Construct GUI, and then listen for user input
    def __init__(self):
        self.data = [283, 439, 451, 447, 135, 315, 475, 467, 435]
    
        self.root = Tk()
        self.root.iconphoto(True, PhotoImage(data=ICON))
        self.root.title("20 Questions: Real People Edition")
        self.root.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        
        # Spacer
        Frame(self.root, height=10).pack()
        
        # AI question area
        self.question_label_text = StringVar()
        self.question_label_text.set("Welcome to 20 Questions!\nThink of a real person, and I'll try to guess who it is!")
        Label(self.root, textvariable=self.question_label_text, font="Helvetica 16 bold", 
                wraplength=round(0.75*self.WIDTH), justify="center", height=3).pack()
        
        # Spacer
        Frame(self.root, height=10).pack()
        
        # Canvas area (when the AI guesses a person, that person's picture will be shown here)        
        self.canvas = Canvas(self.root, height=DIMENSION, width=self.WIDTH) 
        self.canvas.pack()
        
        self.background_image = PhotoImage(data=BACKGROUND)
        
        # Spacer
        Frame(self.root, height=10).pack()
        
        # Player input area (buttons to press; text box to type in the right answer if the AI guesses wrong)
        self.player_input = Frame(self.root)
        
        self.utility_button_text = StringVar()
        self.utility_button_text.set('Play')
        
        self.utility_button = WideButton(self.player_input, textvariable=self.utility_button_text, bg=self.START_BLUE, command=self.reset)
                    
        self.yes_button = WideButton(self.player_input, text='Yes', bg='forest green')
        self.maybe_button = WideButton(self.player_input, text='Maybe', bg='yellow')
        self.no_button = WideButton(self.player_input, text='No', bg='firebrick1')
        
        self.entry_text = StringVar()
        self.entry_frame = Frame(self.player_input)
        entry_label = Label(self.entry_frame, text="Enter a name: ")
        entry = Entry(self.entry_frame, width=WideButton.WIDTH * 2, textvariable=self.entry_text)
        entry_label.pack(side=LEFT)
        entry.pack(side=LEFT)
        
        self.utility_button.pack()
        self.player_input.pack()
        
        
        self.root.mainloop()
        
if __name__ == '__main__':
    App()
    
