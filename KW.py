import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import editTables

class selectProject:

    def __init__(self, n):
        self.id = n

class selectEmployee:

    def __init__(self, n):
        self.employee = n

projectObj = selectProject(None)

arr = []
employeeObj = selectEmployee(arr)

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


def printEmployees(company, frame, canvas):
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
    printTable(frame, employeeTable, canvas)

    conn.close()

    pass

def printTable(frame, table, canvas):
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
        tk.Button(frame, text="pick", justify="left", command = lambda m = i[4], l = f: collectId(canvas ,m, frame, l)).grid(row=f, column=5, pady=10, padx=10, sticky="w")

def collectId(canvas ,f, frame, col):
    """
    collects the id´s of the picked employees

    :param f: id of the pickes employee == string with 6 charakters
    :param frame: frame where the buttons are in
    :param col: column of the button
    :return: none prints results in employeeObj as a list ( employeeObj.employee.append(f) )
    """

    # deletes the button of the pick employee
    #
    # bug after the first button is deleted the next shifts wrongly
    #buttonNum = 0
    #done = True
    #widgets = frame.winfo_children()
    #for widget in widgets:
    #    if type(widget) == type(tk.Button()):
    #        buttonNum += 1
    #    if buttonNum == col and done:
    #        widget.destroy()
    #        done = False



    employeeObj.employee.append(f)
    printSkill(canvas)

    print(employeeObj.employee)


def printSkill(canvas):
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    skillCount = 0
    for i in employeeObj.employee:
        command = f"SELECT experience FROM employee WHERE id = '{i}'"
        skill = cur.execute(command).fetchall()
        skillCount = skillCount + skill[0][0]
        print(skillCount)
    text = f"Skill:\n{str(skillCount)}"
    skill = tk.Label(canvas, text=text)
    skill.place(relx=0.3, rely=0.8, relwidth=0.2, relheight=0.05, anchor='nw')
    pass

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
        tk.Label(frame, text=round(i[3], 2), justify="left").grid(row=f, column=3, pady=10, padx=10, sticky="w")
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
    employeeObj.employee = []
    root.destroy()
    #print(projectObj.id)
    mainWindow()

def printDiffireq(canvas):
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    command = f"SELECT difficulty FROM project WHERE id = '{projectObj.id}'"
    table = cur.execute(command).fetchall()
    conn.close()

    if table != []:
        text = f"Required Skill: \n{table[0][0]}"
        diffLabel = tk.Label(canvas, text=text)
        diffLabel.place(relx=0.05, rely=0.8, relwidth=0.2, relheight=0.05, anchor='nw')

        skill = tk.Label(canvas, text = "skill\n0")
        skill.place(relx=0.3, rely=0.8, relwidth=0.2, relheight=0.05, anchor='nw')

