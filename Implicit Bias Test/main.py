from game_sheets import *
from PIL import ImageTk, Image
import random
"""Provides code for a IAT in respect of racial preferences. Built in GUI, is intended as a aid for the researchers who 
will ultimately build a web-based solution."""
item = ""
status = ""
item_count = 1
round_num = 1
number_questions = 20
info_screen = "yes"
answer_screen = "no"
reset_screen = "no"
photo_location = "Harvard IBT - Pics"
words = {
	'Good': ["Adore", "Appealing", "Attractive", "Cheer", "Excellent", "Friend", "Friendship", "Joyful", "Joyous",
			 "Lovely", "Magnificent", "Smiling", "Terrific"],
	'Bad': ["Abuse", "Awful", "Disaster", "Despise", "Dirty", "Disgust", "Hate", "Horrible", "Hurtful",
			"Nasty", "Poison", "Scorn"]
}
photos = {
	"African American": ["bf1_nc", "bf2_nc", "bf3_nc", "bm1_nc", "bm2_nc", "bm3_nc"],
	"European American": ["wm1_nc", "wm2_nc", "wm3_nc", "wf1_nc",
						  "wf2_nc", "wf3_nc"]
}

# Todo random allocation of characteristics to key e or key i
# round_1_e (i) is the variable allocated to key e (i) in round one. Similarly, round_2_e (i) is the variable allocated
# to key e (i) in round one.
round_1_e = random.choice(["European American", "African American"])
if round_1_e == "European American":
	round_1_i = "African American"
else:
	round_1_i = "European American"
round_2_e = random.choice(["Good", "Bad"])
if round_2_e == "Good":
	round_2_i = "Bad"
else:
	round_2_i = "Good"


def button_config(number):
	"""Based on the original allocation of characteristics to keys, the function determines the key allocation in each
	round"""
	if number == 1:
		e = round_1_e
		i = round_1_i
	elif number == 2:
		e = round_2_e
		i = round_2_i
	elif number in [3, 4]:
		e = round_1_e, round_2_e
		i = round_1_i, round_2_i
	elif number == 5:
		e = round_1_i
		i = round_1_e
	else:
		e = round_1_i, round_2_e
		i = round_1_e, round_2_i
	return [e, i]


def choose_item(number):
	"""Random choice of item for IBT analysis. Rounds 1 and 5 are restricted to photos, round 2 is restricted to words,
	and all other rounds are a random choice of word or picture"""
	if number in [1, 5]:
		# status_1 is the category of object from European American, African American, Good, and Bad. Whereas, thing is
		# the actual object i.e. the photo or the word.
		status_1 = random.choice(list(photos.keys()))
		thing = random.choice(photos[status_1])
	elif number == 2:
		status_1 = random.choice(list(words.keys()))
		thing = random.choice(words[status_1])
	else:
		rand_number = random.randint(0, 1)
		# In rounds where the object can be either a photo or a word, rand_number is used to choose the type of object.
		# Both the object and category of object are chosen as per other rounds.
		if rand_number == 0:
			status_1 = random.choice(list(words.keys()))
			thing = random.choice(words[status_1])
		else:
			status_1 = random.choice(list(photos.keys()))
			thing = random.choice(photos[status_1])
	return thing, status_1


def clear_screen(event=None):
	"""The clear_screen function is triggered when the space bar is pressed. When the participant is on an instruction
	screen at the start of a round, pressing the space bar activates the next round. Whereas, after an incorrect answer,
	pressing the space bar causes the participant to either see another object to classify or navigates them to the next
	round if appropriate. Finally, if the participant is required to categorise an object, the function effectively
	doesn't do anything."""
	global info_screen, item, item_count, status, answer_screen, round_num, reset_screen
	item_of_interest = choose_item(round_num)
	item = item_of_interest[0]
	status = item_of_interest[1]
	if reset_screen == "yes":
		# reset_screen = "yes" only when the participant has incorrectly answered the ultimate question, but they are
		# starting a new round.
		item_count = 1
		round_num += 1
		info_screen = "yes"
		frame.update_labels_info(button_config, round_num)
		if round_num > 7:
			# print to the console that provides information on performance. Once we agree on a performance measure,
			# this information will be stored as a variable and not output to the screen.
			print(f"When {button_config(4)[0][0]} was associated with {button_config(4)[0][1]}, and "
				  f"{button_config(4)[1][0]} was associated with {button_config(4)[1][1]}:\nThe number of wrong "
				  f"answers was {frame.wrong_answer_round_4} and the time taken to complete the round was "
				  f"{round(frame.time_elapsed_4, 2)} seconds\n\nWhereas, when {button_config(7)[0][0]} was associated "
				  f"with {button_config(7)[0][1]}, and {button_config(7)[1][0]} was associated with "
				  f"{button_config(7)[1][1]}:\nThe number of wrong answers was {frame.wrong_answer_round_7} and "
				  f"the time elapsed was {round(frame.time_elapsed_7, 2)} seconds")
			window.destroy()
		reset_screen = "no"
	elif info_screen == "yes":
		answer_screen = "yes"
		info_screen = "no"
		frame.update_question(status, lookup, item)
		frame.timer("start", round_num)
	else:
		pass


