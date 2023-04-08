from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
import datetime
import csv
import tkinter as ttk

ver = 'v1.7'
appName = 'SkinnyVision'
appTitle = f'{appName} {ver}'
path = "C:\Program Files\FatTrac\data/"

root = Tk()
root.title(appTitle)
root.geometry("500x920")

# Define lists for goals, weights, dates.
goals = []
dates = []
weights = []

# Open image db file and create list.
images = []
imgs = open(f'{path}images.txt', 'r')
im = imgs.readlines()

for i in im:
    images.append(i.replace("\n", ""))
imgs.close()

def update_files(new_dl, new_current, new_goal):
    """
    Write new values to file and re-draw graph.
    """
    with open(f'{path}data.csv', mode='a', newline='') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([new_goal, new_dl, new_current])

def i_mage(xps):
    """
    Change picture based' upon progress.
    """
    img = images[0]
        
    if xps >= 20:
        img = images[1]
    if xps >= 40:
        img = images[2]
    if xps >= 60:
        img = images[3]
    if xps >= 80:
        img = images[4]
    if xps == 100:
        img = images[5]

    mimage = ImageTk.PhotoImage(Image.open(img))
    myImage = Label(root, image=mimage)
    myImage.photo = mimage
    myImage.grid(row=1, rowspan=4, column=2)

def last_60_weights(weights):
    y = weights[-60:]
    return y

def draw_graph_60():
    """
    Draw graph for last 60 days.
    """
    try:
        fig = Figure(figsize = (5, 2.5), dpi = 100)
        y = last_60_weights(weights) # weights
        # x = last_60_dates(dates) #dates.
        plot1 = fig.add_subplot(111)
        plot1.plot(y)
    
        # Create the Tkinter canvas.
        canvas = FigureCanvasTkAgg(fig, master = root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=7, columnspan=4)   
    
    except IndexError:
        draw_graph()

def draw_graph():
    """
    Draw graph.
    """
    fig = Figure(figsize = (5, 2.5), dpi = 100)
    y = weights
    x = dates
    plot1 = fig.add_subplot(111)
    plot1.plot(y)
    
    # Create the Tkinter canvas.
    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=8, columnspan=4)

def days_delta(dates):
    """
    Calculate the number of days since first record.
    """
    try:
        du = dates[0]
        d1 = datetime.datetime.strptime(du, '%m/%d/%y').date() 
        dc = dates[-1]
        da = datetime.datetime.strptime(dc, '%m/%d/%y').date() 
        delta = da - d1
        days = delta.days
    except IndexError:
        days = 0
    return days

def days_to_goal(goals, weights, days):
    """
    Calculate the number of days to reach goal at current rate.
    """
    try:
        goal = goals[-1]
    except IndexError:
        print('Index error goals')
    try:
        current = weights[-1]
    except IndexError:
        print('Index Error weights')

    try:
        cl = weights[0] - weights[-1]
        daily = cl / days
        tg = int(current) - int(goal)
        dtg = tg / daily
        dtg = int(dtg)
    except IndexError:
        print('Index Error')
        dtg = 0
    except ZeroDivisionError:
        print('ZeroDivisionError')
        dtg = 0
    return dtg

def daily_loss(weights, days):
    """
    Calculate the amount of weight lost per day
    """
    try:
        cl = weights[0] - weights[-1]
        daily = cl / days
    except IndexError:
        print('Index Error')
        daily = 0
    except ZeroDivisionError:
        print('ZeroDivisionError')
        daily = 0
    return daily

def get_xps(weights, goal):
    """
    Calculate percentage lost towards goal.
    """
    cl = weights[0] - weights[-1]
    progress = weights[0] - int(goal) 
    xp = cl / progress
    xps = xp * 100
    xps = int(xps)
    return xps

