import random
import sqlite3
import math

def createCompanies():
    """
    creates random company stats
    amount = list of companynames
    """

    nameArray = [
        "Tesla",
        "Apple",
        "Mojang",
        "Nvidia",
        "SpaceX",
        ]
    # data sets will be changed to sql

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
    # data sets will be changed to sql

#id name hq geld
    
    conn = sqlite3.connect("kw.sql")

    cur = conn.cursor()

    numId = 1000
    
    for company in nameArray:
        numId += 1
        id = f"{company[0]}{company[1]}{numId}"


        money = random.randint(50000, 1000000)
        hq = orteArray[random.randint(0, (len(orteArray) - 1))]
        name = company

        command = f"INSERT INTO company VALUES('{id}', '{name}', '{hq}', {money})"

        cur.execute(command)
        conn.commit()
        print(command)

    conn.close()
def generatePosition(xp):
    rank = [
        'Intern',
        'Designer',
        'Developer',
        'Product Manager',
        'Sales Manager',
        ]
    #data sets will be changed to sql


    if xp <= 5:
        position = rank[0]
    elif xp <= 10 and xp > 5:
        position = rank[1]
    elif xp <= 15 and xp > 10:
        position = rank[2]
    elif xp <= 20 and xp > 15:
        position = rank[3]
    elif xp <= 25 and xp > 20:
        position = rank[4]
    
    return position
def salaryRand(position):
    """get salary based on position in company needs position asa argument"""
    salary = 0
    
    if position == 'Intern':
        salary = random.randint(0, 1200)
    elif position == 'Designer':
        salary = random.randint(1200, 3500)
    elif position == 'Developer':
        salary = random.randint(2500, 4000)
    elif position == 'Product Manager':
        salary = random.randint(2900, 5200)
    elif position == 'Sales Manger':
        salary = random.randint(1000, 6500)
    
    
    return salary 


def createEmployees(count):
    """
    creates random employees table
    the amount = count argument
    """

    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()

    name = [
        "Juste",
        "Qillaq",
        "Wilfrith",
        "Galenos",
        "Vitalianus",
        "Godtfred",
        "Keila",
        "Randal",
        "Sven",
        "Mattis",
        "Tryphosa",
        "Timotei",
        "Finn",
        "Simran",
        "Livy",
        "Ellis",
        "Kishori",
        "Nichole",
        "Ekaterian",
        "Opaline",
        "Lottie",
        "Hemming",
        "Antipatros",
        "Vassiliki",
        "Fred",
        "John",
        "Bart",
        "Britta",
        "Jeff"
    ]
    # data sets will be changed to sql
    sirname = [
        "Helios",
        "Aniketos",
        "Eutychios",
        "Mirella",
        "Nathan",
        "Valentinianus",
        "Nalini",
        "Golzar",
        "Abraham",
        "Radzimierz",
        "Ruaidri",
        "Khalid",
        "Milla",
        "Eos",
        "Elaine",
        "Baldomero",
        "Uni",
        "Madilynn",
        "Shreya",
        "Erika",
        "Bilyana",
        "Yoselin",
        "Gali",
        "Fred",
        "James",
        "Patrik",
        "Swanson"
    ]
    # data sets will be changed to sql
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
    # data sets will be changed to sql
    

    companyCommand = f"SELECT * FROM company"
    companyTable = cur.execute(companyCommand).fetchall()

    numId = 1000

    for i in range(count):
        numId += 1

        company_id = companyTable [random.randint(0, (len(companyTable) - 1))][0]
        experience = random.randint(0, 25)
        residence = orteArray[random.randint(0, (len(orteArray) - 1))]
        randName = name[random.randint(0, (len(name) - 1))]
        randSirName = sirname[random.randint(0, (len(sirname) - 1))]
        id = f"{randSirName[0]}{randSirName[1]}{numId}"
        position = generatePosition(experience)
        hiring_date = hiringDateGenerator()
        salary = salaryRand(position)
        project_id = "NULL"
        
        command = f"INSERT INTO employee VALUES('{id}', '{randName}', '{randSirName}', '{position}', '{experience}', '{residence}', '{salary}', '{hiring_date}', '{company_id}', '{project_id}')"
        cur.execute(command)
        print(command)
        conn.commit()
        
    conn.close()
def hiringDateGenerator():
    """
    generates a random date between 2000, 2021
    always beginning with the first of the month
    """

    year = random.randint(2000, 2021)
    month = random.randint(1, 12)
    if month < 10:
        month = f"0{month}"
    day = "01"

    date = f"{year}-{month}-{day}"
    return date

def createProject():
    """
    creates Random Projects amount is based on the number of names there are
    id is created trough the name and an id num ex. "pl1015"
    """

    projectName = [
        'placeHolder1',
        'placeHolder2',
        'placeHolder3',
        'placeHolder4',
        'placeHolder5',
        'placeHolder6',
        'placeHolder7',
        'placeHolder8',
        'placeHolder9',
        'placeHolder10',
        'placeHolder11',
        'placeHolder12',
        
        ]
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    
    f = 1000
    for i in projectName:
        f += 1
        proid = f"{i[0:1]}{f}"
        difficulty = random.randint(50, 200)
        
        returnSalary = 1000 * (1 + (math.sin((0.0025*difficulty) * math.pi))) * 7
        #sin adds a multipier to the base value so salary is based on the difficulty

        print()
        command = f"INSERT INTO project VALUES('{proid}', '{i}', {difficulty}, {returnSalary} )"
        cur.execute(command)
        conn.commit()
        print(command)
         
    
    pass

def checkTable(table):
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()


    command = f"SELECT * FROM {table}"
    out = cur.execute(command).fetchall()
    for i in out:
        print(i)

    conn.close()


    pass

def resourceTable():
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()

    resourceName = [
        ["coal", 0.15],
        ["diamond", 36000000],
        ["silicon", 1.7],
        ["Aluminium", 1.8],
        ["Steel", 0.45],
        ["Plastic", 0.0738],
        ["Wood", 1.15],

    ]

    for i in resourceName:
        command = f"INSERT INTO resource VALUES('{i[0]}', {i[1]})"
        cur.execute(command)
        conn.commit()
        print(command)


def delTable(table):
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    command = f"DELETE FROM {table}"
    cur.execute(command)
    conn.commit()
    conn.close()
    pass

def codeSql():
    while True:
        userInput = input(":")
        executeSqlCommand(userInput)

def executeSqlCommand(command):
    print(command)
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    table = cur.execute(f"{command}").fetchall()
    conn.commit()
    conn.close()
    print('done')
    print(table)
    pass


if __name__ == '__main__':
    #createCompanies()
    #creates companies with, random hq place, random money

    #outputs table content in consol - parameter = table name

    #delete table content - dev tool
    #delTable("project")

    #createEmployees(30)
    ### --> cap in copany einführen für unterschiedliche mitarbeiter zahlen
    
    #checkTable("resource")

    #resourceTable()
    #createProject()
    
    #codeSql()
    #quick sql terminal for debuging


#Sql, py project - conect python GUI with sql data base
#
#Bastian Lipka -