def check_answer(event):
	global status, round_num, item_count, item, info_screen, answer_screen, reset_screen
	map_1 = {
		"e": 0,
		"i": 1
	}
	if answer_screen == "yes":
		# triggered if the participant correctly answers the question
		if status in button_config(round_num)[map_1[event.char]]:
			item_of_interest = choose_item(round_num)
			# while loop is deployed to ensure the participant is not required to categorise the same object in
			# subsequent questions.
			while item == item_of_interest[0]:
				item_of_interest = choose_item(round_num)
			item = item_of_interest[0]
			status = item_of_interest[1]
			frame.update_question(status, lookup, item)
		else:
			frame.wrong_answer(wrong_img, round_num)
			frame.timer("stop", round_num)
			info_screen = "yes"
			answer_screen = "no"
			if item_count < number_questions:
				pass
			else:
				# activated when a participant answer incorrectly, but it is the final question of the round. Designed
				# to push the program into the specific clear_screen case.
				reset_screen = "yes"
		if item_count < number_questions:
			item_count += 1
		elif reset_screen == "yes":
			pass
		else:
			item_count = 1
			round_num += 1
			info_screen = "yes"
			frame.update_labels_info(button_config, round_num)
			frame.timer("stop", round_num)
			if round_num > 7:
				print(f"When {button_config(4)[0][0]} was associated with {button_config(4)[0][1]}, and "
					  f"{button_config(4)[1][0]} was associated with {button_config(4)[1][1]}:\nThe number of wrong "
					  f"answers was {frame.wrong_answer_round_4} and the time taken to complete the round was "
					  f"{round(frame.time_elapsed_4, 2)} seconds\n\nWhereas, when {button_config(7)[0][0]} was associated "
					  f"with {button_config(7)[0][1]}, and {button_config(7)[1][0]} was associated with "
					  f"{button_config(7)[1][1]}:\nThe number of wrong answers was {frame.wrong_answer_round_7} and "
					  f"the time elapsed was {round(frame.time_elapsed_7, 2)} seconds")
				window.destroy()

	else:
		pass


window = IatWindow()
frame = IatFrame(window)
frame.update_labels_info(button_config, round_num)
# Todo load pictures required for analysis and to indicate an incorrect answer
wrong_img = PhotoImage(file=f"{photo_location}/wrong.png")
bf1_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/bf1_nc.jpg"))
bf2_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/bf2_nc.jpg"))
bf3_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/bf3_nc.jpg"))
bm1_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/bm1_nc.jpg"))
bm2_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/bm2_nc.jpg"))
bm3_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/bm3_nc.jpg"))
wm1_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/wm1_nc.jpg"))
wm2_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/wm2_nc.jpg"))
wm3_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/wm3_nc.jpg"))
wf1_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/wf1_nc.jpg"))
wf2_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/wf2_nc.jpg"))
wf3_nc = ImageTk.PhotoImage(Image.open(f"{photo_location}/wf3_nc.jpg"))
# dictionary to allow me to load pictures after referring to them via their string name
lookup = {
	"bf1_nc": bf1_nc,
	"bf2_nc": bf2_nc,
	"bf3_nc": bf3_nc,
	"bm1_nc": bm1_nc,
	"bm2_nc": bm2_nc,
	"bm3_nc": bm1_nc,
	"wm1_nc": wm1_nc,
	"wm2_nc": wm2_nc,
	"wm3_nc": wm3_nc,
	"wf1_nc": wf1_nc,
	"wf2_nc": wf2_nc,
	"wf3_nc": wf3_nc,
}
# binding e, i, and space keys to specific functions.
window.bind("<e>", check_answer)
window.bind("<i>", check_answer)
window.bind("<space>", clear_screen)
window.mainloop()
