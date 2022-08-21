from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
import datetime
import pandas
import csv

root = Tk()
root.title('FatTrac Weight Tracker Pro')
root.geometry("500x600")

# Variables, lists, dictionaries.   
img = Image.open("Y:/Jeromy/PythonProjects/FatTrack/images/fatman150.png")
image = ImageTk.PhotoImage(img)

def update():
    """
    Write new values to csv
    """
    new_dl = e.get()
    new_current = e1.get()
    new_current = int(new_current)
    new_goal = e2.get()

    #print(new_dl, new_current, new_goal)
    updates = new_dl, new_current, new_goal
    Weights.append(new_current)

    with open('Y:\Jeromy\PythonProjects\FatTrack\data\weights.csv', 'a') as f:
        writer = csv.writer(f)
        #writer.writerow(updates)

    # Insert graph
    fig = Figure(figsize = (5, 3), dpi = 100)
    y = Weights
    x = dates
    plot1 = fig.add_subplot(111)
    plot1.plot(y)
    
    # Creat the Tkinter canvas.
    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=5, columnspan=4, pady=25)

# Get current date.
dn = datetime.datetime.now()
d = dn.date()
dl = d.strftime("%x")

# Open csv and create lists and variables.
colnames = ['date', 'weight', 'goal']
data = pandas.read_csv('Y:\Jeromy\PythonProjects\FatTrack\data\weights.csv', names=colnames)
dates = data.date.tolist()
Weigh = data.weight.tolist()
gl = data.goal.tolist()
Weigh.pop(0)
Weights = [eval(i) for i in Weigh]
gl.pop(0)
goal = gl[0]
current = Weights[-1]

# Calculate avg amount lost per day and extrapolate number of days to reach goal.
dtg = 1011

# Insert graph
fig = Figure(figsize = (5, 3), dpi = 100)
y = Weights
x = dates
plot1 = fig.add_subplot(111)
plot1.plot(y)

# Creat the Tkinter canvas.
canvas = FigureCanvasTkAgg(fig, master = root)
canvas.draw()
canvas.get_tk_widget().grid(row=5, columnspan=4, pady=25)

# Title
myLabel = Label(root, text="FatTrac Weight Tracker Pro", font="bold", fg="dark blue", borderwidth=2, pady=10)
myLabel.grid(row=0, columnspan=4, padx=5, pady=20)

# Display current goal weight or null value if not set.
myLabel = Label(root, text=f"Goal Weight")
myLabel.grid(row=1, column=3, padx=5, pady=0)
myLabel5 = Label(root, text=f"{goal}", font="bold")
myLabel5.grid(row=2, column=3, padx=5, pady=5)

# Display projected time to reach goal as number of days.
myLabel1 = Label(root, text=f"Days to reach goal")
myLabel1.grid(row=3, column=3, padx=5, pady=0)
myLabel6 = Label(root, text=f"{dtg}", font="bold")
myLabel6.grid(row=4, column=3, padx=5, pady=5)

# Take inputs of weight, goal, and date.
myLabel2 = Label(root, text="Enter date: ")
myLabel2.grid(row=1, column=0, padx=5, pady=5)
e = Entry(root, width=20, bg="light gray")
e.grid(row=1, column=1, padx=5, pady=5)
e.insert(0,f"{dl}")

myLabel3 = Label(root, text="Enter weight: ")
myLabel3.grid(row=2, column=0, padx=5, pady=5)
e1 = Entry(root, width=20, bg="light gray")
e1.grid(row=2, column=1, padx=5, pady=5)
e1.insert(0,f"{current}")

myLabel4 = Label(root, text="Enter new goal: ")
myLabel4.grid(row=3, column=0, padx=5, pady=5)
e2 = Entry(root, width=20, bg="light gray")
e2.grid(row=3, column=1, padx=5, pady=5)
e2.insert(0,f"{goal}")

# Insert fatman image - show skinnier images as progress is made towards goal.
myImage = Label(image=image)
myImage.grid(row=1, rowspan=4, column=2,)

# Insert a quote of my biggest reason for wanting to lose weight.

# Save and refresh display
myButton = Button(root, text='Submit', padx=20, bg="light gray", command=update)
myButton.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()