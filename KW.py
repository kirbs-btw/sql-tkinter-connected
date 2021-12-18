import tkinter as tk
from tkinter import ttk
import sqlite3
import os

def getCompanyList():
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    command = f"SELECT name FROM company"
    companyList = cur.execute(command).fetchall()
    conn.close()
    
    return companyList

def destroyWidget(frame):
     widgets = frame.winfo_children()
     for widget in widgets:
         widget.destroy()
    

def printEmployees(company, frame):
    destroyWidget(frame)
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    companyName = str()
    
    #cuts tring up input is weird
    for i in company:
        if i == "(" or i == ")" or i == "," or i == "'":
            pass
        else:
            companyName = companyName + i
    command = f"SELECT DISTINCT employee.name, employee.lastname, employee.position,employee.experience FROM company, employee WHERE employee.company_id = (SELECT id FROM company WHERE name = '{companyName}')"
    employeeTable = cur.execute(command).fetchall()
    printTable(frame, employeeTable)
    
    conn.close()
        
    pass

def printTable(frame, table):
    print(table)
    f = 0
    for i in table:
        f += 1
        tk.Label(frame, text=i[0], justify="left").grid(row=f, column=1, pady=10, padx=10, sticky="w")
        tk.Label(frame, text=i[1], justify="left").grid(row=f, column=2, pady=10, padx=10, sticky="w")
        tk.Label(frame, text=i[2], justify="left").grid(row=f, column=3, pady=10, padx=10, sticky="w")
        tk.Label(frame, text=i[3], justify="left").grid(row=f, column=4, pady=10, padx=10, sticky="w")
        
def printTableProjects(frame):
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    command = f"SELECT * FROM project"
    table = cur.execute(command).fetchall()
    conn.close()
    f = 0
    for i in table:
        f += 1
        tk.Label(frame, text=i[1], justify="left").grid(row=f, column=1, pady=10, padx=10, sticky="w")
        tk.Label(frame, text=i[2], justify="left").grid(row=f, column=2, pady=10, padx=10, sticky="w")
        tk.Label(frame, text=i[3], justify="left").grid(row=f, column=3, pady=10, padx=10, sticky="w")
        tk.Label(frame, text=i[0], justify="left").grid(row=f, column=4, pady=10, padx=10, sticky="w")
        tk.Button(frame, text = "Choose Project", justify="left", command = lambda m = i[0]: chooseProject(m)).grid(row=f, column=5, pady=10, padx=10, sticky="w")

def chooseProject(projectId):
    
    pass
        
def openProjectsWindow():
    root = tk.Tk()
    
    canvas = tk.Canvas(root, width=750, height=450, bg='#ffffff')
    canvas.pack()
    
    table = tk.Canvas(canvas, bg="black")
    table.place(relwidth=1, relheight=1, anchor='nw')
    # create a main frame
    mainFrame = tk.Frame(table, bg="#ffffff")
    mainFrame.pack(fill='both', expand=1)
    # canvas
    canvas1 = tk.Canvas(mainFrame)
    canvas1.pack(side='left', fill='both', expand=1)
    # scrollbar
    canvScroll = ttk.Scrollbar(mainFrame, orient='vertical', command=canvas1.yview)
    canvScroll.pack(side='right', fill='y')
    # cofig canvas
    canvas1.configure(yscrollcommand=canvScroll.set)
    canvas1.bind('<Configure>', lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))
    # create another frame in canvas
    frameScroll = tk.Frame(canvas1)
    # add fram to window in canvas
    canvas1.create_window((0, 0), window=frameScroll, anchor="nw")
    
    printTableProjects(frameScroll)
    
    root.mainloop()

