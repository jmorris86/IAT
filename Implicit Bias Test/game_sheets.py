from tkinter import *
import time


class IatWindow(Tk):

    def __init__(self):
        super().__init__()
        self.title("Implicit Association Test")
        self.maxsize(12000,  10000)


class IatFrame(Frame):
    """Is a Frame object with the relevant labels to insert text, classification objects etc."""
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.width = 12000
        self.height = 10000
        self.grid(row=0, column=0)
        self.config(background="white")
        self.label_left_1 = Label(self, text='Press "E" for', background="white")
        self.label_left_1.grid(row=0, column=0)
        self.label_left_2 = Label(self, text=f"", background="white", font=("Courier", 16),
                                  fg="blue")
        self.label_left_2.grid(row=1, column=0)
        self.label_left_3 = Label(self, text="", background="white")
        self.label_left_3.grid(row=2, column=0)
        self.label_left_4 = Label(self, text="", background="white", font=("Courier", 16), fg="blue")
        self.label_left_4.grid(row=3, column=0)
        self.label_right_1 = Label(self, text='Press "I" for', background="white")
        self.label_right_1.grid(row=0, column=1)
        self.label_right_2 = Label(self, text=f"", background="white", font=("Courier", 16),
                                   fg="blue")
        self.label_right_2.grid(row=1, column=1)
        self.label_right_3 = Label(self, text="", background="white")
        self.label_right_3.grid(row=2, column=1)
        self.label_right_4 = Label(self, text="", background="white", font=("Courier", 16), fg="blue")
        self.label_right_4.grid(row=3, column=1)
        self.label_centre_1 = Label(self, text=f"Part 1 of 7", background="white", padx=0, pady=20)
        self.label_centre_1.grid(row=4, column=0, columnspan=2)
        self.label_centre_2 = Label(self, text=f"", background="white")
        self.label_centre_2.grid(row=5, column=0, columnspan=2)
        self.label_centre_3 = Label(self, text="", background="white")
        self.label_centre_3.grid(row=6, column=0, columnspan=2)
        self.label_centre_4 = Label(self, text=f"Items will appear one at a time.", background="white")
        self.label_centre_4.grid(row=7, column=0, columnspan=2, )
        self.label_centre_5 = Label(self,
                               text=f"If you make a mistake a red X will appear. Press the space bar to continue. Go as"
                                    f" fast as you can whilst being accurate.", background="white", padx=0, pady=20,
                               fg='red')
        self.label_centre_5.grid(row=8, column=0, columnspan=2)
        self.label_centre_6 = Label(self, text=f"Press the space bar when you are ready to start.", background="white")
        self.label_centre_6.grid(row=9, column=0, columnspan=2)
        self.wrong_answer_round_4 = 0
        self.wrong_answer_round_7 = 0
        self.start_time = 0
        self.end_time = 0
        self.time_elapsed_4 = 0
        self.time_elapsed_7 = 0

    def update_labels_info(self, button_config, round_num):
        """Updates the frame to the information required at the start of each round."""
        self.label_centre_1.config(text=f"Part {round_num} of 7")
        self.label_left_2.config(text=button_config(round_num)[0])
        self.label_right_2.config(text=button_config(round_num)[1])
        self.label_centre_2.config(text=f"Put a left finger on 'E' key for items that belong to the category "
                                           f"{button_config(round_num)[0]}.")
        self.label_centre_3.config(text=f"Put a right finger on 'I' key for items that belong to the category "
                                        f"{button_config(round_num)[1]}.", image='', font="TkDefaultFont", fg="black")
        self.label_centre_4.config(text=f"Items will appear one at a time.", background="white")
        self.label_centre_5.config(text=f"If you make a mistake a red X will appear. Press the space bar to continue. "
                                        f"Go as fast as you can whilst being accurate.", fg='red')
        self.label_centre_6.config(text=f"Press the space bar when you are ready to start.", font="TkDefaultFont",
                                   fg="black")
        if round_num in [1, 2, 5]:
            self.label_left_2.config(text=f"{button_config(round_num)[0]}")
            self.label_right_2.config(text=f"{button_config(round_num)[1]}")
            self.label_left_3.config(text=f"")
            self.label_right_3.config(text=f"")
            self.label_left_4.config(text=f"")
            self.label_right_4.config(text=f"")
        elif round_num in [3, 4, 6, 7]:
            self.label_left_2.config(text=f"{button_config(round_num)[0][0]}")
            self.label_right_2.config(text=f"{button_config(round_num)[1][0]}")
            self.label_left_3.config(text=f"or")
            self.label_right_3.config(text=f"or")
            self.label_left_4.config(text=f"{button_config(round_num)[0][1]}")
            self.label_right_4.config(text=f"{button_config(round_num)[1][1]}")

    def update_question(self, status, lookup, item):
        """Updates the frame to an active question screen."""
        self.label_centre_1.config(text=f"")
        self.label_centre_2.config(text=f"")
        self.label_centre_4.config(text="")
        self.label_centre_5.config(text=f"")
        self.label_centre_6.config(text=f"If you make a mistake a red X will appear. Press the space bar to continue.",
                                   fg='red', font=("Courier", 12))
        if status in ["European American", "African American"]:
            self.label_centre_3.config(text=f"", fg='blue', font=("Courier", 30), image=lookup[item])
        else:
            self.label_centre_3.config(text=item, fg='blue', font=("Courier", 30), image='')

    def wrong_answer(self, img, round_num):
        """Used in response to an incorrect answer to update the screen such to show a large cross."""
        self.label_centre_3.config(text=f"", fg='blue', font=("Courier", 30), image=img)
        self.label_centre_6.config(text=f"Press the space bar when you are ready to restart.",
                                    font=("TkDefaultFont", 16),
                                    fg="red")
        if round_num == 4:
            self.wrong_answer_round_4 += 1
        elif round_num == 7:
            self.wrong_answer_round_7 += 1
        else:
            pass

    def timer(self, instruction, round_num):
        """Ultimately performance will be measured by comparing the difference between performance on roudns 4 and 5,
        this simple function calculates how long was taken on each round. The timer is only active while the participant
        is viewing a question - the clock is paused when the participant is on an information screen following a wrong
         answer."""
        if instruction == "start":
            self.start_time = time.time()
        if instruction == "stop":
            if round_num == 4:
                self.time_elapsed_4 += time.time() - self.start_time
            elif round_num == 7:
                self.time_elapsed_7 += time.time() - self.start_time
            else:
                pass
