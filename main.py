BACKGROUND_COLOR = "#B1DDC6"

from tkinter import *
import pandas
import random

window = Tk()
window.title("My first flash card app")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# window.minsize(width=800, height=680)

# pandas 메소드를 이용하는 경우 with open으로 파일을 열 필요 없음.
# word_data = 외부 csv 파일 형태의 dataframe.
try:
    word_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_word_data = pandas.read_csv("data/french_words.csv")
    word_list = original_word_data.to_dict(orient="records")
else:
    word_list = word_data.to_dict(orient="records")

current_card = {}

# ---------functions-------------#
def pick_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(word_list)
    french = current_card["French"]

    # 버튼을 누를 때마다(= pick_rand_card()를 실행시킬 때마다 word_text의 텍스트 내용(config)를 바꾸고 싶으므로.
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=french, fill="black")

    canvas.itemconfig(card_image, image=image_card_front)

    flip_timer = window.after(3000, func=card_flip)

# def clicked_checkmark():
#     word_list.remove(current_card)
#     df = pandas.DataFrame(word_list)
#     df.to_csv("./data/words_to_learn.csv", index=False)

def is_known():
    word_list.remove(current_card)
    pick_card()
    # 체크마크가 눌릴 때마다; is_known() 함수가 실행될 때마다 업데이트 된 csv 데이터 파일이 저장되어야 함.
    df = pandas.DataFrame(word_list)
    df.to_csv("data/words_to_learn.csv", index=False)


def card_flip():
    canvas.itemconfig(card_image, image=image_card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    global current_card
    english = current_card["English"]
    canvas.itemconfig(word_text, text=english, fill="white")



flip_timer = window.after(3000, func=card_flip)

#--------covert to photoimage------------------#
image_card_back = PhotoImage(file="./images/card_back.png")
image_card_front = PhotoImage(file="./images/card_front.png")
image_right = PhotoImage(file="./images/right.png")
image_wrong = PhotoImage(file="./images/wrong.png")
#----------------------------------------------#


canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = canvas.create_image(405,263,image=image_card_front)
title_text =canvas.create_text(400, 150, text="title", fill="black", font=("Arial", 40, "italic"))
word_text =canvas.create_text(400, 263, text="word", fill="black", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


wrong_button = Button(image=image_wrong, highlightthickness=0, command=pick_card)
wrong_button.grid(row=1, column=0)
right_button = Button(image=image_right, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)


pick_card()





window.mainloop()