def update():
    """
    main function that updates data and visualizations.
    """
    # Get new variables from inputs.
    new_dl = e.get()
    new_current = float(e1.get())
    new_goal = e2.get()

    # Update csv file,
    update_files(new_dl, new_current, new_goal)

    # Append lists
    goals.append(new_goal)
    weights.append(new_current)
    dates.append(new_dl)

    # Get starting and new date and calculate total days.
    days = days_delta(dates)

    # Calculate days to reach goal.
    dtg = days_to_goal(goals, weights, days)

    # Re-calculate amount lost per day and percentage towards goal.
    goal = new_goal
    xps = get_xps(weights, goal)

    # Display current goal weight or null value if not set.
    myLabel8 = Label(root, text=f"Goal Weight", font=("Arial", 11))
    myLabel8.grid(row=1, column=3, padx=5, pady=0)
    myLabel9 = Label(root, text=f"{new_goal}", font="bold")
    myLabel9.grid(row=2, column=3, padx=5, pady=5)

    # Refresh projected time to reach goal as number of days.
    myLabel10 = Label(root, text=f"Days to reach goal", font=("Arial", 11))
    myLabel10.grid(row=3, column=3, padx=5, pady=0)
    myLabel11 = Label(root, text=f"   {dtg}   ", font="bold")
    myLabel11.grid(row=4, column=3, padx=5, pady=5)
    
    daily = daily_loss(weights, days)

    # Display the average amount lost per day and the total number of days since first record.
    try:
        dail = "{:.2f}".format(daily)
    except UnboundLocalError:
        dail = 'Null'
    myLabel12 = Label(root, 
        text=f"{dail} average pounds lost per day over the last {days} days.", 
        font=("Arial", 12))
    myLabel12.grid(row=9, columnspan=4, pady=10)

    # Display percentage of weight lost towards goal so far,
    myLabel13 = Label(root, text=f"    You are {xps}% towards your goal!    ", 
        font=("Arial", 14))
    myLabel13.grid(row=5, columnspan=4, pady=25)

    # Call img function.
    i_mage(xps)

    # Draw 30 day graph.
    draw_graph_60()

    # Call draw graph function.
    draw_graph()

    # Display last entry date.
    last = dates[-1]
    myLabel15 = Label(root, text=f"Last updated {last}", 
    font=("Arial", 10))
    myLabel15.grid(row=6, columnspan=4, pady=5)
    return(goals, weights, dates)

# Get current date.
dn = datetime.datetime.now()
d = dn.date()
dl = d.strftime("%x")

# Open csv file and create lists and variables
with open(f'{path}data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        goals.append(row[0])
        dates.append(row[1])
        weights.append(row[2])

goals = [eval(i) for i in goals]
try:
    goal = goals[-1]
except IndexError:
    print('Index error goals')

weights = [eval(i) for i in weights]
try:
    current = weights[-1]
except IndexError:
    print('Index Error weights')

# Get starting and ending dates and calculate total days.
days = days_delta(dates)

# Calculate days to reach goal.
dtg = days_to_goal(goals, weights, days)

# Calculate total weight loss, amount lost per day and percentage towards goal.
xps = get_xps(weights, goal)

# Call image function.
i_mage(xps)

# Draw 30 day graph.
draw_graph_60()

# Call draw graph function.
draw_graph()

# Display title header.
myLabel = Label(root, text=appName, fg="dark blue", 
    borderwidth=2, pady=10, font=("Arial", 20))
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

# Save and refresh display.
myButton = Button(root, text='Submit', padx=10, bg="light gray", command=update)
myButton.grid(row=4, column=1, padx=5, pady=5)

daily = daily_loss(weights, days)

try:
    dail = "{:.2f}".format(daily)
    myLabel12 = Label(root, 
        text=f"{dail} average pounds lost per day over the last {days} days.", 
        font=("Arial", 12))
except NameError:
    myLabel12 = Label(root, 
    text=f"Null average pounds lost per day over the last Null days.", 
    font=("Arial", 12))
myLabel12.grid(row=9, columnspan=4, pady=10)

# Display percentage of weight lost towards goal so far.
try:
    xps = get_xps(weights, goal)
    myLabel13 = Label(root, text=f"You are {xps}% towards your goal!", 
        font=("Arial", 14))
    myLabel13.grid(row=5, columnspan=4, pady=25)
except IndexError:
    myLabel13 = Label(root, text=f"You are Null% towards your goal!", 
        font=("Arial", 14))
    myLabel13.grid(row=5, columnspan=4, pady=25)

# Display last entry date.
last = dates[-1]
myLabel15 = Label(root, text=f"Last updated {last}", 
    font=("Arial", 10))
myLabel15.grid(row=6, columnspan=4, pady=5)

root.mainloop()