import random
import sqlite3


def createProject(name, returnMoney, difficulty):
    """
    creates Random Projects amount is based on the number of names there are
    id is created trough the name and an id num ex. "pl1015"
    """

    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()

    command = "SELECT * FROM project"
    prevId = cur.execute(command).fetchall()[-1][0]
    print(prevId)

    f = int(prevId[1:]) + 1

    proid = f"{name[0:1]}{f}"

    command = f"INSERT INTO project VALUES('{proid}', '{name}', {difficulty}, {returnMoney})"
    cur.execute(command)
    conn.commit()
    print(command)

    requiredResourceTable(proid, difficulty)

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