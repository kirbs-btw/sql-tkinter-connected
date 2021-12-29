import tkinter as tk
from tkinter import ttk
import sqlite3
import os

class selectProject:

    def __init__(self, n):
        self.id = n

projectObj = selectProject(None)

def getCompanyList():
    """
    gets the company list for the dropdown menu and other
    applictions

    used sql table is kw.sql

    :return: company table as 2d array
    """

    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    command = f"SELECT name FROM company"
    companyList = cur.execute(command).fetchall()
    conn.close()
    
    return companyList

def destroyWidget(frame):
    """
    :param frame: frame = the frame where the children will be killed
    :return: none - kills the children of frame
    """

    widgets = frame.winfo_children()
    for widget in widgets:
        widget.destroy()
    

def printEmployees(company, frame):
    """
    :param company: company name to get the employees of the company
    :param frame: frame where to display the information
    :return: none it returns the information via the scrollbar in the frame
    """
    destroyWidget(frame)
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    companyName = str()
    
    #cuts try to cut up - input is weird
    for i in company:
        if i == "(" or i == ")" or i == "," or i == "'":
            pass
        else:
            companyName = companyName + i
    command = f"SELECT DISTINCT employee.name, employee.lastname, employee.position, employee.experience, employee.id FROM company, employee WHERE employee.company_id = (SELECT id FROM company WHERE name = '{companyName}') ORDER BY employee.experience DESC"
    employeeTable = cur.execute(command).fetchall()
    printTable(frame, employeeTable)
    
    conn.close()
        
    pass

def printTable(frame, table):
    """
    :param frame: frame where it puts the information
    :param table: table with the information (table is 2d)
    :return: Nothing - returns the values inside the scrollbar table
    """

    #print(table)
    f = 0
    for i in table:
        f += 1
        tk.Label(frame, text=i[0], justify="left").grid(row=f, column=1, pady=10, padx=10, sticky="w")
        tk.Label(frame, text=i[1], justify="left").grid(row=f, column=2, pady=10, padx=10, sticky="w")
        tk.Label(frame, text=i[2], justify="left").grid(row=f, column=3, pady=10, padx=10, sticky="w")
        tk.Label(frame, text=i[3], justify="left").grid(row=f, column=4, pady=10, padx=10, sticky="w")
        tk.Button(frame, text="pick", justify="left", command = lambda m = i[4]: printID(m)).grid(row=f, column=5, pady=10, padx=10, sticky="w")

def printID(f):
    print(f)

def printTableProjects(frame, root):
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
        tk.Button(frame, text = "Choose Project", justify="left", command = lambda m = i[0]: chooseProject(m, root)).grid(row=f, column=5, pady=10, padx=10, sticky="w")

def chooseProject(projectId, root):
    """

    selected project id gets saved in projectObj for later use

    :param projectId: id of the selected Project
    :param root: root of the projects window so it can be closed

    opens mainWindow again so you can select a company to do the project for you
    """

    projectObj.id = projectId
    root.destroy()
    #print(projectObj.id)
    mainWindow()

def printProjectReq(canvas):
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    command = f"SELECT * FROM required_resources WHERE project_id LIKE '{projectObj.id}'"
    table = cur.execute(command).fetchall()
    command = f"SELECT * FROM project WHERE id = '{projectObj.id}'"
    projectInfoTable = cur.execute(command).fetchall()
    #print(projectInfoTable)
    #print(table)
    f = 1
    if projectInfoTable != []:
        projectInfo = f"{projectInfoTable[0][0]} : {projectInfoTable[0][1]} : {projectInfoTable[0][2]} : {projectInfoTable[0][3]}"
        tk.Label(canvas, text=projectInfo).grid(row=f, column=4, pady=10, padx=10, sticky="w")


    for i in table:
        f += 1
        text = f"{i[1]}: {i[2]}"
        tk.Label(canvas, text=text).grid(row=f, column=4, pady=10, padx=10, sticky="w")

    pass
        
def openProjectsWindow(root):
    """
    the projects window has the purpose to let the user select a project from the list

    :param root: root of the previous window - destroys the previous window
    :return: none - return is the window poping up
    """

    root.destroy()
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
    
    printTableProjects(frameScroll, root)
    
    root.mainloop()

def mainWindow():
    """
    main user interface
    used to select companies and employees

    also there is a secrete button behind the kw logo :) shhhht
    password = kw

    :return: none - return = window poping up for the user
    """

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
    projectsWindowButton = tk.Button(canvas, command = lambda: openProjectsWindow(root), text = "Choose project")
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


    #### scrollbar stuff - employee list#############################
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

    #### scrollbar stuff - resource list#############################
    tableReq = tk.Canvas(canvas, bg="black")
    tableReq.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.3, anchor='nw')
    # create a main frame
    mainFrameReq = tk.Frame(tableReq, bg="#ffffff")
    mainFrameReq.pack(fill='both', expand=1)
    # canvas
    canvas1Req = tk.Canvas(mainFrameReq)
    canvas1Req.pack(side='left', fill='both', expand=1)
    # scrollbar
    canvScrollReq = ttk.Scrollbar(mainFrameReq, orient='vertical', command=canvas1Req.yview)
    canvScrollReq.pack(side='right', fill='y')
    # cofig canvas
    canvas1Req.configure(yscrollcommand=canvScrollReq.set)
    canvas1Req.bind('<Configure>', lambda e: canvas1Req.configure(scrollregion=canvas1Req.bbox("all")))
    # create another frame in canvas
    frameScrollReq = tk.Frame(canvas1Req)
    # add fram to window in canvas
    canvas1Req.create_window((0, 0), window=frameScrollReq, anchor="nw")
    ##############################################################



    #add mitarbeiter
    #angaben inputs
    
    #mitarbeiter projekte zuweisen
    
    #project start
    
    printEmployees(selectedCompany.get(), frameScroll)
    printProjectReq(frameScrollReq)

    root.mainloop()

def login(entry, root):
    """
    checks if the password is correct

    :param entry: password try entry = entry.get() so entry is a string here
    :param root: root of the login window has to be killed if the password is right
    :return: none - return in form of a new window poping up
    """

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
    """
    creates login window for the development terminal
    access only via correct password

    :return: none - returns a login window
    """

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
    """
    :param command: sql command a string
    :return: return is printed in the console by now
    """

    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    table = cur.execute(command).fetchall()
    conn.commit()
    conn.close()
    print(table)
    pass

def devWindow():
    """
    creates a development window with a sql terminal and other
    useful elements - comming soon

    :return: none - returns a window for the user
    """

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
    
    # password to dev Window is = kw

    #devWindow()

#Sql, py project - connect python GUI with sql data base
#
#Bastian Lipka -

    
    
    
    