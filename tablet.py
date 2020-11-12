import tkinter as tk
from PIL import ImageTk, Image
import anki_vector
from tkmacosx import Button

index = 0
img_name = ["you", "go", "stop", "want", "I", "it", "more", "not", "like"]


def next(panel):
    # path = "go.png"
    global index
    if index < len(img_name) - 1:
        index += 1
    path = "images/"+str(img_name[index])+".png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel.configure(image=img)
    panel.image = img  # keep a reference!


def prev(panel):
    global index
    if index > 0:
        index -= 1
    path = "images/"+str(img_name[index])+".png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel.configure(image=img)
    panel.image = img


def select(label):
    stext = label.cget("text") + img_name[index] + " "
    label.config(text=stext)
    print(stext[17:])


def speak(label):
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        stext = label.cget("text")
        robot.behavior.say_text(stext[17:])
        stext = 'vector will say: '
        label.config(text=stext)


def app():
    # Create main window
    window = tk.Tk()
    # divide window into two sections.
    top = tk.Frame(window)
    top.pack(side="top")
    bottom = tk.Frame(window)
    bottom.pack(side="bottom")

    # place string
    slabel = tk.Label(window, text="Vector will say: ",
                      fg="black", relief=tk.FLAT)
    slabel.pack()

    # place image
    #path = ["you", "go", "stop", "want", "I", "it", "more", "not", "like"]
    img = ImageTk.PhotoImage(Image.open("images/"+str(img_name[0])+".png"))
    panel = tk.Label(window, image=img)
    panel.image = img

    # place buttons
    # prev_button = tk.Button(window, text="Previous", width=8,
    #                         height=2, command=lambda: prev(panel))
    # prev_button.pack(in_=top, side="left")
    # panel.pack(in_=top, fill="both", expand="yes", side="left")
    prev_button = Button(window, text='Previous', width=80, height=20, command=lambda: prev(panel))
    prev_button.pack(in_=top, side='left')
    panel.pack(in_=top, fill='both', expand='yes', side='left')


    # next_button = tk.Button(window, text="Next", width=8,
    #                         height=2, command=lambda: next(panel))
    # next_button.pack(in_=top, side="left")
    next_button = Button(window, text='Next', width=80, height=20, command=lambda: next(panel))
    next_button.pack(in_=top, side='right')

    # sele_button = tk.Button(window, text="Select", width=10,
    #                         height=2, command=lambda: select(slabel))
    # sele_button.pack(in_=bottom, side="left")
    sele_button = Button(window, text='Select', width=80, height=20, command=lambda: select(slabel))
    sele_button.pack(in_=bottom, side='left')

    # speak_button = tk.Button(window, text="Speak", width=10,
    #                          height=2, command=lambda: speak(slabel))
    # speak_button.pack(in_=bottom, side="right")
    speak_button = Button(window, text='Speak', width=80, height=20, command=lambda: speak(slabel))
    speak_button.pack(in_=bottom, side='right')

    # Start the GUI
    window.mainloop()


if __name__ == '__main__':
    app()
