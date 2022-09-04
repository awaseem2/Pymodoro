from tkinter import *
import math
from enum import Enum
from turtle import window_width


# TODO
# - [Done] Change buttons to be more aesthetic (use image?)
# - [Done] move these buttons.... also can they just be images lol
# - [Done] create pause button
# - add plus button which adds at bottom with time
# - chain events
# - make timer a visual timer rather than coundown on start

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
WORK_BACKGROUND_COLOR = "#d95550"
WORK_ACTION_CTR_COLOR = "#dd6662"
BREAK_BACKGROUND_COLOR = "#4c9195"
BREAK_ACTION_CTR_COLOR = "#5e9ca0"
MEETING_BACKGROUND_COLOR = "#457ca3"
MEETING_ACTION_CTR_COLOR = "#5889ac"
FOOD_BACKGROUND_COLOR = "#f7b05b"
FOOD_ACTION_CTR_COLOR = "#ffc15e"
STRETCH_BACKGROUND_COLOR = "#453750"
STRETCH_ACTION_CTR_COLOR = "#73648a"
title_color = "#ffffff"
SMALL_INTERVAL = 5
BIG_INTERVAL = 20
ACTION_BUTTON_SCALE = 18
PAUSE_TIMER = False

class Labels(Enum):
    WORK = 1
    BREAK = 2
    MEETING = 3
    FOOD = 4
    STRETCH = 5

action_to_label = {
    Labels.WORK: "Work",
    Labels.BREAK: "Break",
    Labels.MEETING: "Meeting",
    Labels.FOOD: "Food",
    Labels.STRETCH: "Stretch",
}

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global time
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Pymodoro Customizable Timer")
    check_marks.config(text="")
    global reps
    reps = 0
    time = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps, PAUSE_TIMER
    PAUSE_TIMER = False
    reps += 1
    if time == 0:
        return
    # If it's the 1st/3rd/5th/7th rep
    if reps % 8 == 0:
        count_down()
        title_label.config(text="Break", fg=RED)
    # If it's the 8th rep
    elif reps % 2 == 0:
        count_down()
        title_label.config(text="Break", fg=PINK)
    # If it's the 2nd/4th/6th rep
    else:
        count_down()
        title_label.config(text=action_to_label[current_action])

def pause_timer():
    global PAUSE_TIMER
    PAUSE_TIMER = True
    animate_pause(0)

def animate_pause(pause_cnt):
    global PAUSE_TIMER, time
    if not PAUSE_TIMER or time == 0:
        return

    count_min = math.floor(time / 60)
    if count_min < 10:
        count_min = f"0{count_min}"
    count_sec = time % 60
    # Dynamic typing allows for changing the data type of a variable
    # Just by assigning it to a different kind of value
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if pause_cnt % 2 == 0:
        canvas.itemconfig(timer_text, text=f"{count_min} {count_sec}")
    else:
        canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    
    window.after(1000, animate_pause, pause_cnt + 1)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down():
    global time, timer, PAUSE_TIMER
    if PAUSE_TIMER:
        return
    count_min = math.floor(time / 60)
    if count_min < 10:
        count_min = f"0{count_min}"
    count_sec = time % 60
    # Dynamic typing allows for changing the data type of a variable
    # Just by assigning it to a different kind of value
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if time > 0:
        time -= 1
        timer = window.after(1000, count_down)
    else:
        # start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✓"
        check_marks.config(text=marks)

def add_time(interval):
    global time
    time += interval * 60
    count_min = math.floor(time / 60)
    if count_min < 10:
        count_min = f"0{count_min}"
    count_sec = time % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

def subtract_time(interval):
    global time
    time = max(0, time - (interval * 60))
    count_min = math.floor(time / 60)
    if count_min < 10:
        count_min = f"0{count_min}"
    count_sec = time % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

def change_bg_color(bg_color, action_color):
    global current_bg, current_action_color, canvas, title_label, action_buttons
    current_bg = bg_color
    current_action_color = action_color
    window.config(bg=bg_color)
    canvas.config(bg=bg_color)
    title_label.config(bg=bg_color, text=action_to_label[current_action])
    canvas.itemconfig(action_ctr, fill=action_color)

    # fix button backgrounds LOL
    for button in action_buttons:
        button.config(bg=action_color, activebackground=current_action_color)
    for button in labels_buttons:
        button.config(bg=action_color, activebackground=current_action_color)
    for button in interval_buttons:
        button.config(bg=action_color, activebackground=current_action_color)

def configure_buttons():
    for button in action_buttons:
        button.config(bg=current_action_color, bd = 0, activebackground=current_action_color, highlightthickness=0)
        # TODO: maybe add highlight?
    for button in labels_buttons:
        button.config(bg=current_action_color, bd=0, activebackground=current_action_color, highlightthickness=0, height=20, width = 55, fg='black', compound="center")
    for button in interval_buttons:
        button.config(bg=current_action_color, bd=0, activebackground=current_action_color, highlightthickness=0, height=28, width = 28, fg='black', compound="center")


