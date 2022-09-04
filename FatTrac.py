from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import datetime

root = Tk()
root.title('FatTrac Weight Tracker 5000 Pro')
root.geometry("500x720")

img = Image.open("C:\Program Files\FatTrac/images/fatman150.png")
image = ImageTk.PhotoImage(img)

def update():
    """
    Write new values to file and re-draw graph.
    """
    # Get new variables from inputs.
    new_dl = e.get()
    new_current = e1.get()
    new_current = float(new_current)
    new_goal = e2.get()

    # Open data files and append with new inputs.
    weights.append(new_current)
    with open('C:\Program Files\FatTrac\data\weights.txt', 'w') as wts:
        for item in weights: 
            wts.write("%s\n" % item)

    dates.append(new_dl)
    with open('C:\Program Files\FatTrac\data\dates.txt', 'w') as dts:
        for item in dates: 
            dts.write("%s\n" % item)

    goals.append(new_goal)
    with open('C:\Program Files\FatTrac\data\goals.txt', 'w') as gts:
        for item in goals: 
            gts.write("%s\n" % item)
    
    # Re-calculate avg amount lost per day.
    try:
        d = dates[0]
        d1 = datetime.datetime.strptime(d, '%m/%d/%y').date() 
        dn = datetime.datetime.now()
        da = dn.date()
        delta = da - d1
        days = delta.days
        cl = weights[0] - weights[-1]
        daily = cl / days

        # Remaining weight to lose divided by the avg amount loss so far.
        tg = new_current - int(new_goal)
        dtg = tg / daily
        dtg = int(dtg)
    except ZeroDivisionError:
        dtg = 'Null'
    # Display current goal weight or null value if not set.
    myLabel8 = Label(root, text=f"Goal Weight", font=("Arial", 11))
    myLabel8.grid(row=1, column=3, padx=5, pady=0)
    myLabel9 = Label(root, text=f"{new_goal}", font="bold")
    myLabel9.grid(row=2, column=3, padx=5, pady=5)

    # Refresh projected time to reach goal as number of days.
    myLabel10 = Label(root, text=f"Days to reach goal", font=("Arial", 11))
    myLabel10.grid(row=3, column=3, padx=5, pady=0)
    myLabel11 = Label(root, text=f"{dtg}", font="bold")
    myLabel11.grid(row=4, column=3, padx=5, pady=5)

    try:
        dail = "{:.2f}".format(daily)
    except UnboundLocalError:
        dail = 'Null'
    myLabel12 = Label(root, text=f"{dail} average pounds lost per day over the last {days} days.", font=("Arial", 12))
    myLabel12.grid(row=7, columnspan=4, pady=10)

    # Display percentage of weight lost towards goal so far.
    progress = weights[0] - int(new_goal)
    xp = cl / progress
    xps = xp * 100
    xps = int(xps)

    myLabel12 = Label(root, text=f"    You are {xps}% towards your goal!    ", font=("Arial", 14))
    myLabel12.grid(row=5, columnspan=4, pady=25)

    # Re-draw graph.
    fig = Figure(figsize = (5, 3), dpi = 100)
    y = weights
    x = dates
    plot1 = fig.add_subplot(111)
    plot1.plot(y)
    
    # Create the Tkinter canvas.
    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=6, columnspan=4)   

# Get current date.
dn = datetime.datetime.now()
d = dn.date()
dl = d.strftime("%x")

# Open txt files and create lists and variables.
goals = []
gl = open('C:\Program Files\FatTrac\data\goals.txt', 'r')
gls = gl.readlines()
for g in gls:
    goals.append(g.replace("\n", ""))
gl.close()
try:
    goals = [eval(i) for i in goals]
    goal = goals[-1]
except IndexError:
    print('Index error')
dates = []
dt = open('C:\Program Files\FatTrac\data\dates.txt', 'r')
dts = dt.readlines()
for d in dts:
    dates.append(d.replace("\n", ""))
dt.close()

weights = []
weigh = open('C:\Program Files\FatTrac\data\weights.txt', 'r')
wt = weigh.readlines()
for w in wt:
    weights.append(w.replace("\n", ""))
weigh.close()
weights = [eval(i) for i in weights]
try:
    current = weights[-1]
except IndexError:
    print('Index Error')

