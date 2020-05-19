from Pai import originalYama
from Game_action import getFirstHand, decideCut
from JudgeRon import Ron
import tkinter
import numpy as np

# this function is our main state
# we wil always back to this function
def displayHands(event):
    global h1,h2,h3,h4
    global state
    # clear the canvas
    canvas.delete("all")
    # display player 1
    paths = [p.imgPathU() for p in h1]
    x_cord = 200
    y_cord = 750
    img1 = []
    for path in paths:
       img1.append(tkinter.PhotoImage(file = path))
    for i in img1:
        canvas.create_image(x_cord, y_cord, image=i)
        x_cord += 50
    # display player 2
    paths = [p.imgPathL() for p in h2]
    x_cord = 900
    y_cord = 680
    img2 = []
    for path in paths:
       img2.append(tkinter.PhotoImage(file = path))
    for i in img2:
        canvas.create_image(x_cord, y_cord, image=i)
        y_cord -= 50
    # display player 3
    paths = [p.imgPathD() for p in h3]
    x_cord = 780
    y_cord = 50
    img3 = []
    for path in paths:
       img3.append(tkinter.PhotoImage(file = path))
    for i in img3:
        canvas.create_image(x_cord, y_cord, image=i)
        x_cord -= 50
    # display player 4
    paths = [p.imgPathR() for p in h4]
    x_cord = 80
    y_cord = 130
    img4 = []
    for path in paths:
       img4.append(tkinter.PhotoImage(file = path))
    for i in img4:
        canvas.create_image(x_cord, y_cord, image=i)
        y_cord += 50

    # check the next stage of game cut or take
    if len(yama) == 0:
        finishGame(None)
        
    if state != "cut":
        button = tkinter.Button(root, text=u'摸牌',width=15)
        button.bind("<Button-1>",takePai)
        button.place(x=400,y=400)
    else:
        button_cut = tkinter.Button(root, text=u'切牌',width=15)
        button_cut.bind("<Button-1>",cutPai)
        button_cut.place(x=400,y=400)

    canvas.pack()
    root.mainloop()

def takePai(event):
    global h1,h2,h3,h4
    global yama
    global turn
    global state

    # using turn to check the current player
    if turn == 0:
        h1 = np.append(h1, yama[0])
        if Ron(h1):
            ronGame()
    elif turn == 1:
        h2 = np.append(h2, yama[0])
        if Ron(h2):
            ronGame()
    elif turn == 2:
        h3 = np.append(h3, yama[0])
        if Ron(h3):
            ronGame()
    else:
        h4 = np.append(h4, yama[0])
        if Ron(h4):
            ronGame()

    yama = yama[1:]   # decrease yama
    state = "cut"     # change state to cut
    displayHands(None)

def cutPai(event):
    global h1,h2,h3,h4
    global yama
    global turn
    global state
    canvas.delete("button")

    # using turn to check the current player
    if turn == 0:
        h1,cut = decideCut(h1)
        h1.sort()
    elif turn == 1:
        h2,cut = decideCut(h2)
        h2.sort()
    elif turn == 2:
        h3,cut = decideCut(h3)
        h3.sort()
    else:
        h4,cut = decideCut(h4)
        h4.sort()

    state = "take"        # change state for next player
    turn = (turn + 1) % 4 # change turn for next player

    # display discarded Pai as button
    button_cut = tkinter.Button(root, text="切牌是"+str(cut),width=15)
    button_cut.bind("<Button-1>",displayHands)
    button_cut.place(x=400,y=400)

def ronGame():
    canvas.clear("all")
    button_cut = tkinter.Button(root, text="和",width=15)
    button_cut.bind("<Button-1>",finishGame)
    button_cut.place(x=400,y=400)

def finishGame(event):
    canvas.clear("all")
    root.mainloop()

if __name__ == "__main__":
    # prepare the things
    h1,h2,h3,h4,yama = getFirstHand(originalYama)
    h1.sort()
    h2.sort()
    h3.sort()
    h4.sort()
    turn = 0
    state = ""

    root = tkinter.Tk()
    root.title("麻雀（仮）")
    root.resizable(False,False)
    canvas = tkinter.Canvas(root, width=1000, height=820, bg="black")

    button_start = tkinter.Button(root, text=u'開始',width=15)
    button_start.bind("<Button-1>",displayHands)
    button_start.place(x=400,y=400)

    canvas.pack()
    root.mainloop()
