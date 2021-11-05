import tkinter as tk
from tkinter.filedialog import askopenfilename
from enrich_reviews import main

window = tk.Tk()
frame = tk.Frame()
label = tk.Label(master=frame)

greeting = tk.Label(
    text="Please select a file",
    fg="white",
    bg="#2e282e",
    width=100,
    height=40
)

def fileselect():
    # show an "Open" dialog box and return the path to the selected file
    selected_File = askopenfilename()
    print(selected_File)
    main(selected_File)

button = tk.Button(
    text="Select File",
    width=50,
    height=5,
    bg="#706fbf",
    fg="yellow",
    command=fileselect
)



# Basically loads everything built
greeting.pack()
button.pack()
label.pack()
window.mainloop()
