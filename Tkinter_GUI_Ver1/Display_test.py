from Pai import originalYama
from Game_action import getFirstHand
import tkinter

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("麻雀（仮）")
    root.resizable(False,False)

    canvas = tkinter.Canvas(root, width=1000, height=800,bg="black")

    s1,s2,s3,s4,yama = getFirstHand(originalYama)
    s1.sort()
    s2.sort()
    s3.sort()
    s4.sort()

    # display player 1 (Upward)
    paths = [p.imgPathU() for p in s1]
    x_cord = 200
    y_cord = 700
    img1 = []
    for path in paths:
       img1.append(tkinter.PhotoImage(file = path))
    for i in img1:
        canvas.create_image(x_cord, y_cord, image=i)
        x_cord += 50

    # display player 2 ((Leftward)
    paths = [p.imgPathL() for p in s2]
    x_cord = 900
    y_cord = 680
    img2 = []
    for path in paths:
       img2.append(tkinter.PhotoImage(file = path))
    for i in img2:
        canvas.create_image(x_cord, y_cord, image=i)
        y_cord -= 50

    # display player 3 ((Downward)
    paths = [p.imgPathD() for p in s3]
    x_cord = 780
    y_cord = 50
    img3 = []
    for path in paths:
       img3.append(tkinter.PhotoImage(file = path))
    for i in img3:
        canvas.create_image(x_cord, y_cord, image=i)
        x_cord -= 50

    # display player 4 ((Rightward)
    paths = [p.imgPathR() for p in s4]
    x_cord = 100
    y_cord = 100
    img4 = []
    for path in paths:
       img4.append(tkinter.PhotoImage(file = path))
    for i in img4:
        canvas.create_image(x_cord, y_cord, image=i)
        y_cord += 50

    canvas.pack()
    root.mainloop()
