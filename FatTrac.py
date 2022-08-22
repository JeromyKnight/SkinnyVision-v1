from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
import datetime

root = Tk()
root.title('FatTrac Weight Tracker Pro')
root.geometry("500x600")

img = Image.open("Y:/Jeromy/PythonProjects/FatTrack/weightloss_tracker/images/fatman150.png")
image = ImageTk.PhotoImage(img)

def update():
    """
    Write new values to file and re-draw graph.
    """
    new_dl = e.get()
    new_current = e1.get()
    new_current = int(new_current)
    new_goal = e2.get()

    weights.append(new_current)
    with open('Y:\Jeromy\PythonProjects\FatTrack\weightloss_tracker\data\weights.txt', 'w') as wts:
        for item in weights: 
            wts.write("%s\n" % item)

    dates.append(new_dl)
    with open('Y:\Jeromy\PythonProjects\FatTrack\weightloss_tracker\data\dates.txt', 'w') as dts:
        for item in dates: 
            dts.write("%s\n" % item)

    goals.append(new_goal)
    with open('Y:\Jeromy\PythonProjects\FatTrack\weightloss_tracker\data\goals.txt', 'w') as gts:
        for item in goals: 
            gts.write("%s\n" % item)

    # Re-calculate avg amount lost per day and extrapolate number of days to reach goal.
    d = dates[0]
    d1 = datetime.datetime.strptime(d, '%m/%d/%y').date() 
    dn = datetime.datetime.now()
    da = dn.date()
    delta = da - d1
    days = delta.days
    print(days)

    cl = weights[0] - weights[-1]
    daily = cl / days

    tg = current - int(new_goal)
    dtg = tg / daily
    dtg = int(dtg)

    # Display current goal weight or null value if not set.
    myLabel = Label(root, text=f"Goal Weight")
    myLabel.grid(row=1, column=3, padx=5, pady=0)
    myLabel5 = Label(root, text=f"{new_goal}", font="bold")
    myLabel5.grid(row=2, column=3, padx=5, pady=5)

    # Refresh projected time to reach goal as number of days.
    myLabel1 = Label(root, text=f"Days to reach goal")
    myLabel1.grid(row=3, column=3, padx=5, pady=0)
    myLabel6 = Label(root, text=f"{dtg}", font="bold")
    myLabel6.grid(row=4, column=3, padx=5, pady=5)

    # Insert graph
    fig = Figure(figsize = (5, 3), dpi = 100)
    y = weights
    x = dates
    plot1 = fig.add_subplot(111)
    plot1.plot(y)

    # Insert graph
    fig = Figure(figsize = (5, 3), dpi = 100)
    y = weights
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

# Open txt files and create lists and variables.
goals = []
gl = open('Y:\Jeromy\PythonProjects\FatTrack\weightloss_tracker\data\goals.txt', 'r')
gls = gl.readlines()
for g in gls:
    goals.append(g.replace("\n", ""))
gl.close()
goals = [eval(i) for i in goals]
goal = goals[-1]

dates = []
dt = open('Y:\Jeromy\PythonProjects\FatTrack\weightloss_tracker\data\dates.txt', 'r')
dts = dt.readlines()
for d in dts:
    dates.append(d.replace("\n", ""))
dt.close()

weights = []
weigh = open('Y:\Jeromy\PythonProjects\FatTrack\weightloss_tracker\data\weights.txt', 'r')
wt = weigh.readlines()
for w in wt:
    weights.append(w.replace("\n", ""))
weigh.close()
weights = [eval(i) for i in weights]
current = weights[-1]

# Calculate avg amount lost per day and extrapolate number of days to reach goal.
d = dates[0]
d1 = datetime.datetime.strptime(d, '%m/%d/%y').date() 
dn = datetime.datetime.now()
da = dn.date()
delta = da - d1
days = delta.days
print(days)

cl = weights[0] - weights[-1]
daily = cl / days

tg = current - goal
dtg = tg / daily
dtg = int(dtg)

# Insert graph
fig = Figure(figsize = (5, 3), dpi = 100)
y = weights
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

# Save and refresh display
myButton = Button(root, text='Submit', padx=20, bg="light gray", command=update)
myButton.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()