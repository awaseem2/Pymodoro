from tkinter import *
import math
from enum import Enum
from turtle import window_width


# TODO
# - [Done] Change buttons to be more aesthetic (use image?)
# - [Done] move these buttons.... also can they just be images lol
# - [Done] create pause button
# - [Done] add plus button which adds at bottom with selected_time
# - [Done] chain events
# - [Done] Move queue over on deletion
# - make timer a visual timer rather than coundown on start
# - play noise on time ending

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Courier"

timer = None
curr_time = 0

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

queue = []
queue_buttons = []
QUEUE_INIT_X = 0
QUEUE_INIT_Y = 325
QUEUE_LENGTH = 140
QUEUE_SPACE = 30
QUEUE_TEXT_SPACE = 15
QUEUE_ACTION_Y = 410
QUEUE_TIME_Y = 455

class QueueInfo:
    def __init__(self, rectangle, action_label, time_label, time, x_coord):
        self.rectangle = rectangle
        self.action_label = action_label
        self.time_label = time_label
        self.time = time
        self.x_coord = x_coord


class Labels():
    WORK = "Work"
    BREAK = "Break"
    MEETING = "Meeting"
    FOOD = "Food"
    STRETCH = "Stretch"


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global selected_time, queue, PAUSE_TIMER, curr_time
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Pymodoro Customizable Timer")
    selected_time = 0
    curr_time = 0
    PAUSE_TIMER = False
    while True:
        res = pop_queue()
        if not res:
            break

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global PAUSE_TIMER, curr_time
    PAUSE_TIMER = False
    if len(queue_buttons) == 0:
        print("Error: add to queue before starting timer")
        return
    if curr_time == 0:
        curr_time = queue_buttons[0].time
    current_action = queue_buttons[0].action_label.cget("text")
    labels(current_action)
    count_down()

def pause_timer():
    global PAUSE_TIMER
    PAUSE_TIMER = True
    animate_pause(0)

def animate_pause(pause_cnt):
    global PAUSE_TIMER, curr_time
    if not PAUSE_TIMER or curr_time == 0:
        return

    count_min = math.floor(curr_time / 60)
    if count_min < 10:
        count_min = f"0{count_min}"
    count_sec = curr_time % 60
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
    global curr_time, timer, PAUSE_TIMER, canvas
    if PAUSE_TIMER:
        return
    count_min = math.floor(curr_time / 60)
    if count_min < 10:
        count_min = f"0{count_min}"
    count_sec = curr_time % 60
    # Dynamic typing allows for changing the data type of a variable
    # Just by assigning it to a different kind of value
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if curr_time > 0:
        curr_time -= 1
        timer = window.after(1000, count_down)
    elif curr_time == 0:
        # delete from queue
        info = queue_buttons[0]
        deleted_x = info.x_coord
        pop_queue()
        # start next queue if exists
        if len(queue_buttons) != 0:
            # shift queue over
            for idx, button in enumerate(queue_buttons):
                distance = QUEUE_LENGTH + QUEUE_SPACE
                space = 0 if idx == 0 else QUEUE_SPACE
                new_x = deleted_x - QUEUE_LENGTH + space + QUEUE_TEXT_SPACE
                button.action_label.place(x=new_x, y=QUEUE_ACTION_Y)
                button.time_label.place(x=new_x, y=QUEUE_TIME_Y)
                canvas.move(button.rectangle, distance * -1, 0)
                button.x_coord = deleted_x
                deleted_x = deleted_x + QUEUE_LENGTH
                
            curr_time = queue_buttons[0].time
            current_action = queue_buttons[0].action_label.cget("text")
            labels(current_action)
            count_down()
        else:
            reset_timer()

def add_time(interval):
    global selected_time
    selected_time += interval
    count_min = math.floor(selected_time / 60)
    if count_min < 10:
        count_min = f"0{count_min}"
    count_sec = selected_time % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

def subtract_time(interval):
    global selected_time
    selected_time = max(0, selected_time - (interval * 60))
    count_min = math.floor(selected_time / 60)
    if count_min < 10:
        count_min = f"0{count_min}"
    count_sec = selected_time % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

def change_bg_color(bg_color, action_color):
    global current_bg, current_action_color, canvas, title_label, action_buttons
    current_bg = bg_color
    current_action_color = action_color
    window.config(bg=bg_color)
    canvas.config(bg=bg_color)
    title_label.config(bg=bg_color, text=current_action)
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

# ---------------------------- INTERVAL MECHANISM ------------------------------- # 

def pop_queue():
    if len(queue_buttons) == 0:
        return False

    info = queue_buttons[0]
    info.time_label.destroy()
    canvas.delete(info.rectangle)
    info.action_label.destroy()
    queue_buttons.pop(0)
    return True

def add_to_queue():
    global queue, current_action_color
    if selected_time == 0:
        return
    # add current action to queue
    queue.append((current_action, selected_time))
    # add a canvas
    last_x = QUEUE_INIT_X if len(queue_buttons) == 0 else queue_buttons[-1].x_coord
    curr_x = last_x + QUEUE_SPACE
    queue_button = canvas.create_rectangle(curr_x, QUEUE_INIT_Y, curr_x + QUEUE_LENGTH, QUEUE_INIT_Y + QUEUE_LENGTH, fill=current_action_color, outline="")
    queue_action = Label(text=current_action, fg=title_color, bg=current_action_color, font=(FONT_NAME, 20), justify="left")
    text_x = curr_x + QUEUE_TEXT_SPACE
    queue_action.place(x=text_x, y=QUEUE_ACTION_Y)
    # TODO: change selected_time to be readable
    queue_time = Label(text=str(selected_time), fg=title_color, bg=current_action_color, font=(FONT_NAME, 15), justify="center")
    queue_time.place(x=text_x, y=QUEUE_TIME_Y)
    info = QueueInfo(queue_button, queue_action, queue_time, selected_time, curr_x + QUEUE_LENGTH)
    queue_buttons.append(info)


def labels(action):
    global current_action
    current_action = action

    if action == "Work":
        change_bg_color(WORK_BACKGROUND_COLOR, WORK_ACTION_CTR_COLOR)
    elif action == "Break":
        change_bg_color(BREAK_BACKGROUND_COLOR, BREAK_ACTION_CTR_COLOR)
    elif action == "Food":
        change_bg_color(FOOD_BACKGROUND_COLOR, FOOD_ACTION_CTR_COLOR)
    elif action == "Meeting":
        change_bg_color(MEETING_BACKGROUND_COLOR, MEETING_ACTION_CTR_COLOR)
    elif action == "Stretch":
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
current_action = "Work"
window.config(padx=50, pady=30, bg=current_bg)
title_label = Label(text="Pymodoro Customizable Timer", fg=title_color, bg=current_bg, font=(FONT_NAME, 30), justify="left", anchor="w")
title_label.grid(column=0, row=0, columnspan=2, sticky='ew')
canvas = Canvas(width=1000, height=500, bg=current_bg, highlightthickness=0)
action_ctr = canvas.create_rectangle(250, 35, 700, 270, fill=current_action_color, outline="")
selected_time = 0
timer_text = canvas.create_text(475, 150, text="00:00", fill="white", font=(FONT_NAME, 40, "bold"))
canvas.grid(column=1, row=1)

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

# add / subtract selected_time buttons
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
next_img = PhotoImage(file="next_button.png")
next_img = next_img.subsample(ACTION_BUTTON_SCALE)
next_button = Button(command = add_to_queue, image=next_img)
next_button.place(x=655, y=INTERVAL_HEIGHT)
interval_buttons.extend([plus, subtract, big_plus, big_subtract, next_button])

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