def mainWindow():
    root = tk.Tk()
    root.title("[KW]")
    root.iconbitmap("gui/kw.ico")

    #images
    refreshImg = tk.PhotoImage(file='gui/refresh.png')
    kw = tk.PhotoImage(file='gui/kw.png')


    canvas = tk.Canvas(root, width=750, height=750, bg='#ffffff')
    canvas.pack()

    kwButton = tk.Button(canvas, image=kw, borderwidth=0, command=lambda: passwordDev(), bg='#ffffff')
    kwButton.place(relx=0.9, rely=0.05, relwidth=0.048, relheight=0.048, anchor="nw")

    canvas.create_text(130, 185, text="Angestellten Tabelle", font=(None, 15), anchor="n")


    refreshButton = tk.Button(canvas, image=refreshImg, borderwidth=0, bg='#ffffff', command = lambda: printEmployees(selectedCompany.get(), frameScroll))
    refreshButton.place(relx=0.5, rely=0.15, relwidth=0.048, relheight=0.048, anchor="nw")

    # drop down employee#####################
    # bsp list eig list wird abfrage einer sql tabelle
    projectsWindowButton = tk.Button(canvas, command = lambda: openProjectsWindow(), text = "Choose project") 
    projectsWindowButton.place(relx=0.275, rely=0.15, relwidth=0.2, relheight=0.05, )
    #############################################################

    #drop down Firma#####################
    #bsp list eig list wird abfrage einer sql tabelle
    #companyList = lib-kw.getCompanies()
    companyList = getCompanyList()
    
    #Variable, die immer der gleichen Wert haben soll, wie das, was im Menü ausgewählt ist
    selectedCompany = tk.StringVar(canvas)
    selectedCompany.set(companyList[0])

    #Hier kommt das eigentliche Menü, wird mit dem fenster und der Variable ausgewaehlt verknüpft
    companyDropdown = tk.OptionMenu(root, selectedCompany, *companyList)
    companyDropdown.place(relx = 0.05, rely=0.15, relwidth=0.2, relheight=0.05)

    #############################################################


    #### scrollbar stuff#############################
    table = tk.Canvas(canvas, bg="black")
    table.place(relx=0.05, rely=0.3, relwidth=0.9, relheight=0.3, anchor='nw')
    # create a main frame
    mainFrame = tk.Frame(table, bg="#ffffff")
    mainFrame.pack(fill='both', expand=1)
    # canvas
    canvas1 = tk.Canvas(mainFrame)
    canvas1.pack(side='left', fill='both', expand=1)
    # scrollbar
    canvScroll = ttk.Scrollbar(mainFrame, orient='vertical', command=canvas1.yview)
    canvScroll.pack(side='right', fill='y')
    # cofig canvas
    canvas1.configure(yscrollcommand=canvScroll.set)
    canvas1.bind('<Configure>', lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))
    # create another frame in canvas
    frameScroll = tk.Frame(canvas1)
    # add fram to window in canvas
    canvas1.create_window((0, 0), window=frameScroll, anchor="nw")
    ##############################################################


    #add mitarbeiter
    #angaben inputs
    
    #mitarbeiter projekte zuweisen
    
    #project dropdown
    
    #project start
    
    
    #allgemeine abragen - dev menu
    
    printEmployees(selectedCompany.get(), frameScroll)
    
    root.mainloop()

def login(entry, root):
    password = "kw"
    
    if entry == password:
        root.destroy()
        devWindow()
        
    else:
        print("wrong password")
        
        
#######################################
# Password check for development window
#######################################

def passwordDev():
    root = tk.Tk()
    root.title("Password")
    root.iconbitmap("gui/kw.ico")
    
    canvas = tk.Canvas(root, width=300, height=150)
    canvas.pack()
    
    canvas.create_text(57.5, 50, text="password", font=(None, 10), anchor="n")
    
    passwordInput = tk.Entry(canvas)
    passwordInput.place(relx = 0.1, rely = 0.45)
    
    loginButton = tk.Button(canvas, text = "login",command = lambda: login(passwordInput.get(), root))
    loginButton.place(relx = 0.6, rely = 0.45)
    
    
    root.mainloop()

def executeSqlCommand(command):
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    table = cur.execute(command).fetchall()
    conn.commit()
    conn.close()
    print(table)
    pass

def devWindow():
    root = tk.Tk()
    root.title("[KW]")
    root.iconbitmap("gui/kw.ico")

    canvas = tk.Canvas(root, width=750, height=750)
    canvas.pack()

    canvas.create_text(375, 75, text="Eingaben", font=(None, 25), anchor="n")
    
    executeButton = tk.Button(canvas, borderwidth=0, text = "okookokokokokokok", bg='#ffffff', command = lambda: executeSqlCommand(commandInput.get()))
    executeButton.place(relx = 0.05, rely=0.2, relwidth=0.5, relheight=0.03)
    
    commandInput = tk.Entry(canvas)
    commandInput.place(relx = 0.05, rely=0.25, relwidth=0.5, relheight=0.03)
    
    
    root.mainloop()






if __name__ == '__main__':
    mainWindow()
    #mainWindow()
    
    # password to dev Window is = kw
    #devWindow()

#Sql, py project - conect python GUI with sql data base
#
#Bastian Lipka -

    
    
    
    