# Calculate avg amount lost.
try:
    d = dates[0]
    d1 = datetime.datetime.strptime(d, '%m/%d/%y').date() 
    dn = datetime.datetime.now()
    da = dn.date()
    delta = da - d1
    days = delta.days

    cl = weights[0] - weights[-1]
    daily = cl / days
    tg = current - goal
    dtg = tg / daily
    dtg = int(dtg)
except IndexError:
    print('Index Error')
except ZeroDivisionError:
    print('ZeroDivisionError')

# Insert graph.
fig = Figure(figsize = (5, 3), dpi = 100)
y = weights
x = dates
plot1 = fig.add_subplot(111)
plot1.plot(y)

# Creat the Tkinter canvas.
canvas = FigureCanvasTkAgg(fig, master = root)
canvas.draw()
canvas.get_tk_widget().grid(row=6, columnspan=4)

# Display title header.
myLabel = Label(root, text="FatTrac Weight Tracker 5000 Pro", fg="dark blue", borderwidth=2, pady=10, font=("Arial", 20))
myLabel.grid(row=0, columnspan=4, padx=5, pady=20)

# Display current goal weight or null value if not set.
myLabel1 = Label(root, text=f"Goal Weight", font=("Arial", 11))
myLabel1.grid(row=1, column=3, padx=5, pady=0)
try:
    myLabel2 = Label(root, text=f"{goal}", font="bold")
    myLabel2.grid(row=2, column=3, padx=5, pady=5)
except NameError:
    myLabel2 = Label(root, text=f"Null", font="bold")
    myLabel2.grid(row=2, column=3, padx=5, pady=5)
# Display projected time to reach goal as number of days.
myLabel3 = Label(root, text=f"Days to reach goal", font=("Arial", 11))
myLabel3.grid(row=3, column=3, padx=5, pady=0)
try:
    myLabel4 = Label(root, text=f"{dtg}", font="bold")
except NameError:
    myLabel4 = Label(root, text=f"Null", font="bold")
myLabel4.grid(row=4, column=3, padx=5, pady=5)

# Take inputs of weight, goal, and date.
myLabel5 = Label(root, text="Enter date:", font=("Arial", 11))
myLabel5.grid(row=3, column=0, padx=5, pady=5, sticky="e")
e = Entry(root, width=10, bg="light gray")
e.grid(row=3, column=1, padx=0, pady=5)
e.insert(0,f"{dl}")

myLabel6 = Label(root, text="Enter weight:", font=("Arial", 11))
myLabel6.grid(row=1, column=0, padx=5, pady=5, sticky="e")
e1 = Entry(root, width=10, bg="light gray")
e1.grid(row=1, column=1, padx=0, pady=5)
try:
    e1.insert(0,f"{current}")
except NameError:
    print('NameError')

myLabel7 = Label(root, text="Enter goal:", font=("Arial", 11))
myLabel7.grid(row=2, column=0, padx=5, pady=5, sticky="e")
e2 = Entry(root, width=10, bg="light gray")
e2.grid(row=2, column=1, padx=0, pady=5)
try:
    e2.insert(0,f"{goal}")
except NameError:
    print('NameError')

# Insert fatman image - show skinnier images as progress is made towards goal.
myImage = Label(image=image)
myImage.grid(row=1, rowspan=4, column=2)

# Save and refresh display.
myButton = Button(root, text='Submit', padx=10, bg="light gray", command=update)
myButton.grid(row=4, column=1, padx=5, pady=5)

try:
    dail = "{:.2f}".format(daily)
    myLabel12 = Label(root, text=f"{dail} average pounds lost per day over the last {days} days.", font=("Arial", 12))
except NameError:
    myLabel12 = Label(root, text=f"Null average pounds lost per day over the last Null days.", font=("Arial", 12))
myLabel12.grid(row=7, columnspan=4, pady=10)

# Display percentage of weight lost towards goal so far.
try:
    progress = weights[0] - int(goal)
    xp = cl / progress
    xps = xp * 100
    xps = int(xps)
    myLabel13 = Label(root, text=f"You are {xps}% towards your goal!", font=("Arial", 14))
    myLabel13.grid(row=5, columnspan=4, pady=25)
except IndexError:
    myLabel13 = Label(root, text=f"You are Null% towards your goal!", font=("Arial", 14))
    myLabel13.grid(row=5, columnspan=4, pady=25)
myLabel14 = Label(root, text="Copyright 2022 Jeromy Knight", font=("Arial", 8))
myLabel14.grid(row=8, columnspan=4, pady=10)

root.mainloop()