def labels(label):
    global current_action
    current_action = label

    if label == Labels.WORK:
        change_bg_color(WORK_BACKGROUND_COLOR, WORK_ACTION_CTR_COLOR)
    elif label == Labels.BREAK:
        change_bg_color(BREAK_BACKGROUND_COLOR, BREAK_ACTION_CTR_COLOR)
    elif label == Labels.FOOD:
        change_bg_color(FOOD_BACKGROUND_COLOR, FOOD_ACTION_CTR_COLOR)
    elif label == Labels.MEETING:
        change_bg_color(MEETING_BACKGROUND_COLOR, MEETING_ACTION_CTR_COLOR)
    elif label == Labels.STRETCH:
        change_bg_color(STRETCH_BACKGROUND_COLOR, STRETCH_ACTION_CTR_COLOR)

    # TODO: add text box and random color

def getorigin(eventorigin):
      global x_coord, y_coord
      x_coord = eventorigin.x
      y_coord = eventorigin.y + 50
      print("mouse location = (" + str(x_coord) + ", " + str(y_coord) + ")")



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pymodoro")
current_bg = WORK_BACKGROUND_COLOR
current_action_color = WORK_ACTION_CTR_COLOR
current_action = Labels.WORK
window.config(padx=50, pady=30, bg=current_bg)
title_label = Label(text="Pymodoro Customizable Timer", fg=title_color, bg=current_bg, font=(FONT_NAME, 30), justify="left", anchor="w")
title_label.grid(column=0, row=0, columnspan=2, sticky='ew')
# Need to check the background colour of the canvas as well
canvas = Canvas(width=1000, height=500, bg=current_bg, highlightthickness=0)
# highlightthicknes is used for making the highlight disappear
# tomato_img = PhotoImage(file="tomato.png")
action_ctr = canvas.create_rectangle(250, 35, 700, 270, fill=current_action_color, outline="")
time = 0
timer_text = canvas.create_text(475, 150, text="00:00", fill="white", font=(FONT_NAME, 40, "bold"))
canvas.grid(column=1, row=1)
# count_down(5)
# x and y values are half of the width and the height

action_buttons = []
start_img = PhotoImage(file="play_button.png")
start_img = start_img.subsample(ACTION_BUTTON_SCALE)
start_button = Button(text="Start", command=start_timer, image=start_img)
start_button.place(x=430, y=270)
reset_img = PhotoImage(file="stop_button.png")
reset_img = reset_img.subsample(ACTION_BUTTON_SCALE)
reset_button = Button(text="Reset", command = reset_timer, image=reset_img)
reset_button.place(x=490, y=270)
pause_img = PhotoImage(file="pause_button.png")
pause_img = pause_img.subsample(ACTION_BUTTON_SCALE)
pause_button = Button(text="Pause", command = pause_timer, image=pause_img)
pause_button.place(x=550, y=270)
action_buttons.extend([start_button, reset_button, pause_button])

# pause button TODO

check_marks = Label(text="✓", fg=title_color, bg=current_bg)
# check_marks.grid(column=1, row=3)

# add / subtract time buttons
interval_buttons = []
interval_img = PhotoImage(file="Rounded_Square.png")
interval_img = interval_img.subsample(20)
INTERVAL_HEIGHT = 180
plus = Button(text="+", command=lambda: add_time(SMALL_INTERVAL), image=interval_img)
plus.place(x=570, y=INTERVAL_HEIGHT)
subtract = Button(text="-", highlightthickness=0, command=lambda: subtract_time(SMALL_INTERVAL), image=interval_img)
subtract.place(x=350, y=INTERVAL_HEIGHT)
big_plus = Button(text="++", highlightthickness=0, command=lambda: add_time(BIG_INTERVAL), image=interval_img)
big_plus.place(x=610, y=INTERVAL_HEIGHT)
big_subtract = Button(text="--", highlightthickness=0, command=lambda: subtract_time(BIG_INTERVAL), image=interval_img)
big_subtract.place(x=310, y=INTERVAL_HEIGHT)
interval_buttons.extend([plus, subtract, big_plus, big_subtract])

# labels for pomodoro
labels_buttons = []
label_img = PhotoImage(file="Rounded_Rectangle.png")
label_img = label_img.subsample(10)
work_button = Button(text="work", command=lambda: labels(Labels.WORK), image=label_img)
work_button.place(x=310, y=120)
break_button = Button(text="break", command=lambda: labels(Labels.BREAK), image=label_img)
break_button.place(x=372, y=120)
meeting_button = Button(text="meeting", command=lambda: labels(Labels.MEETING), image=label_img)
meeting_button.place(x=435, y=120)
food_button = Button(text="food", command=lambda: labels(Labels.FOOD), image=label_img)
food_button.place(x=495, y=120)
stretch_button = Button(text="stretch", command=lambda: labels(Labels.STRETCH), image=label_img)
stretch_button.place(x=555, y=120)
labels_buttons.extend([work_button, break_button, meeting_button, food_button, stretch_button])

configure_buttons()
window.bind("<Button 1>", getorigin)
window.mainloop()




