import random
import sqlite3
import time 
from datetime import datetime
import tkinter as tk

def generatePosition(xp):
    rank = [
        'Intern',
        'Designer',
        'Developer',
        'Product Manager',
        'Sales Manager',
        ]
    #data sets will be changed to sql
    print(xp)

    if xp <= 5:
        position = rank[0]
    elif xp <= 10 and xp > 5:
        position = rank[1]
    elif xp <= 15 and xp > 10:
        position = rank[2]
    elif xp <= 20 and xp > 15:
        position = rank[3]
    elif xp > 20:
        position = rank[4]

    return position

def addEmployee(firstName, lastName, salary, exp, company, canvas):
    orteArray = [
        "Moskau",
        "London",
        "Berlin",
        "Weisenheim am Sand",
        "Lambsheim",
        "Rom",
        "Wien",
        "Paris",
        "Belgrad",
        "Kasan",
        "Sofia",
        "Perm",
        "Dnipro",
        "New York",
        "Rio",
        "Sao Paulo",
    ]
    
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    
    command = "SELECT * FROM employee"
    prevId = cur.execute(command).fetchall()[-1][0]
    
        
    idEmployee = int(prevId[2:]) + 1
    
    idEmp = f"{firstName[0]}{lastName[0]}{idEmployee}"
    
    companyName = str()

    # cuts try to cut up - input is weird
    for i in company:
        if i == "(" or i == ")" or i == "," or i == "'":
            pass
        else:
            companyName = companyName + i
    print(companyName)
    
    command = f"SELECT * FROM company WHERE name = '{companyName}'"
    company_id = cur.execute(command).fetchall()[0][0]
    
    residence = orteArray[random.randint(0, (len(orteArray) - 1))]
    print(exp)
    position = generatePosition(int(exp))
    
    hiring_date = datetime.today().strftime('%Y-%m-%d')
    project_id = None
    
    command = f"INSERT INTO employee VALUES('{idEmp}', '{firstName}', '{lastName}', '{position}', '{exp}', '{residence}', '{salary}', '{hiring_date}', '{company_id}', '{project_id}')"
    cur.execute(command)
    conn.commit()
    
    print(command)

    color = f"#{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
    checkLabel = tk.Label(canvas, bg=color, text="Angestellter Hinzugef??gt!")
    checkLabel.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)
    
if __name__ == '__main__':
    addEmployee("horst", "maier", 25000, 14, "Tesla")


def createCompany(name, money, hq, canvas):
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()

    command = "SELECT * FROM company"
    prevId = cur.execute(command).fetchall()[-1][0]
    print(prevId)

    f = int(prevId[2:]) + 1

    idComp = f"{name[0:2]}{f}"

    command = f"INSERT INTO company VALUES('{idComp}', '{name}', '{hq}', {money})"
    cur.execute(command)
    conn.commit()

    resources_owned_by_company(idComp)

    color = f"#{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
    checkLabel = tk.Label(canvas, bg=color, text="Firma Hinzugef??gt!")
    checkLabel.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)

def resources_owned_by_company(idComp):
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()

    command = f"SELECT * FROM resource"
    resourceNames = cur.execute(command).fetchall()

    for i in resourceNames:
        resource = i[0]
        amount = random.randint(10000, 200000)
        command = f"INSERT INTO resources_owned_by_company VALUES('{idComp}', '{resource}', {amount})"
        cur.execute(command)
        conn.commit()
        print(command)

def createProject(name, returnMoney, difficulty, canvas):
    """
    creates Random Projects amount is based on the number of names there are
    id is created trough the name and an id num ex. "pl1015"
    """

    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()

    command = "SELECT * FROM project"
    prevId = cur.execute(command).fetchall()[-1][0]
    print(prevId)

    f = int(prevId[2:]) + 1

    proid = f"{name[0:2]}{f}"

    command = f"INSERT INTO project VALUES('{proid}', '{name}', {difficulty}, {returnMoney})"
    cur.execute(command)
    conn.commit()
    print(command)

    requiredResourceTable(proid, difficulty)

    color = f"#{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
    checkLabel = tk.Label(canvas, bg=color, text="Projekt Hinzugef??gt!")
    checkLabel.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)

def requiredResourceTable(id, difficulty):
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()

    command = f"SELECT name FROM resource"
    resourceId = cur.execute(command).fetchall()

    for j in resourceId:
        command = f"INSERT INTO required_resources VALUES('{id}', '{j[0]}', {random.randint(0, int(difficulty))})"
        cur.execute(command)
        print(command)
        conn.commit()

    print("project added :)")

def delCompany(company, canvas):
    companyName = str()

    # cuts try to cut up - input is weird
    for i in company:
        if i == "(" or i == ")" or i == "," or i == "'":
            pass
        else:
            companyName = companyName + i

    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
        
    command = f"SELECT id FROM company WHERE name = '{companyName}'"
    companyId = cur.execute(command).fetchall()[0][0]
    
    command = f"DELETE FROM company WHERE id = '{companyId}'"
    cur.execute(command)
    conn.commit()
    
    command = f"DELETE FROM employee WHERE company_id = '{companyId}'"
    cur.execute(command)
    conn.commit()
    
    command = f"DELETE FROM resources_owned_by_company WHERE company_id = '{companyId}'"
    cur.execute(command)
    conn.commit()
    
    color = f"#{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
    checkLabel = tk.Label(canvas, bg=color, text=f"{companyName} ZERST??RT!!")
    checkLabel.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)

def delTable(table):
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    command = f"DELETE FROM {table}"
    cur.execute(command)
    conn.commit()
    conn.close()

def ende():
    delTable("employee")
    delTable("company")
    delTable("project")
    delTable("required_resources")
    delTable("resources_owned_by_company")
    delTable("resource")