def doProject(canvas, company):
    """
    does the project
    looks at the resource of the company and the skill of the employees
    to get the result of the project

    """
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()

    command = f"SELECT difficulty FROM project WHERE id = '{projectObj.id}'"
    projDifficulty = cur.execute(command).fetchall()[0][0]

    skillCount = 0
    for i in employeeObj.employee:
        command = f"SELECT experience FROM employee WHERE id = '{i}'"
        skill = cur.execute(command).fetchall()
        skillCount = skillCount + skill[0][0]

    skillEmployee = skillCount

    # brakes function if skill is not => difficulty
    if skillEmployee < projDifficulty:
        return False

    # delete resource from company
    companyName = str()

    # cuts try to cut up - input is weird
    for i in company:
        if i == "(" or i == ")" or i == "," or i == "'":
            pass
        else:
            companyName = companyName + i

    command = f"SELECT id FROM company WHERE name LIKE '{companyName}'"
    companyId = cur.execute(command).fetchall()[0][0]

    print(companyId)

    command = f"SELECT * FROM resources_owned_by_company WHERE company_id = '{companyId}' ORDER BY resource_id"
    companyResource = cur.execute(command).fetchall()

    command = f"SELECT * FROM required_resources WHERE project_id = '{projectObj.id}' ORDER BY resource_id"
    resourcesRequired = cur.execute(command).fetchall()


    j = 0
    # print(companyResource)

    # deleting the resources required from the resources_owned_by_company table
    for i in resourcesRequired:
        print(i)
        newResource = companyResource[j][2] - i[2]
        command = f"UPDATE resources_owned_by_company SET amount = {newResource} WHERE company_id LIKE '{companyResource[j][0]}' AND resource_id LIKE '{i[1]}'"
        cur.execute(command)
        conn.commit()
        j += 1

    # adding the money from the project to the company Table
    command = f"SELECT * FROM project WHERE id LIKE '{projectObj.id}'"
    returnMoney = cur.execute(command).fetchall()

    command = f"SELECT * FROM company WHERE name LIKE '{companyName}'"
    companyMoney = cur.execute(command).fetchall()
    print(companyMoney)

    addedMoney = returnMoney[0][3] + companyMoney[0][3]

    command = f"UPDATE company SET money = {addedMoney} WHERE name = '{companyName}'"
    cur.execute(command)
    conn.commit()

    # deleting the project

    command = f"DELETE FROM project WHERE id = '{projectObj.id}'"
    cur.execute(command)
    conn.commit()

    # reset projectObj

    projectObj.id = None

    return True

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


    refreshButton = tk.Button(canvas, image=refreshImg, borderwidth=0, bg='#ffffff', command = lambda: printEmployees(selectedCompany.get(), frameScroll, canvas))
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


    if projectObj.id != None:
        doProjectButton = tk.Button(canvas, text="execute", command=lambda: doProject(canvas, selectedCompany.get()))
        doProjectButton.place(relx=0.6, rely=0.8, relwidth=0.2, relheight=0.05, anchor='nw')


    #add mitarbeiter
    #angaben inputs

    #mitarbeiter projekte zuweisen

    #project start

    printDiffireq(canvas)

    printEmployees(selectedCompany.get(), frameScroll, canvas)

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

    # executeButton = tk.Button(canvas, borderwidth=0, text = "okookokokokokokok", bg='#ffffff', command = lambda: executeSqlCommand(commandInput.get()))
    # executeButton.place(relx = 0.05, rely=0.2, relwidth=0.5, relheight=0.03)

    # commandInput = tk.Entry(canvas)
    # commandInput.place(relx = 0.05, rely=0.25, relwidth=0.5, relheight=0.03)

    # add new project
    inputHeight = 0.03
    inputWidth = 0.15

    # add project ###############################################################
    canvas.create_text(100, 150, text="Project hinzufügen", anchor="n")

    canvas.create_text(55, 215, text="Name", anchor="w")
    nameInput = tk.Entry(canvas)
    nameInput.place(relx=0.069, rely=0.3, relwidth=inputWidth, relheight=inputHeight)

    canvas.create_text(55, 275, text="schwierigkeit", anchor="w")
    difficultyInput = tk.Entry(canvas)
    difficultyInput.place(relx=0.069, rely=0.385, relwidth=inputWidth, relheight=inputHeight)

    canvas.create_text(55, 335, text="einnahme", anchor="w")
    returnInput = tk.Entry(canvas)
    returnInput.place(relx=0.069, rely=0.47, relwidth=inputWidth, relheight=inputHeight)

    addProjButton = tk.Button(canvas, text="Hinzufügen",command=lambda: editTables.createProject(nameInput.get(), returnInput.get(), difficultyInput.get()))
    addProjButton.place(relx=0.069, rely=0.555, relwidth=inputWidth, relheight=inputHeight)
    
    #############################################################################
    
    #add Employee ###############################################################
    # name lastname salary (hireringdate) company
    
    canvas.create_text(350, 150, text="Mitarbeiter hinzufügen", anchor="n")

    empNameInput = tk.Entry(canvas)
    empNameInput.place(relx=0.38, rely=0.3, relwidth=inputWidth, relheight=inputHeight)

    empLastNameInput = tk.Entry(canvas)
    empLastNameInput.place(relx=0.38, rely=0.385, relwidth=inputWidth, relheight=inputHeight)

    experienceInput = tk.Entry(canvas)
    experienceInput.place(relx=0.38, rely=0.47, relwidth=inputWidth, relheight=inputHeight)
    
    salaryInput = tk.Entry(canvas)
    salaryInput.place(relx=0.38, rely=0.555, relwidth=inputWidth, relheight=inputHeight)
    
    #dropdown companylist
    companyList = getCompanyList() 

    #Variable, die immer der gleichen Wert haben soll, wie das, was im Menü ausgewählt ist
    selectedCompany = tk.StringVar(canvas)
    selectedCompany.set(companyList[0])

    #Hier kommt das eigentliche Menü, wird mit dem fenster und der Variable ausgewaehlt verknüpft
    companyDropdown = tk.OptionMenu(root, selectedCompany, *companyList)
    companyDropdown.place(relx = 0.38, rely=0.640, relwidth=inputWidth, relheight=inputHeight)
    
    addEmployeeButton = tk.Button(canvas, text="Hinzufügen", command=lambda: editTables.addEmployee(empNameInput.get(), empLastNameInput.get(), salaryInput.get(),experienceInput.get(), selectedCompany.get()))
    addEmployeeButton.place(relx = 0.38, rely=0.725, relwidth=inputWidth, relheight=inputHeight)
    
    ###################################################################################
    
    canvas.create_text(600, 150, text="Firma Hinzufügen", anchor="n")

    canvas.create_text(550, 215, text="Name", anchor="w")
    compNameInput = tk.Entry(canvas)
    compNameInput.place(relx=0.73, rely=0.3, relwidth=inputWidth, relheight=inputHeight)

    canvas.create_text(550, 275, text="Geld", anchor="w")
    compMoneyInput = tk.Entry(canvas)
    compMoneyInput.place(relx=0.73, rely=0.385, relwidth=inputWidth, relheight=inputHeight)

    canvas.create_text(550, 335, text="Hauptsitz", anchor="w")
    compHqInput = tk.Entry(canvas)
    compHqInput.place(relx=0.73, rely=0.47, relwidth=inputWidth, relheight=inputHeight)

    addCompanyButton = tk.Button(canvas, text="Hinzufügen",command=lambda: editTables.createCompany(compNameInput.get(), compMoneyInput.get(), compHqInput.get()))
    addCompanyButton.place(relx=0.73, rely=0.555, relwidth=inputWidth, relheight=inputHeight)

    root.mainloop()






if __name__ == '__main__':
    mainWindow()

    # password to dev Window is = kw

    #devWindow()

#Sql, py project - connect python GUI with sql data base
#
#Bastian Lipka -
